# Changelog

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
