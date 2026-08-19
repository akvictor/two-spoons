# Two Spoons

A calorie tracker built for two people sharing the same goal. One file, no build step,
no backend, no account — open `index.html` in any browser and it runs.

Inspired by the parts of LoseIt! and Cal AI that actually get used day to day.

## What it does

- **Two profiles side by side**, each with a name you can change at any time and an
  optional photo. Calorie budgets come from sex, age, height, weight, activity level and
  goal (Mifflin-St Jeor), recalculated automatically as logged weight changes.
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
- **Saved meals.** Bundle a meal you eat often into one entry and re-add it in a tap.
- **~115-item food database** weighted toward Singapore hawker food (chicken rice, char
  kway teow, laksa, cai fan, the full kopi/teh matrix) plus everyday staples, and a
  28-activity exercise database.
- **Insights** — 7-day averages, days on target, and a projected weekly weight change with
  an estimated date for reaching your goal weight.
- **Shared view** — both people's numbers, streaks, weekly chart and weight trends together.

## Garmin

Garmin Connect on a computer exports your activities as CSV (**Activities → All Activities
→ Export CSV**); the app reads that file and pulls out date, activity, duration and
calories. Re-importing the same file is safe — entries are keyed by their contents, so
nothing is duplicated.

There is no live Garmin sync, and there cannot be one while the app stays serverless:
Garmin's Health API needs an approved developer account plus a server to receive its
webhooks, and none of that can live in a page running on the phone.

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
other imports — food, exercise, water and weights merge by id, so importing twice never
duplicates or loses anything.

## Accuracy

Calorie and macro values are typical-portion estimates meant for spotting trends, not
laboratory figures. Budgets use Mifflin-St Jeor with a standard activity multiplier, and
exercise burn uses MET values scaled by body weight. If you log workouts, pick a lower
activity level so the same effort is not counted twice. This is not medical advice.

## License

MIT
