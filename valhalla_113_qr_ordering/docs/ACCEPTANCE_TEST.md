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
