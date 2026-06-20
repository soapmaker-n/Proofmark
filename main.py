"""
Proof Vault — write a note, get permanent proof it existed at this moment.

Each entry is saved locally AND pushed to 0G storage. The on-chain root
hash + transaction hash become permanent, verifiable proof that this
exact content existed at this exact time — useful for ideas, drafts,
screenshots, or anything you might need to prove later.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import json
import os
import time
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SIDECAR_DIR = os.path.join(BASE_DIR, "sidecar")
ENTRIES_DIR = os.path.join(BASE_DIR, "entries")
os.makedirs(ENTRIES_DIR, exist_ok=True)

LOCAL_LOG = os.path.join(BASE_DIR, "proof_log.json")


def load_log():
    if os.path.exists(LOCAL_LOG):
        with open(LOCAL_LOG) as f:
            return json.load(f)
    return []


def save_log(log):
    with open(LOCAL_LOG, "w") as f:
        json.dump(log, f, indent=2)


def push_to_0g(entry_path, key, on_done):
    """Runs the Node sidecar in a background thread and calls on_done(result_dict_or_None)."""
    def worker():
        try:
            result = subprocess.run(
                ["node", "sync.js", "push", entry_path, key],
                cwd=SIDECAR_DIR,
                timeout=60,
                capture_output=True,
                text=True,
            )
            tx_data = None
            for line in result.stdout.splitlines():
                if line.startswith("RESULT_JSON:"):
                    tx_data = json.loads(line[len("RESULT_JSON:"):])
            on_done(tx_data, result.stdout, result.stderr)
        except Exception as e:
            on_done(None, "", str(e))

    threading.Thread(target=worker, daemon=True).start()


class ProofVaultApp:
    def __init__(self, root):
        self.root = root
        root.title("Proof Vault — Notarize on 0G")
        root.geometry("600x600")

        tk.Label(root, text="Write something. Save it. Prove it existed.",
                 font=("Segoe UI", 11, "bold")).pack(pady=(12, 4))

        self.text = scrolledtext.ScrolledText(root, wrap="word", font=("Segoe UI", 10))
        self.text.pack(fill="both", expand=True, padx=12, pady=8)

        self.status_label = tk.Label(root, text="", fg="gray", font=("Segoe UI", 9))
        self.status_label.pack(pady=(0, 4))

        btn = tk.Button(root, text="Save & Notarize on 0G", command=self.save_entry,
                         bg="#1a1a2e", fg="white", font=("Segoe UI", 10, "bold"), pady=6)
        btn.pack(pady=(0, 12))

        self.history_box = tk.Listbox(root, height=6)
        self.history_box.pack(fill="x", padx=12, pady=(0, 12))
        self.refresh_history()

    def refresh_history(self):
        self.history_box.delete(0, tk.END)
        for entry in reversed(load_log()):
            root_hash = entry.get('rootHash') or 'pending...'
            label = f"{entry['timestamp']} — {entry['preview']} — {root_hash[:16]}..."
            self.history_box.insert(tk.END, label)

    def save_entry(self):
        content = self.text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo("Empty", "Write something first.")
            return

        entry_id = str(uuid.uuid4())[:8]
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry_path = os.path.join(ENTRIES_DIR, f"{entry_id}.txt")

        with open(entry_path, "w", encoding="utf-8") as f:
            f.write(content)

        log = load_log()
        record = {
            "id": entry_id,
            "timestamp": timestamp,
            "preview": content[:40].replace("\n", " "),
            "rootHash": None,
            "txSeq": None,
        }
        log.append(record)
        save_log(log)
        self.refresh_history()

        self.status_label.config(text="Saved locally. Pushing to 0G...", fg="orange")
        self.text.delete("1.0", tk.END)

        def on_done(tx_data, stdout, stderr):
            log = load_log()
            for r in log:
                if r["id"] == entry_id:
                    if tx_data:
                        r["rootHash"] = tx_data.get("dataMerkleRoot") or tx_data.get("rootHash")
                        r["txSeq"] = tx_data.get("seq") or tx_data.get("txSeq")
                    break
            save_log(log)

            def update_ui():
                self.refresh_history()
                if tx_data:
                    self.status_label.config(text="✅ Notarized on 0G", fg="green")
                else:
                    self.status_label.config(text="0G push failed — saved locally only", fg="red")
                    print("PUSH STDOUT:", stdout)
                    print("PUSH STDERR:", stderr)

            self.root.after(0, update_ui)

        push_to_0g(entry_path, entry_id, on_done)


if __name__ == "__main__":
    root = tk.Tk()
    app = ProofVaultApp(root)
    root.mainloop()
