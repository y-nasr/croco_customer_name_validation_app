# Changelog

All notable changes to **Customer Name Validation** are documented here.
This project loosely follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — Initial release

### Added

- **Server-side validation** of `Customer.customer_name` on every save
  (add and edit), covering both the quick-entry dialog and the full form.
  A valid name starts with a letter (any Unicode script) and contains only
  letters and spaces between words — no digits, no special characters, and
  no leading/trailing spaces.
- **Client-side full-form validator** that mirrors the server rule for
  instant feedback before the round-trip.
- **Administrator-only feature flag** with a real-time toggle in the
  Customer list-page menu. Flipping the flag propagates to every connected
  desk session via Socket.IO — no per-browser refresh required.
- **Asset cache-busting** via `_v()` in `hooks.py`.

### Notes

- Standalone app — depends only on Frappe ≥ 15 and ERPNext ≥ 15. No custom
  fields, no external Python packages.

[0.1.0]: https://github.com/CrocoIT/customer_name_validation/releases/tag/v0.1.0
