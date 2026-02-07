#!/usr/bin/env python3

"""
Anchor a file’s hash to the blockchain using OpenTimestamps.

This script computes the SHA‑256 hash of a given file, ensures that the
OpenTimestamps client is installed, and then stamps the file with
`ots stamp`. The resulting `.ots` proof is moved to
`../proofs/ots/`. After stamping, the script updates the most recent
entry in `../ledger/seal_log.json` to indicate that a blockchain anchor
has been submitted, recording the timestamp of submission. Finally, it
prints the computed hash and instructions on how to upgrade the proof.

Usage:
    python anchor_to_blockchain.py <file_path>

Only standard library modules are used, aside from invoking `pip` to
install `opentimestamps-client` if necessary. The script relies on the
`ots` command being available after installation.
"""

import sys
import os
import json
import hashlib
import subprocess
import shutil
from datetime import datetime
from importlib.util import find_spec


def compute_sha256(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def ensure_opentimestamps_installed() -> None:
    """Ensure the OpenTimestamps client is installed. Installs it via pip if absent."""
    if find_spec("opentimestamps") is None:
        # Install opentimestamps-client using pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", "opentimestamps-client"], check=True)


def stamp_file(filepath: str) -> str:
    """Stamp the file with ots and return the generated .ots file path."""
    # Run ots stamp
    subprocess.run(["ots", "stamp", filepath], check=True)
    ots_path = filepath + ".ots"
    return ots_path


def update_seal_log(seal_log_path: str) -> None:
    """Update the last seal log entry to mark the blockchain anchor submission."""
    try:
        with open(seal_log_path, "r") as f:
            content = f.read().strip()
            log = json.loads(content) if content else []
    except (FileNotFoundError, json.JSONDecodeError):
        log = []

    if log:
        timestamp = datetime.utcnow().isoformat() + "Z"
        # Update the last entry
        log[-1]["blockchain_anchor"] = "OTS_SUBMITTED"
        log[-1]["anchor_timestamp"] = timestamp
        with open(seal_log_path, "w") as f:
            json.dump(log, f, indent=2)


def main():
    if len(sys.argv) < 2:
        print("Usage: anchor_to_blockchain.py <file_path>")
        sys.exit(1)

    target_path = sys.argv[1]
    if not os.path.isfile(target_path):
        print(f"Error: {target_path} not found or not a file")
        sys.exit(1)

    # Compute hash
    digest = compute_sha256(target_path)

    # Ensure OpenTimestamps is available
    try:
        ensure_opentimestamps_installed()
    except subprocess.CalledProcessError as e:
        print("Failed to install opentimestamps-client.")
        print(e)
        sys.exit(1)

    # Stamp the file
    try:
        ots_path = stamp_file(target_path)
    except subprocess.CalledProcessError as e:
        print("Failed to stamp file with ots.")
        print(e)
        sys.exit(1)

    # Move the proof to proofs/ots directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.normpath(os.path.join(script_dir, "..", "proofs", "ots"))
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, os.path.basename(ots_path))
    try:
        if os.path.exists(dest_path):
            os.remove(dest_path)
        shutil.move(ots_path, dest_path)
    except Exception as e:
        print("Error moving OTS file:", e)

    # Update the seal log
    seal_log_path = os.path.normpath(os.path.join(script_dir, "..", "ledger", "seal_log.json"))
    update_seal_log(seal_log_path)

    # Print summary and instructions
    print(f"Hash: {digest}")
    print(f"Proof saved to {dest_path}")
    print(f"To upgrade proof later, run: ots upgrade \"{dest_path}\"")


if __name__ == "__main__":
    main()