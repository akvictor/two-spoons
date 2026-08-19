#!/usr/bin/env python3
"""Pull recent Garmin activities and write them where the app can read them.

Runs in GitHub Actions. Credentials come from repository secrets and are never
written to the output file. If SYNC_PASSPHRASE is set the payload is encrypted
before it is committed, so a public repo does not publish your training log.

Secrets, per profile (suffix A = first person, B = second, both optional):
  GARMIN_TOKENS_A    base64 session tokens from scripts/garmin_login.py  (preferred)
  GARMIN_EMAIL_A     \\ only needed if you are not using tokens; fails on
  GARMIN_PASSWORD_A  / accounts with two-factor turned on
  SYNC_PASSPHRASE    optional; encrypts the output
"""
import os, sys, json, base64, io, tarfile, tempfile, datetime

OUT = "garmin.json"
DAYS_BACK = 45
MAX_ACTIVITIES = 100


def client_for(suffix):
    """Return a logged-in Garmin client for this profile, or None if unconfigured."""
    tokens = os.environ.get("GARMIN_TOKENS_" + suffix, "").strip()
    email = os.environ.get("GARMIN_EMAIL_" + suffix, "").strip()
    password = os.environ.get("GARMIN_PASSWORD_" + suffix, "").strip()
    if not tokens and not (email and password):
        return None

    from garminconnect import Garmin

    if tokens:
        d = tempfile.mkdtemp()
        with tarfile.open(fileobj=io.BytesIO(base64.b64decode(tokens))) as t:
            t.extractall(d)
        g = Garmin()
        g.login(d)                      # resume the saved session
        return g

    g = Garmin(email, password)
    g.login()
    return g


def activities_for(g):
    """Normalise Garmin's activity records down to what the app actually stores."""
    cutoff = (datetime.date.today() - datetime.timedelta(days=DAYS_BACK)).isoformat()
    out = []
    for a in g.get_activities(0, MAX_ACTIVITIES) or []:
        start = a.get("startTimeLocal") or a.get("startTimeGMT") or ""
        date = str(start)[:10]
        if len(date) != 10 or date < cutoff:
            continue
        kcal = a.get("calories") or a.get("activeKilocalories") or 0
        try:
            kcal = int(round(float(kcal)))
        except (TypeError, ValueError):
            continue
        if kcal <= 0:
            continue
        try:
            mins = int(round(float(a.get("duration") or 0) / 60.0))
        except (TypeError, ValueError):
            mins = 0
        name = (a.get("activityName")
                or (a.get("activityType") or {}).get("typeKey")
                or "Garmin activity")
        out.append({"date": date, "name": str(name)[:60], "mins": mins, "kcal": kcal})
    return out


def encrypt(payload, passphrase):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    salt = os.urandom(16)
    iv = os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                     salt=salt, iterations=200000).derive(passphrase.encode())
    ct = AESGCM(key).encrypt(iv, json.dumps(payload).encode(), None)
    b64 = lambda b: base64.b64encode(b).decode()
    return {"v": 1, "enc": True, "salt": b64(salt), "iv": b64(iv), "data": b64(ct)}


def main():
    profiles, errors = {}, []
    for suffix, pid in (("A", "a"), ("B", "b")):
        try:
            g = client_for(suffix)
        except Exception as e:                      # noqa: BLE001 - report, don't crash
            errors.append("%s: login failed: %s" % (suffix, e))
            continue
        if g is None:
            continue
        try:
            profiles[pid] = activities_for(g)
            print("profile %s: %d activities" % (pid, len(profiles[pid])))
        except Exception as e:                      # noqa: BLE001
            errors.append("%s: fetch failed: %s" % (suffix, e))

    if not profiles:
        print("No profile synced. " + ("; ".join(errors) if errors else
              "Set GARMIN_TOKENS_A (or GARMIN_EMAIL_A + GARMIN_PASSWORD_A)."))
        return 1

    payload = {"v": 1,
               "syncedAt": datetime.datetime.now(datetime.timezone.utc)
                            .replace(microsecond=0).isoformat(),
               "profiles": profiles}

    passphrase = os.environ.get("SYNC_PASSPHRASE", "").strip()
    doc = encrypt(payload, passphrase) if passphrase else dict(payload, enc=False)
    if passphrase:
        doc["syncedAt"] = payload["syncedAt"]       # keep the timestamp readable

    with open(OUT, "w") as f:
        json.dump(doc, f, separators=(",", ":"))
    print("wrote %s (%s)" % (OUT, "encrypted" if passphrase else "plain"))
    if errors:
        print("warnings: " + "; ".join(errors))
    return 0


if __name__ == "__main__":
    sys.exit(main())
