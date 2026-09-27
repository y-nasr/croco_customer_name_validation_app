// Full-form client-side validation for Customer Name — mirrors the server
// rule in customer.py so the user gets instant feedback and the save is
// blocked before a round-trip. The server hook is the real enforcement;
// this is UX only. Both are gated by the same feature flag.

function customer_name_validation_enabled() {
	return !(frappe.boot && frappe.boot.customer_name_validation_enabled === false);
}

// A valid name: starts with a Unicode letter, then only letters and spaces
// between words. No digits, no special characters, no leading/trailing space.
var CMV_NAME_RE = /^\p{L}[\p{L} ]*$/u;

// Every rejection returns the exact same message, by request.
var CMV_ERROR_MESSAGE = "customer name accepts letters only";

function _cmv_name_error(name) {
	if (!name) return null; // required-ness is ERPNext's concern
	if (name !== name.trim() || !/^\p{L}/u.test(name) || !CMV_NAME_RE.test(name)) {
		return __(CMV_ERROR_MESSAGE);
	}
	return null;
}

frappe.ui.form.on("Customer", {
	validate: function (frm) {
		if (!customer_name_validation_enabled()) return;
		var err = _cmv_name_error(frm.doc.customer_name);
		if (err) {
			frappe.msgprint({ title: __("Invalid Customer Name"), message: err, indicator: "red" });
			frappe.validated = false;
		}
	},
});
