import frappe
from frappe import _


# ─── Feature flag ────────────────────────────────────────────────────────────
# Toggle the whole feature. The flag is toggled from the Customer list page
# menu (Administrator only) and persisted as a global default in the DB. As a
# fallback, it can also be set in site_config.json:
#
#     "customer_name_validation_enabled": 0   # disable everything
#
# Resolution order: DB default → site_config.json → True (default)
_FLAG_KEY = "customer_name_validation_enabled"


def _is_enabled():
    db_val = frappe.db.get_default(_FLAG_KEY)
    if db_val is not None and str(db_val) != "":
        return str(db_val).strip() not in ("0", "false", "False", "no", "No")
    return bool(frappe.local.conf.get(_FLAG_KEY, 1))


def boot_customer_name_validation(bootinfo):
    """Expose the feature flag to client-side JS via frappe.boot."""
    bootinfo[_FLAG_KEY] = _is_enabled()


@frappe.whitelist()
def get_customer_name_validation_status():
    return {"enabled": _is_enabled()}


@frappe.whitelist()
def set_customer_name_validation_status(enabled):
    # Administrator only — not even other System Managers can toggle.
    if (frappe.session.user or "").lower() != "administrator":
        frappe.throw(
            _("Only the Administrator can change this setting."),
            frappe.PermissionError,
        )
    val = "1" if str(enabled).strip() in ("1", "true", "True", "yes", "Yes") else "0"
    frappe.db.set_default(_FLAG_KEY, val)

    # Clear the bootinfo cache for ALL users so any manual refresh fetches
    # fresh boot data (Frappe caches frappe.boot per-user in Redis).
    try:
        frappe.cache.delete_keys("bootinfo")
    except Exception:
        frappe.clear_cache()

    # Broadcast to every connected desk session so all browsers update at once
    # without needing each user to hard-refresh.
    frappe.publish_realtime(
        event="customer_name_validation_flag_changed",
        message={"enabled": val == "1"},
        after_commit=True,
    )
    return {"enabled": val == "1"}


# ─── Validation ──────────────────────────────────────────────────────────────
# A valid Customer name:
#   - starts with a letter (any Unicode script: Latin, Arabic, etc.);
#   - contains only letters and spaces between words;
#   - has no digits, no special characters, and no leading/trailing whitespace.
_ALLOWED_SEPARATORS = frozenset({" "})


# Every rejection raises the exact same message, by request.
_ERROR_MESSAGE = "customer name accepts letters only"


def _validate_name(name):
    if not name:
        # Required-ness is ERPNext's own concern; we only validate content.
        return

    # Leading/trailing space, must-start-with-letter, and any invalid character
    # all raise the same single message.
    if name != name.strip():
        frappe.throw(_(_ERROR_MESSAGE), frappe.ValidationError)

    if not name[0].isalpha():
        frappe.throw(_(_ERROR_MESSAGE), frappe.ValidationError)

    for ch in name:
        if ch.isalpha() or ch in _ALLOWED_SEPARATORS:
            continue
        frappe.throw(_(_ERROR_MESSAGE), frappe.ValidationError)


def validate_customer_name(doc, method):
    if not _is_enabled():
        return
    # Pass the raw value (not stripped) so leading/trailing spaces are caught.
    _validate_name(doc.get("customer_name"))
