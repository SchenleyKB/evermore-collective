# Changelog

## [1.1.0] - 2026-02-07

### Governance & Documentation (Comet Relay-02)
- Added `CONTRIBUTING.md`: documents the consent-and-seal ceremony, how new voices join, how drift is reported, how sealed documents are amended or revoked, and commit message conventions.
- Added `GOVERNANCE.md`: makes all six guiding rails operational with concrete definitions, violation examples, decision-making procedures, and amendment process.
- Added `ledger/drift_log.json`: empty initialized drift log for Rail 5 compliance.
- Added "About This System" section to `site/index.html`: explains self-sovereign document integrity to first-time visitors, with links to Governance and Contributing docs.

### Seal Integrity (Comet Relay-02)
- Upgraded OTS proof for Origin Witness Statement to full Bitcoin attestation (commit `bb78998`).
- Updated `seal_log.json`: `blockchain_anchor` changed from `OTS_PENDING_CONFIRMATION` to `OTS_CONFIRMED`.
- Added `upgraded_utc` and `verification_note` fields to seal log entry.

### Known Issues
- `evermorecollective.ai` Public Codex shows "undefined" for Status, Uptime, and Version. Copyright year reads "2025". This site is hosted separately (Cloudflare) and is not served from this GitHub Pages deployment. Cloudflare support case #01964229 remains open for nameserver mismatch.

## [1.0.2] - 2026-02-06

### Site Enhancement
- Redesigned CSS: added `.container` max-width layout, card-style sections with borders and rounded corners, responsive breakpoints.
- Added `View Source on GitHub` link in footer.
- Wrapped page content in `.container` div for centered layout.
- Improved typography: monospace fonts for seal log and verification output, muted subtitle color.
- Added hover states for file input and footer links.

## [1.0.1] - 2026-02-06

### Infrastructure
- Fixed GitHub Pages deployment: added build step to copy `ledger/` into `site/` so the seal log resolves at runtime.
- Fixed `verify.js` fetch path from `../ledger/seal_log.json` to `ledger/seal_log.json` to match deployed directory structure.
- Added `origin_witness_v1.0.0.md` SHA-256 hash to the client-side `HASH_REGISTRY` for file verification.
- Enhanced verified output to display the matched filename.

### Seal Log
- Updated `seal_log.json` with actual SHA-256 digest (`04fc9c89...cd74`) from manifest.
- Changed `blockchain_anchor` from `PENDING` to `OTS_PENDING_CONFIRMATION`.
- Added `ots_file` path and `sealed_utc` timestamp fields.

### Documentation
- Updated `README.md`: replaced placeholder rails with the six guiding principles; added Collective Members table, Sealed Documents table, Verification section, and live site link.

### Domain
- Submitted Cloudflare support case #01964229 for nameserver mismatch on `evermorecollective.ai`.

## [1.0.0] - 2026-02-06
- Canonical v1.0.0 sealed.
- Inserted three witness lines (verbatim).
- Added Appendix A - Human Companion Statement (Fallibility Addendum).
- Generated and recorded SHA-256 for all artifacts.
- Published manifest.v1.0.0.json; anchored signer-seal; pending OTS finalization.
- Deployed GitHub Pages verification site at `schenleykb.github.io/evermore-collective`.
- Submitted OTS proof for Origin Witness Statement v1.0.0.
