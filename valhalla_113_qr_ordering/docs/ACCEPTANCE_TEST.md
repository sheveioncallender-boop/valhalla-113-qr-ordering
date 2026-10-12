# Acceptance Test Checklist

Perform this test on a staging database before live restaurant service.

## Configuration

- [ ] The addon installs without an RPC error.
- [ ] The target POS has at least one assigned floor and two active tables.
- [ ] **Apply Valhalla QR Setup** sets Self Ordering to **QR menu + Ordering**, service to **Table**, and payment timing to **Meal**.
- [ ] The official Valhalla brand image appears in the self-order configuration.
- [ ] The restaurant POS session opens successfully.

## QR cards

- [ ] The print wizard lists only floors assigned to the selected POS.
- [ ] Disabled QR tables are excluded.
- [ ] Four-up A4 PDF output renders correctly.
- [ ] Single-card PDF output renders correctly.
- [ ] Each selected table has a different scannable QR code.
- [ ] Print count and last-print date update on each table.

## Guest order flow

- [ ] Scan Table 1 and confirm the mobile menu opens.
- [ ] Add at least one food item and one drink.
- [ ] Add a customer note or product note where configured.
- [ ] Submit the order.
- [ ] Confirm the order appears in the open POS session.
- [ ] Confirm it appears on Table 1, not another table.
- [ ] Confirm the backend order shows **Valhalla QR Table Order**.
- [ ] Confirm kitchen/bar preparation routing behaves according to native printer or preparation-display settings.
- [ ] Open Table 1 in POS and complete payment.

## Negative tests

- [ ] Scan a code while the POS session is closed and confirm Odoo blocks order submission appropriately.
- [ ] Disable a table, regenerate cards, and confirm it is excluded.
- [ ] Attempt setup while a POS session is active and confirm the addon prevents unsafe configuration changes.


## Website companion regression

1. Install both addons fresh on Odoo 19; confirm either install order succeeds.
2. Confirm website root opens Valhalla; native header, mobile menu, cart, login, and all added pages render.
3. Publish one product, enable POS/self-order availability, and configure the relevant categories. Check that the same record appears in the online shop and native QR menu.
4. Choose variants, add to the website cart, check tax/pricelist totals and complete a test checkout. Confirm one native Sales order and the correct payment state.
5. Scan an actual table QR and submit a separate order. Confirm the correct POS session/table and preparation routing. Confirm website checkout did not create an extra POS order.
6. Record the POS payment/service settings, table identifiers, token and custom landing image; click Apply Branding Only. Verify all recorded values remain unchanged.
7. Upgrade both addons twice. Verify no duplicate menus/products/QR cards and preserved website logo, new page edits and POS configuration.
8. Test mobile menu, cart icon, disabled payment buttons and QR pages on desktop/mobile. Check readability on all native forms/dialogs.
