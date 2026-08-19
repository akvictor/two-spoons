#!/usr/bin/env python3
"""Log in to Garmin once, here on your own machine, and print a session blob.

Why this exists: Garmin accounts with two-factor turned on cannot be logged into
from a scheduled job, because something has to type the code. So you log in once
interactively, and the resulting session tokens go into a GitHub secret. Nothing
is uploaded by this script and your password is never stored -- it is typed here,
used once, and discarded.

  python3 -m pip install garminconnect
  python3 scripts/garmin_login.py

Copy the block it prints into a repository secret named GARMIN_TOKENS_A
(or GARMIN_TOKENS_B for the second person).
"""
import base64, getpass, io, os, sys, tarfile, tempfile


def main():
    try:
        from garminconnect import Garmin
    except ImportError:
        print("Missing dependency. Run:  python3 -m pip install garminconnect")
        return 1

    email = input("Garmin email: ").strip()
    password = getpass.getpass("Garmin password (not shown, not saved): ")

    g = Garmin(email, password)
    try:
        result = g.login()
        # Newer clients signal a required 2FA code by returning a tuple.
        if isinstance(result, tuple) and result and result[0] == "needs_mfa":
            code = input("Two-factor code from your email or app: ").strip()
            g.resume_login(result[1], code)
    except Exception as e:                          # noqa: BLE001
        print("Login failed: %s" % e)
        print("If you use Google/Apple sign-in for Garmin, set a Garmin password first.")
        return 1

    d = tempfile.mkdtemp()
    g.garth.dump(d)

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as t:
        for name in os.listdir(d):
            t.add(os.path.join(d, name), arcname=name)
    blob = base64.b64encode(buf.getvalue()).decode()

    try:
        name = g.get_full_name()
    except Exception:                               # noqa: BLE001
        name = email
    print("\nLogged in as: %s" % name)
    print("\n--- copy everything between the lines into the GitHub secret ---")
    print(blob)
    print("--- end ---\n")
    print("These tokens act like a logged-in session. Keep them in a GitHub")
    print("secret, never in the repository itself. Re-run this if syncing")
    print("starts failing months from now -- sessions do eventually expire.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
