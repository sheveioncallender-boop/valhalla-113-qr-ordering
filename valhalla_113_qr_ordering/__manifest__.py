{
    "name": "Valhalla 113 QR Table Ordering",
    "summary": "Branded QR table cards and table-linked restaurant self-ordering",
    "version": "19.0.1.0.1",
    "category": "Sales/Point of Sale",
    "author": "SPXCORP Limited",
    "license": "LGPL-3",
    "depends": [
        "point_of_sale",
        "pos_restaurant",
        "pos_self_order",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/pos_config_views.xml",
        "views/restaurant_table_views.xml",
        "views/pos_order_views.xml",
        "views/qr_print_wizard_views.xml",
        "reports/qr_card_report.xml",
        "data/repair_existing_configs.xml",
    ],
    "assets": {
        "pos_self_order.assets": [
            "valhalla_113_qr_ordering/static/src/xml/landing_page_fallback.xml",
            "valhalla_113_qr_ordering/static/src/scss/self_order_branding.scss",
        ],
    },
    "images": [
        "static/description/banner.png",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "post_init_hook": "post_init_hook",
}
