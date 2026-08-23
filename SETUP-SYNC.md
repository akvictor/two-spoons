# Turning on automatic sync

Do this once, on **one** phone (whoever started the journey). The other phone gets
everything from an invite — no typing, no second setup.

You need a free Cloudflare account. No card, no cost at this size.

---

## 1. Make the account

Go to <https://dash.cloudflare.com/sign-up>, sign up, confirm the email. That's it —
skip anything it offers about adding a domain.

## 2. Make a place to keep the data

In the left sidebar: **Storage & Databases → KV → Create a namespace**.

Call it `two-spoons`. Create it. You'll see it listed with an **ID** — a long string of
letters and numbers. Copy that; you need it in a moment.

## 3. Make the worker

Left sidebar: **Compute (Workers) → Create → Start with Hello World → Deploy**.

Name it `two-spoons-sync`. Once it deploys, click **Edit code**. Delete everything in
the editor, paste in the whole contents of [`sync-worker/worker.js`](sync-worker/worker.js),
and hit **Deploy** again.

## 4. Connect the two

Still on the worker: **Settings → Bindings → Add → KV namespace**.

- Variable name: `SYNC`  ← must be exactly this
- KV namespace: pick `two-spoons`

Save, then **Deploy** once more so the binding takes effect.

## 5. Check it

The worker page shows its address, something like

```
https://two-spoons-sync.yourname.workers.dev
```

Open that address with `/health` on the end. If it says `ok`, it's working.

## 6. Tell the app

On your phone, open **Settings → Automatic sync**, paste the address (without
`/health`), and press **Save**. It should turn to **On**.

## 7. Bring your partner in

**Settings → Send invite** and send them the code. When they import it, their phone
picks up the address and the key by itself and starts syncing. They never see any of
this page.

---

## What actually happens

Your phone encrypts everything — food, exercise, weight, meal photos — *before* it
leaves the device, then uploads it. Your partner's phone downloads it and decrypts it.
The key never goes to Cloudflare; it only travels inside the invite you send each other.

So Cloudflare stores two blobs it has no way to read.

Each phone writes only its own slot and reads only the other's, so nothing can
overwrite anything. Your partner's day shows up read-only on your phone — you can see
what they ate and the photo they took, but only their phone can change their log.

Sync runs when you open the app, when you switch back to it, about every 45 seconds
while it's open, and shortly after you change something. If a sync fails, nothing is
lost — it catches up next time.

## Will I run out of free tier?

The free allowance is 1,000 writes and 100,000 reads a day. Two people logging meals
use a handful of writes an hour — an idle app writes nothing at all. Photos upload once
each and are never rewritten. You will not get near the limits.

## If something goes wrong

- **"Couldn't reach your sync relay"** — the address is wrong, or the worker isn't
  deployed. Check `/health` in a browser.
- **"The other phone is using a different invite"** — one of you is on older
  credentials. Send a fresh invite and import it.
- **Worker returns an error about `SYNC`** — step 4 was missed, or the variable name
  isn't exactly `SYNC`.

## Turning it off

**Settings → Automatic sync → Turn off.** Nothing more is uploaded. To wipe what's
stored, delete the KV namespace in the Cloudflare dashboard.
