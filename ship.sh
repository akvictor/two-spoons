#!/usr/bin/env bash
# Ship whatever is in this folder to the live app, then wait until it's actually there.
#
#   ./ship.sh                 # commits with a timestamp
#   ./ship.sh "bigger bowls"  # commits with your own message
#
# Safe to run when nothing changed — it just re-checks that live matches local.
set -uo pipefail
cd "$(dirname "$0")"

URL="https://akvictor.github.io/two-spoons/"
say(){ printf "%s\n" "$*"; }

# --- sanity: don't ship a file that won't run ---
if command -v node >/dev/null 2>&1; then
  if ! node --input-type=module -e "
    import fs from 'fs';
    const s=fs.readFileSync('index.html','utf8');
    const m=s.match(/<script>([\s\S]*)<\/script>/);
    if(!m){console.error('no <script> block found');process.exit(1);}
    new Function(m[1]);
  " 2>/tmp/ship_syntax.txt; then
    say "Stopped: index.html has a JavaScript error, so shipping it would break the app."
    say ""
    sed 's/^/   /' /tmp/ship_syntax.txt
    exit 1
  fi
  say "Checked: the app's code parses."
fi

# --- commit anything new ---
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -q -m "${1:-Update $(date '+%Y-%m-%d %H:%M')}"
  say "Committed your changes."
else
  say "No changes to commit — checking the live copy is current."
fi

# --- push ---
if ! git push -q origin main 2>/tmp/ship_push.txt; then
  say ""
  say "Couldn't push. Git said:"
  sed 's/^/   /' /tmp/ship_push.txt
  say ""
  say "If it mentions rejected/non-fast-forward, run:  git pull --rebase && ./ship.sh"
  exit 1
fi
say "Pushed to GitHub."

# --- wait for the live site to catch up ---
local_sum=$(shasum -a 256 index.html | awk '{print $1}')
printf "Waiting for the live site"
for i in $(seq 1 30); do
  live_sum=$(curl -s -L "$URL" | shasum -a 256 | awk '{print $1}')
  if [ "$live_sum" = "$local_sum" ]; then
    say ""
    say ""
    say "Live and up to date:"
    say "   $URL"
    say ""
    say "On each phone: open that link, then Share -> Add to Home Screen."
    exit 0
  fi
  printf "."
  sleep 10
done

say ""
say ""
say "Pushed fine, but the live site hasn't updated after 5 minutes."
say "GitHub Pages is usually a minute; it may be slow or having problems."
say "Check https://www.githubstatus.com — your work is safely pushed either way."
exit 1
