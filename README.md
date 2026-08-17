# Two Spoons

A calorie tracker built for two people sharing the same goal. One file, no build step,
no backend, no account — open `index.html` in any browser and it runs.

Inspired by the parts of LoseIt! and Cal AI that actually get used day to day.

## What it does

- **Two profiles side by side.** Each person gets a calorie budget derived from sex, age,
  height, weight, activity level and goal (Mifflin-St Jeor), recalculated automatically
  as logged weight changes.
- **Daily log** with a calorie ring, remaining count, protein/carb/fat bars, meals split
  into breakfast / lunch / dinner / snacks, streaks, copy-yesterday, and day-by-day history.
- **Plain-language logging.** Type `kaya toast + 2 soft boiled eggs and kopi c` and it
  parses the quantities and matches each item — no photo API, no per-scan cost.
- **~115-item food database** weighted toward Singapore hawker food (chicken rice, char
  kway teow, laksa, cai fan, the full kopi/teh matrix) plus everyday staples, with search,
  recents, a portion stepper, and custom foods.
- **Shared view** — both people's numbers, streaks, weekly chart and weight trends together.
- **Trends** — 14-day intake against your budget line, plus weight logging and trend chart.

## Storage

There is no server, so data stays on the device. Persistence tries three tiers in order
and reports which one is live in Settings:

| Tier | When it's used |
|---|---|
| `localStorage` | Normal browsers. The usual case. |
| IndexedDB | When `localStorage` is blocked but IndexedDB isn't (some embedded/sandboxed viewers). |
| In-memory | Everything blocked. Data survives while the tab is open; the app says so plainly and offers one-tap backup, plus a warning before you close with unsaved changes. |

## Using it on two phones

Each device keeps its own copy. To combine them, one person exports from Settings and the
other imports — entries merge by id, so importing twice never duplicates or loses anything.

## Accuracy

Calorie and macro values are typical-portion estimates meant for spotting trends, not
laboratory figures. Budgets use Mifflin-St Jeor with a standard activity multiplier.
This is not medical advice.

## License

MIT
