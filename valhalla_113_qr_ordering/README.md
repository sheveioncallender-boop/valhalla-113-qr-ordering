# Valhalla 113 QR Table Ordering — Odoo 19

A GitHub-ready custom addon for Valhalla 113 Bar & Grill. It extends Odoo's native Restaurant POS and POS Self Order modules rather than replacing them.

## What it does

- Uses Odoo's native restaurant floors and tables.
- Generates a secure, table-specific self-order URL and branded printable QR card for every selected table.
- Opens Odoo's native mobile self-order menu when a guest scans the QR code.
- Forces mobile self-orders to carry both `self_ordering_table_id` and `table_id`, so the order appears on the correct POS floor-plan table.
- Keeps the order available for cashier/server payment in the native POS workflow.
- Adds 4-up A4 and single-card print layouts.
- Adds QR enable/disable, custom printed labels, print count and last-printed tracking per table.
- Applies the official Valhalla 113 logo and a dark metallic/red self-order visual layer.
- Includes a branded portrait landing image and a defensive mobile fallback so a fresh phone never receives a blank landing page.

## Required Odoo apps

- Point of Sale
- Restaurant
- POS Self Order

Target: Odoo 19 Community or Enterprise where the above native addons are available. Native payment-provider capabilities still depend on the Odoo edition and the payment integrations installed.

## Installation on Cloudpepper

1. Keep the `valhalla_113_qr_ordering` folder at the top level of your custom-addons GitHub repository.
2. Push the repository to GitHub and let Cloudpepper deploy/synchronize it.
3. Restart Odoo if required by the deployment configuration.
4. Enable developer mode and select **Apps → Update Apps List**.
5. Search for **Valhalla 113 QR Table Ordering** and install it.
6. Close any open restaurant POS session before changing self-order settings.

## Initial setup

1. Open **Point of Sale → Configuration → Point of Sales**.
2. Open the Valhalla restaurant POS configuration.
3. Open the **Valhalla QR Ordering** tab.
4. Click **Apply Valhalla QR Setup**.
5. Confirm that the restaurant floor(s) and table(s) are assigned to this POS.
6. Click **Print Table QR Cards**.
7. Select the floors/tables and the print layout.
8. Generate the PDF and print the cards.
9. Open the restaurant POS session.
10. Scan a printed code, place a test order, and confirm that it appears on the matching table.

## Operating flow

Guest scans table QR → native mobile menu opens → guest submits order → order enters the open POS session on the matching table → kitchen/bar preparation flow receives the order according to native printer/preparation configuration → staff opens the table and collects payment.

## Important operational notes

- The restaurant POS session must be open for guests to submit orders.
- Products must be available in POS/self-order and have the intended categories, prices, taxes and variants configured.
- QR URLs include Odoo's POS access token and the native random table identifier. Do not manually edit printed URLs.
- Regenerating the POS access token or table identifier invalidates older printed codes; reprint them afterward.
- Test the complete flow on a staging database before using it in live service.

## Version

`19.0.1.0.1`


## Mobile blank-screen repair

Version `19.0.1.0.1` repairs configurations made with the first release. After upgrading, refresh the QR link on the phone. If the old page is cached, open the **Valhalla QR Ordering** tab and click **Repair Mobile Landing Screen**, then reload Safari. The table QR URL itself does not need to change.
