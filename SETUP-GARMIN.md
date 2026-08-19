# Automatic Garmin sync

A scheduled job logs in to Garmin every 30 minutes, writes your recent activities
to `garmin.json` in this repository, and the app reads that file when you open it.
No server to run and nothing to pay for.

Setting it up takes about ten minutes and only has to be done once.

---

## Before you start: this repository is public

`garmin.json` will be readable by anyone who finds this repository. Workout names,
dates, durations and calories are not nothing — they show when you are reliably out
of the house.

So step 3 sets a passphrase and the job encrypts the file before committing it.
Anyone can download it; only someone with the passphrase can read it. **Skip step 3
only if you genuinely don't mind it being public.**

---

## 1. Get a Garmin session

Garmin blocks scripted logins on accounts with two-factor turned on, so log in once
here on your Mac and hand the resulting session to GitHub.

```bash
python3 -m pip install garminconnect
python3 ~/Desktop/calorie-tracker/scripts/garmin_login.py
```

It asks for your Garmin email, your password, and a two-factor code if you use one.
Your password is used once and never saved. It prints a long block of text — copy it.

## 2. Store it as a secret

Go to **Settings → Secrets and variables → Actions** in this repository
(https://github.com/akvictor/two-spoons/settings/secrets/actions), click
**New repository secret**, and add:

| Name | Value |
|---|---|
| `GARMIN_TOKENS_A` | the block printed in step 1 |

Secrets are write-only: the job can read them, nobody browsing the repository can.

Only one of you wears a Garmin? You're done with this bit. If you both do, run step 1
again on the other person's account and save it as `GARMIN_TOKENS_B`.

*Which profile is which:* `_A` is the person on the left in the app, `_B` the one on
the right.

## 3. Add a passphrase (recommended)

Add a second secret:

| Name | Value |
|---|---|
| `SYNC_PASSPHRASE` | any phrase you'll both remember, e.g. `two-spoons-orchid-road` |

The app asks for it once per phone, under **Settings → Garmin**, and remembers it.

## 4. Run it

Go to the **Actions** tab, pick **Garmin sync**, and hit **Run workflow**. It should
finish in under a minute and commit a `garmin.json`. After that it runs by itself
every 30 minutes, and opening the app pulls in whatever is new.

---

## If it doesn't work

**The job fails at login** — the session expired, or two-factor rejected it. Re-run
step 1 and update the secret. Sessions last months, not forever.

**"No profile synced"** — no secrets are set, or the names are misspelled. They are
case-sensitive: `GARMIN_TOKENS_A`, not `garmin_tokens_a`.

**The workflow never runs on its own** — GitHub pauses scheduled jobs on repositories
with no activity for 60 days. Push any commit to wake it up.

**Workouts don't appear in the app** — pull down to refresh, or use **Sync now** in
Settings. If it says the passphrase is wrong, it must match `SYNC_PASSPHRASE` exactly.

**You'd rather not automate it** — the app also imports a Garmin CSV by hand. See the
Garmin section in the README.

---

## What this actually does

`garminconnect` is a community library that talks to the same endpoints the Garmin
Connect website uses. It is not an official Garmin integration — Garmin's supported
API needs a business account and an approved application. In practice the library
works fine for personal use, but Garmin could change things and break it; if that
happens, the CSV import still works, and nothing already in your log is affected.

Activities are read, never written. Nothing is sent back to Garmin.
