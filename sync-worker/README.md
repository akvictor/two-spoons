# Two Spoons sync relay

A ~60-line Cloudflare Worker that lets two phones keep a
[Two Spoons](https://akvictor.github.io/two-spoons/) journey in step.

It stores two small blobs — one per phone — plus meal photos, and hands them back.
That is the entire job.

**It cannot read any of it.** Each phone encrypts with AES-GCM before uploading, using a
key that exists only on the two devices and travels only inside an invite. Cloudflare
stores ciphertext.

Each phone writes only its own slot and reads only the other's, so two phones can never
overwrite each other and there is nothing to merge server-side.

## Deploy

[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/akvictor/two-spoons/tree/main/sync-worker)

The KV namespace is created for you. Full walkthrough: [SETUP-SYNC.md](../SETUP-SYNC.md).

## API

| | |
|---|---|
| `GET /health` | liveness check |
| `GET /s/{room}/{who}` | read a phone's state blob |
| `PUT /s/{room}/{who}` | write it (max 4 MB) |
| `GET /p/{room}/{photoId}` | read a meal photo |
| `PUT /p/{room}/{photoId}` | write one (max 2 MB) |

`{room}` is a random 32-character id minted when the journey starts. Knowing it is what
grants access, which is why it only ever travels inside an invite. Stored values expire
after ~13 months untouched.

## Cost

Free tier: 1,000 writes and 100,000 reads a day. Two people logging meals use a handful
of writes an hour, and an idle app writes nothing at all.
