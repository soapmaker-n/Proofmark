# Proofmark
Write something, save it, prove it existed. Every entry is permanently notarized on 0G decentralized storage.

# 🛡️ Proofmark

Write a note. Save it. Get permanent, verifiable proof it existed at 
this exact moment — stored forever on 0G's decentralized storage 
network.

Built for the [0G Zero Cup](https://0g.ai/arena/zero-cup).

## How it works

Every entry you write is:
1. Saved locally as a plain text file
2. Pushed to 0G decentralized storage via a real on-chain transaction
3. Given a permanent root hash you can use to prove the content existed 
   at that timestamp — verifiable by anyone, forever, independent of 
   this app or your computer

This isn't a bolt-on — 0G storage **is** the actual product. Without 
it, this is just a text file with no way to prove when it was written.

## Use cases
- Proving an idea, draft, or design existed before a certain date
- Timestamping screenshots of bugs, disputes, or agreements
- A permanent, tamper-proof journal

## Features
- Simple, distraction-free writing interface
- One-click save + notarize
- History view showing all past entries and their root hashes
- Works fully offline for writing — only the notarization step needs 
  network access

## ⚙️ Running it (for judges / developers)

This app needs **Node.js** installed in addition to the Windows `.exe`.

1. Download `Proofmark.exe` and `sidecar.zip` from the 
   [Releases](../../releases) page
2. Extract `sidecar.zip` into the same folder as `Proofmark.exe`
3. Install [Node.js](https://nodejs.org) if you don't have it
4. Open a terminal in the `sidecar` folder and run:
5. 5. Copy `env.example` to `.env` inside `sidecar`, and add:
   - Your own wallet's private key (testnet only — get test tokens at 
     [faucet.0g.ai](https://faucet.0g.ai))
   - Default RPC/indexer URLs can stay as-is
6. Run `Proofmark.exe`, write something, click **Save & Notarize on 0G**

## Built with
Python, Tkinter, Node.js, `@0gfoundation/0g-storage-ts-sdk`, ethers.js
Coded with [0g.ai](https://0g.ai)

## ⚠️ Note
0G's testnet can occasionally be slow or briefly unavailable — if a 
push fails, your entry is still saved locally and you can retry.
