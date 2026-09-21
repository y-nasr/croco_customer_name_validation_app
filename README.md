# Customer Name Validation

Frappe / ERPNext app that enforces clean, consistent **Customer names**.

A valid customer name:

- **Starts with a letter** — any Unicode script (Latin, Arabic, etc.). No
  leading space, digit, or symbol.
- Contains **only letters and these separators**: space, hyphen `-`,
  apostrophe `'` (straight or curly `’`), and period `.`
- Has **no digits**, **no other symbols**, and **no leading/trailing spaces**.

Examples:

| Input | Result |
|---|---|
| `Mohamed Osama` | ✅ |
| `محمد اسامة` | ✅ (Arabic letters + space) |
| `Al-Sayed` | ✅ (hyphen) |
| `O'Brien` | ✅ (apostrophe) |
| `St. John` | ✅ (period) |
| ` Mohamed` | ❌ leading space |
| `Ahmed123` | ❌ digit |
| `Ahmed*` | ❌ symbol |
| `123 Trading` | ❌ starts with a digit |

## Enforcement

- **Server-side** `Customer.validate` hook — blocks the save on both the
  quick-entry dialog and the full form, on **add and edit**.
- **Client-side** full-form validator mirrors the rule for instant feedback
  (the server hook is the real enforcement).
- Everything is gated behind a single **feature flag** the Administrator can
  toggle from the Customer list-page menu; the change propagates to every
  connected desk session in real time.

## Install

```bash
bench get-app https://github.com/CrocoIT/customer_name_validation
bench --site <site> install-app customer_name_validation
bench build --app customer_name_validation
bench restart
```

No custom fields or external Python dependencies are required.

## Toggle

Customer list page (`/app/customer`) → ⋮ menu → **"Customer Name Validation:
ON / OFF"** (Administrator only). Or set in `site_config.json`:

```json
{ "customer_name_validation_enabled": 0 }
```

## License

MIT — see [`license.txt`](./license.txt).
