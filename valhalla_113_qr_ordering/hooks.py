def post_init_hook(env):
    """Repair only explicitly branded POS configurations; preserve native setup."""
    env["pos.config"]._valhalla_repair_existing_self_order_configs()
