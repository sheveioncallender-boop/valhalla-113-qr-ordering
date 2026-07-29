# Cloudpepper Deployment

## Repository layout

Place the addon folder directly inside the GitHub repository that Cloudpepper uses for custom addons:

```text
repository-root/
└── valhalla_113_qr_ordering/
    ├── __manifest__.py
    ├── models/
    ├── views/
    └── ...
```

Do not add another wrapper folder between the repository root and `valhalla_113_qr_ordering` unless that wrapper is already configured as an Odoo addons path.

## Deployment sequence

1. Commit and push the complete addon folder to GitHub.
2. Synchronize or redeploy the connected Cloudpepper branch.
3. Restart the Odoo service when the deployment requires it.
4. Enable developer mode.
5. Open **Apps** and run **Update Apps List**.
6. Search for **Valhalla 113 QR Table Ordering**.
7. Install the addon.
8. Open the target POS configuration and use the **Valhalla QR Ordering** tab.

## Upgrade sequence

For later versions, replace the module files in GitHub, deploy, restart Odoo if needed, and select **Upgrade** on the installed app. Never rename the technical folder after installation.

## Required native addons

- `point_of_sale`
- `pos_restaurant`
- `pos_self_order`

The custom addon declares these dependencies, so Odoo will require them during installation.
