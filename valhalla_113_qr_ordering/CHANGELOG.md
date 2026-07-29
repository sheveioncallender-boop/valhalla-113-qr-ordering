# Changelog

## 19.0.1.0.2

- Fixed the self-order asset bundle compilation error shown as “A css error occurred, using an old style to render this page”.
- Replaced the custom SCSS asset with plain CSS so Cloudpepper does not parse browser `min()`, `max()`, `clamp()` or safe-area functions as Sass.
- Removed the unnecessary OWL landing-page template override; the module now relies on Odoo’s native landing page with the attached Valhalla image.
- Kept the mobile landing repair and existing QR/table identifiers unchanged.

## 19.0.1.0.1

- Fixed the blank self-order landing screen seen on fresh mobile browsers.
- Automatically attaches a public Valhalla portrait landing image to existing self-order POS configurations during upgrade.
- Added a defensive OWL landing-page fallback so the menu never opens to an empty page even if splash attachments are removed.
- Added **Repair Mobile Landing Screen** and exposed native home images in the Valhalla configuration tab.
- Added iPhone safe-area and small-screen styling.

## 19.0.1.0.0 — Initial release

- Added Valhalla-branded QR cards for restaurant tables.
- Added batch floor/table selection with 4-up and single-card PDF layouts.
- Added table-level QR enablement, custom labels and print tracking.
- Added one-click configuration for native mobile table self-ordering.
- Ensured mobile self-orders carry both the native self-order table reference and the restaurant floor-plan `table_id`.
- Added a dark metallic/red visual layer for the native self-ordering interface.
- Added installation initialization so pre-existing restaurant tables are QR-enabled.
- Added a safe POS-user fallback for native self-order access on older POS configurations.