def post_init_hook(env):
    """Enable Valhalla QR printing on restaurant tables that predate the addon."""
    env["restaurant.table"].search([]).write({"valhalla_qr_enabled": True})
