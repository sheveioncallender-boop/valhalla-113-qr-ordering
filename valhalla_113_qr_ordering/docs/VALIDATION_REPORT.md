# Validation Report — 19.0.1.0.0

## Completed before packaging

- Python source compiled successfully.
- All addon XML files parsed successfully.
- The Odoo manifest parsed and all declared data/assets were present.
- Security access CSV parsed and permission values were valid.
- All supplied/generated PNG assets passed image integrity and dimension checks.
- XML identifiers were checked for duplicates inside the addon.
- The post-install hook was registered and exported correctly.
- Placeholder and accidental secret-marker scans returned no findings.
- The implementation contracts were compared with Odoo 19's native `pos_restaurant` and `pos_self_order` field/method names, report route, asset bundle and table-specific URL flow.

## Deployment boundary

This package has not been installed into the customer's live Cloudpepper database from the build environment. Install it on a staging database first and complete `docs/ACCEPTANCE_TEST.md` before live restaurant use.
