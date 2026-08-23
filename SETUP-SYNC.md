# Turning on automatic sync

Do this once, on **one** phone — whoever started the journey. The other phone gets
everything from an invite: no typing, no second setup, nothing to read.

You need a free Cloudflare account. No card, no cost at this size.

---

## The quick way

### 1. Deploy the relay

[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/akvictor/two-spoons/tree/main/sync-worker)

Click that. It will ask you to sign in to Cloudflare (create the account here if you
don't have one) and to connect GitHub so it can copy the worker into your account.

Then press **Deploy**. Cloudflare creates the storage it needs and puts the relay live.
Takes a minute or two.

### 2. Copy its address

When it finishes you get an address like:

```
https://two-spoons-sync.yourname.workers.dev
```

Check it works: open that address with `/health` on the end. It should say `ok`.

### 3. Tell the app

On your phone: **Settings → Automatic sync**, paste the address (without `/health`),
press **Save**. It should turn to **On**.

### 4. Bring your partner in

**Settings → Send invite**, send them the code. When they import it their phone picks up
the address and the key on its own and starts syncing. They never see this page.

**Done.**

---

## If the button misbehaves

Watch for this one — it happened on the first real run. The button can ignore the
`/sync-worker` part of the link and build from the **root** of the repo instead. It then
finds `index.html`, decides you are publishing a website, and deploys a copy of the
tracker app rather than the relay. The giveaway: `/health` returns 404, and the Worker's
settings say *"cannot be added to a Worker that only has static assets"* with
**Bindings: 0**.

Two fixes, either works:

- **Point it at the right folder.** On the Worker: **Settings → Build → Build
  configuration**, set **Root directory** to `sync-worker`, save. Then create the KV
  namespace (below) and push a commit to trigger a rebuild.
- **Or set it up by hand** from scratch — six minutes.

<details>
<summary><b>Manual setup</b></summary>

**Make the storage.** Cloudflare dashboard → **Storage & Databases → KV → Create a
namespace**. Name it `two-spoons`. Copy the **ID** it shows you.

**Make the worker.** **Compute (Workers) → Create → Start with Hello World → Deploy**.
Name it `two-spoons-sync`. Then **Edit code**, delete everything in the editor, paste in
the whole of [`sync-worker/worker.js`](sync-worker/worker.js), and **Deploy** again.

**Connect them.** On the worker: **Settings → Bindings → Add → KV namespace**.

- Variable name: `SYNC` ← exactly this, capitals included
- KV namespace: `two-spoons`

Save, then **Deploy** once more so the binding takes effect.

Now carry on from step 2 above.

</details>

---

## What actually happens

Your phone encrypts everything — food, exercise, weight, meal photos — *before* it leaves
the device. Your partner's phone downloads it and decrypts it. The key never goes to
Cloudflare; it only ever travels inside the invite you send each other. So Cloudflare
holds two blobs it has no way to read.

Each phone writes only its own slot and reads only the other's, so nothing can overwrite
anything and there is no conflict to resolve. Your partner's day appears read-only on
your phone: you see what they ate and the photo they took, but only their phone can
change their log.

Sync runs when you open the app, when you switch back to it, roughly every 45 seconds
while it's open, and shortly after you change something. A failed sync loses nothing —
it catches up next time.

## Will I run out of free tier?

The allowance is 1,000 writes and 100,000 reads a day. Two people logging meals use a
handful of writes an hour, and an idle app writes nothing at all. You will not get near
it.

## When something's wrong

| The app says | What it means |
|---|---|
| Couldn't reach your sync relay | Wrong address, or the relay isn't deployed. Check `/health`. |
| The other phone is using a different invite | One of you is on older credentials. Send a fresh invite and import it. |
| Worker errors mentioning `SYNC` | The storage binding is missing or misnamed. See manual setup. |

## Turning it off

**Settings → Automatic sync → Turn off.** Nothing more is uploaded. To erase what's
stored, delete the KV namespace in the Cloudflare dashboard.
