app_name = "customer_name_validation"
app_title = "Customer Name Validation"
app_publisher = "Croco IT"
app_description = "Enforces that Customer names contain only letters (any script) plus spaces, hyphens, apostrophes and periods — no digits, no leading spaces, no other symbols."
app_email = "info@crocoit.com"
app_license = "MIT"

# Marketplace metadata — used by Frappe Cloud's marketplace listing and by
# the desk's "About this App" dialog.
app_logo_url = "/assets/customer_name_validation/images/logo.png"
source_link = "https://github.com/CrocoIT/customer_name_validation"
app_license_link = "https://github.com/CrocoIT/customer_name_validation/blob/main/license.txt"
website_url = "https://crocoit.com"
documentation_url = "https://github.com/CrocoIT/customer_name_validation#readme"
support_url = "mailto:info@crocoit.com"


# ── Asset cache-busting ──────────────────────────────────────────────────────
# nginx serves /assets/<app>/js/*.js with `Cache-Control: max-age=1y`, so
# browsers hold the old file forever. Append a query string based on the
# file's mtime — when we edit the file and `bench restart` runs, hooks.py is
# re-imported, the new mtime is picked up, the URL changes, and every browser
# re-fetches the file automatically.
import os as _os
_PUBLIC = _os.path.join(_os.path.dirname(__file__), "public")
def _v(rel):
    try:
        return f"/assets/customer_name_validation/{rel}?v={int(_os.path.getmtime(_os.path.join(_PUBLIC, rel)))}"
    except OSError:
        return f"/assets/customer_name_validation/{rel}"


app_include_js = [
    _v("js/customer_name_flag_listener.js"),
]

doctype_js = {
    "Customer": "public/js/customer.js",
}

doctype_list_js = {
    "Customer": "public/js/customer_list.js",
}

doc_events = {
    "Customer": {
        "validate": "customer_name_validation.customer.validate_customer_name",
    },
}

# Expose the feature flag to the desk so JS can gate its logic.
boot_session = "customer_name_validation.customer.boot_customer_name_validation"
