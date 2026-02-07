#!/usr/bin/env python3

"""
Verify the integrity of files recorded in the hash registry.

This script reads `../ledger/hash_registry.json`, recalculates the SHA‑256
digest of each recorded file, and compares it to the stored hash. For each
entry it reports PASS or FAIL. At the end it prints a summary of how many
files passed verification. The script exits with code 0 if all files pass
and 1 if any fail.

Usage:
    python verify_integrity.py

Only standard library modules are used.
"""

import sys
import os
import json
import hashlib


def compute_sha256(filepath: str) -> str:
    """Return the SHA‑256 digest of the file at `filepath`."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    registry_path = os.path.normpath(os.path.join(script_dir, "..", "ledger", "hash_registry.json"))

    # Load registry
    try:
        with open(registry_path, "r") as f:
            content = f.read().strip()
            registry = json.loads(content) if content else []
    except (FileNotFoundError, json.JSONDecodeError):
        print("No valid hash registry found.")
        sys.exit(1)

    total = len(registry)
    passed = 0
    failures = []

    for entry in registry:
        filepath = entry.get("filename")
        expected_hash = entry.get("hash")

        # Resolve relative paths relative to repository root
        if os.path.isabs(filepath):
            abs_path = filepath
        else:
            abs_path = os.path.normpath(os.path.join(script_dir, "..", filepath))

        if not os.path.isfile(abs_path):
            print(f"{filepath}: FAIL (missing)")
            failures.append(filepath)
            continue

        actual_hash = compute_sha256(abs_path)
        if actual_hash == expected_hash:
            print(f"{filepath}: PASS")
            passed += 1
        else:
            print(f"{filepath}: FAIL")
            failures.append(filepath)

    # Summary
    print(f"{passed} of {total} files verified.")
    if failures:
        print("Failures: " + ", ".join(failures))
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()