"""
Full-version entitlement: Act 1 is free, Acts 2-4 are the paid full version.

There is no store integration yet. The full version counts as unlocked when
  - data/full_version.json contains {"unlocked": true}  (per install), or
  - the environment variable PLATFORMER_FULL_VERSION=1 is set (development).

When publishing, replace full_version_unlocked() with the store's ownership
check (Steam, itch.io, ...); nothing else needs to change.
"""

import json
import os

FREE_ACTS = {1}
FULL_VERSION_FILE = os.path.join("data", "full_version.json")


def full_version_unlocked():
    """True if this install owns the full version (Acts 2-4)"""
    if os.environ.get("PLATFORMER_FULL_VERSION") == "1":
        return True
    try:
        with open(FULL_VERSION_FILE, "r", encoding="utf-8") as f:
            return bool(json.load(f).get("unlocked"))
    except (OSError, ValueError, AttributeError):
        return False


def act_available(act_number):
    """Can this act be played on this install?"""
    return act_number in FREE_ACTS or full_version_unlocked()


def unlock_full_version():
    """Mark this install as owning the full version (store callback / dev use)"""
    os.makedirs(os.path.dirname(FULL_VERSION_FILE), exist_ok=True)
    with open(FULL_VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump({"unlocked": True}, f)
