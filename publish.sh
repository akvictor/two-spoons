#!/usr/bin/env bash
# Creates the GitHub repo, pushes, and turns on GitHub Pages.
# Run this after `gh auth login`. Safe to re-run.
set -euo pipefail

OWNER="akvictor"
REPO="two-spoons"
VIS="--public"          # Pages needs public on a free plan; swap to --private if you have Pro
DESC="A two-person calorie tracker in a single HTML file"

cd "$(dirname "$0")"

if ! gh auth status >/dev/null 2>&1; then
  echo "Not signed in yet. Run:  gh auth login"
  exit 1
fi

# 1. Create the repo (skip if it's already there)
if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  echo "Repo $OWNER/$REPO already exists — reusing it."
else
  echo "Creating $OWNER/$REPO ..."
  gh repo create "$OWNER/$REPO" $VIS -d "$DESC"
fi

# 2. Push over SSH — that key already works, so this needs no token
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "git@github.com:$OWNER/$REPO.git"
else
  git remote add origin "git@github.com:$OWNER/$REPO.git"
fi
echo "Pushing ..."
git push -u origin main

# 3. Turn on Pages, serving / from main
echo "Enabling GitHub Pages ..."
if gh api "repos/$OWNER/$REPO/pages" >/dev/null 2>&1; then
  gh api --method PUT "repos/$OWNER/$REPO/pages" \
    -f "source[branch]=main" -f "source[path]=/" >/dev/null
else
  gh api --method POST "repos/$OWNER/$REPO/pages" \
    -f "source[branch]=main" -f "source[path]=/" >/dev/null
fi

echo
echo "Done. Your app will be live in about a minute at:"
echo "   https://$OWNER.github.io/$REPO/"
echo
echo "Open it on both phones and use Share -> Add to Home Screen."
