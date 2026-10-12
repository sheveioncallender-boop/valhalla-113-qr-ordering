# Validation report — 19.0.1.1.0

Source checks passed for the website and QR companion release:

- 16 Python files parsed, 11 XML files parsed; server data XML validated against Odoo's `import_xml.rng`.
- Three loaded CSS files parsed without errors; all manifest data/assets and referenced local images exist.
- 26 server QWeb expressions parsed; website/footer inheritance targets and native website/POS helper methods checked against official Odoo 19 source commit `74c927424f7da4b9ec9713e10749de93ec0dcf46`.
- Existing website code that suppressed the native header and custom navigation JavaScript removed.
- Four isolated checks executed the actual QR action bodies with environment adapters: branding writes only image/name fields; non-managers are denied; active sessions block initial setup; repair searches only explicitly branded Valhalla configurations.
- Git whitespace checks passed.

These are source and isolated behavior checks, **not a live Odoo integration test**. A running Odoo/PostgreSQL instance was unavailable. Fresh installation, compiled QWeb/assets, browser rendering, payment/checkout, email and POS/table/kitchen behavior must be checked on the deployed database using `ACCEPTANCE_TEST.md`.
