# Two Spoons

A calorie tracker built for two people sharing the same goal. One file, no build step,
no backend, no account — open `index.html` in any browser and it runs.

Inspired by the parts of LoseIt! and Cal AI that actually get used day to day.

## What it does

- **One phone each.** You set up only your own details; your partner installs the app,
  taps *Join my partner*, pastes your invite code, and fills in theirs. Each phone owns
  its person — syncing brings the other's progress across without touching your own.
- **A shared journey** — a day count from the moment the first of you started, days you
  both logged, days you were both on target, combined weight change, and milestones.
- Names are editable any time and photos optional. Calorie budgets come from sex, age,
  height, weight, activity level and goal (Mifflin-St Jeor), recalculated as weight changes.
- **Daily log** with a calorie ring, remaining count, protein/carb/fat bars, meals split
  into breakfast / lunch / dinner / snacks, streaks, copy-yesterday, and day-by-day history.
- **Exercise earns calories back**, three ways: pick an activity and minutes and the burn
  is estimated from your weight and the activity's intensity (METs); enter the numbers by
  hand; or import a Garmin Connect activity CSV. Either figure stays editable afterwards,
  and the day's budget updates immediately.
- **Water tracking** against a per-person daily glass target.
- **Four ways to log food** — search, plain language (`kaya toast + 2 soft boiled eggs and
  kopi c` parses quantities and matches each item), quick-add when you just know the
  number, and custom foods you define once and reuse.
- **Four visual styles** — Sticker, Clean, Blossom and Ink — each with its own shape, type
  and palette, plus light/dark/auto. Chosen at first launch and changeable any time under
  Settings, per phone.
- **Your usuals, one tap.** Anything eaten twice or more for a given meal appears as a chip
  under that meal — tap once to log it. Items already logged today drop out, so the row
  stays useful rather than repeating what's on screen.
- **Undo.** Adding, deleting, or copying yesterday can be reversed for a few seconds from a
  toast, so a mis-tap never costs you the entry.
- **Weekly balance.** A day over budget isn't a failed week. Today shows how far under or
  over you are across the last seven days, counting only days you actually logged — an
  unlogged day is unknown, not a surplus.
- **Saved meals.** Bundle a meal you eat often into one entry and re-add it in a tap.
- **777-item food database**, every entry with its own icon and a category, browsable as
  well as searchable — pick Rice, Noodles, Small plates, Breakfast, Roti & Indian, Asian,
  Western, Protein, Veg, Fruit, Drinks, Snacks or Dessert and see everything in it, or
  just type. Heavy on Singapore hawker food (chicken rice, char kway teow, laksa, cai fan,
  kway chap, zi char, dim sum, cai fan sides, the full kopi/teh matrix, nyonya kueh) plus
  Japanese, Korean, Thai, Vietnamese, Indian, Malay, Taiwanese and Western staples, cafe
  brunch, everyday groceries and condiments. Paired with a 28-activity exercise database.
- **A photo of the meal, and you both see them.** Tap any logged item and add a picture —
  camera or photo library. It becomes the item's thumbnail on the day's list, full size
  when tapped, and it travels to your partner when you sync **by file**. A pasted code
  stays text-sized and carries no photos; the file carries them, so AirDrop or WhatsApp
  that across. Photos are stored apart from the saved state (a 6 MB phone photo lands at
  roughly 30–50 KB), which is what keeps codes small enough to paste at all. The last 45
  days travel, up to 200 photos, so a year of meals never becomes a file nobody can send.
  Settings shows the space used and can clear them.
- **Automatic sync.** With a small relay of your own — a free Cloudflare Worker, one
  click to deploy ([SETUP-SYNC.md](SETUP-SYNC.md)) — both phones keep themselves up to date: on open, when
  you switch back to the app, every 45 seconds while it's open, and shortly after
  anything changes. Food, exercise, water, weight and meal photos all travel.
  Everything is encrypted on the phone before it is uploaded, so the relay holds bytes
  it cannot read; the key only ever travels inside an invite. Each phone writes its own
  slot and reads the other's, so there are no conflicts to resolve. Set it up on one
  phone; the other picks it up from the invite with no typing. Manual file sync still
  works and needs no account at all.
- **Whose day you're looking at.** Once you're paired, two chips at the top of Today switch
  between you. Your partner's day is read-only — their phone owns their log — so you can
  see what they ate and the photo they took, but nothing you tap can change it.
- **Barcode scanning.** Add food → **Scan** opens the camera; hold a packaged product's
  barcode in the box and it looks the product up and drops it into the normal portion
  picker. Nothing the camera sees leaves the phone — only the digits are sent.
  Safari ships the browser's own barcode API switched off, so the app decodes EAN-13,
  EAN-8 and UPC-A itself and uses the native detector only where one actually works.
  You can also just type the number under the bars, which needs no camera permission
  at all.
- **Online lookup when something isn't there.** Search, and under the results there's a
  button that asks [Open Food Facts](https://world.openfoodfacts.org) — a free, public
  food database needing no account or key. It only runs when you tap it, because tapping
  it sends what you typed to someone else's server. It reads packaged and barcoded
  products well and cooked hawker food poorly, which is the opposite of the built-in list,
  so the two cover each other. Anything you add from it is kept on the device as a custom
  food, so it works offline from then on.
- **Your budget, your call.** The calculated figure is a starting point; override it with
  your own number any time from Today, Settings, or the welcome screen.
- **Insights** — switch between a week and a month view for averages, a projected weekly
  weight change, and an estimated date for reaching your goal weight.
- **Consistency at a glance** — one square per day (on target / over / not logged) with the
  percentage logged, the percentage on target, and your best run. The Journey tab shows
  both people's grids together, so "how are we doing?" is one look rather than arithmetic.
  Days before the journey began are marked separately so they don't count as misses.
- **Shared view** — both people's numbers, streaks, weekly chart and weight trends together.

## Garmin

Garmin Connect on a computer exports your activities as CSV (**Activities → All Activities
→ Export CSV**); the app reads that file and pulls out date, activity, duration and
calories. Re-importing the same file is safe — entries are keyed by their contents, so
nothing is duplicated.

For hands-off syncing, a scheduled GitHub Action logs in to Garmin every 30 minutes
and commits your recent activities as `garmin.json`; the app reads it on open and
merges anything new. Because this repository is public the file is encrypted with a
passphrase you choose, so only your two phones can read it. Setup is in
[SETUP-GARMIN.md](SETUP-GARMIN.md).

This uses a community library against Garmin's own web endpoints rather than their
official Health API, which needs an approved business account and a server to receive
webhooks. It works well in practice, and the CSV import remains as a fallback.

## Shipping a change

Edit `index.html`, then from this folder:

```sh
./ship.sh "what you changed"
```

It checks the app still parses (and refuses to publish a broken file), commits, pushes,
and waits until the live site is actually serving your change before it says done.
The message is optional. Running it with nothing changed just re-confirms live matches
local.

## Storage

There is no server, so data stays on the device. Persistence tries three tiers in order
and reports which one is live in Settings:

| Tier | When it's used |
|---|---|
| `localStorage` | Normal browsers. The usual case. |
| IndexedDB | When `localStorage` is blocked but IndexedDB isn't (some embedded/sandboxed viewers). |
| In-memory | Everything blocked. Data survives while the tab is open; the app says so plainly and offers one-tap backup, plus a warning before you close with unsaved changes. |

Exports and partner invites are run through a sanitiser that strips secrets, so a backup
file or an invite code can be shared without leaking anything held on the device.

## Using it on two phones

Each device keeps its own copy. One of you starts the journey and sends an invite
(**Settings → Send invite**); the other chooses **Join my partner** during setup. After
that, **Sync now** on either phone merges both sides: food, exercise, water, weights and
favourites merge by id, so syncing twice never duplicates or loses anything. Your own
profile is always authoritative on your own phone.

## Accuracy

Calorie and macro values are typical-portion estimates meant for spotting trends, not
laboratory figures. Budgets use Mifflin-St Jeor with a standard activity multiplier, and
exercise burn uses MET values scaled by body weight. If you log workouts, pick a lower
activity level so the same effort is not counted twice. This is not medical advice.

## License

MIT
