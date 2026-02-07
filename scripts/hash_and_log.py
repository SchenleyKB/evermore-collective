#!/usr/bin/env python3

"""
Compute the SHA‑256 hash of a file and log it to the hash registry.

This script accepts a single file path as an argument, calculates the file’s
SHA‑256 digest, records metadata about the file in the hash registry, and
prints the resulting hash to stdout. The hash registry is stored as JSON in
`../ledger/hash_registry.json` relative to this script’s location.

Usage:
    python hash_and_log.py <file_path>

The registry entry includes the filename (as provided), the hash, a UTC
timestamp, and the file size in bytes. Only standard library modules are
used.
"""

import sys
import os
import json
import hashlib
from datetime import datetime


def compute_sha256(filepath: str) -> str:
    """Return the SHA‑256 digest of the file at `filepath`."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def load_registry(registry_path: str):
    """Load the existing hash registry, returning a list."""
    try:
        with open(registry_path, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_registry(registry_path: str, registry: list) -> None:
    """Write the registry list back to disk with pretty formatting."""
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)


def main():
    # Ensure a file path is provided
    if len(sys.argv) < 2:
        print("Usage: hash_and_log.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Verify the file exists and is not a directory
    if not os.path.isfile(file_path):
        print(f"Error: {file_path} not found or not a file")
        sys.exit(1)

    # Compute the SHA‑256 digest
    digest = compute_sha256(file_path)
    size_bytes = os.path.getsize(file_path)
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Determine the registry path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    registry_path = os.path.normpath(os.path.join(script_dir, "..", "ledger", "hash_registry.json"))

    # Load existing registry, append new entry, and save
    registry = load_registry(registry_path)
    registry.append({
        "filename": file_path,
        "hash": digest,
        "timestamp": timestamp,
        "size_bytes": size_bytes
    })
    save_registry(registry_path, registry)

    # Output the computed hash
    print(digest)


if __name__ == "__main__":
    main()