#!/usr/bin/env python3

"""
Generate a changelog entry for the Evermore ledger.

This script accepts four arguments: a version number, an action keyword
(e.g. SEAL, DRAFT, AMEND, or REVOKE), an artifact filename, and a
description. It appends an entry with these details and a UTC timestamp
to `../ledger/changelog.json`, creating the file if necessary. The
timestamp is in ISO 8601 UTC format.

Usage:
    python generate_changelog_entry.py <version> <action> <artifact> <description>

Example:
    python generate_changelog_entry.py 1.0.1 AMEND "origin.txt" "Fixed typos"

Only standard library modules are used.
"""

import sys
import os
import json
from datetime import datetime


def main():
    if len(sys.argv) < 5:
        print("Usage: generate_changelog_entry.py <version> <action> <artifact_filename> <description>")
        sys.exit(1)

    version = sys.argv[1]
    action = sys.argv[2]
    artifact = sys.argv[3]
    description = " ".join(sys.argv[4:])
    timestamp = datetime.utcnow().isoformat() + "Z"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    changelog_path = os.path.normpath(os.path.join(script_dir, "..", "ledger", "changelog.json"))

    # Load existing changelog
    try:
        with open(changelog_path, "r") as f:
            content = f.read().strip()
            changelog = json.loads(content) if content else []
    except (FileNotFoundError, json.JSONDecodeError):
        changelog = []

    entry = {
        "version": version,
        "action": action,
        "artifact": artifact,
        "description": description,
        "timestamp": timestamp
    }
    changelog.append(entry)

    # Write back
    with open(changelog_path, "w") as f:
        json.dump(changelog, f, indent=2)

    print(f"Added changelog entry for {artifact} ({version})")


if __name__ == "__main__":
    main()