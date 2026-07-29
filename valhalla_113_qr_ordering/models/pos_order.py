from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    valhalla_qr_order = fields.Boolean(
        string="Valhalla QR Table Order",
        readonly=True,
        copy=False,
        index=True,
        help="This order originated from a Valhalla table QR self-ordering link.",
    )

    @api.model
    def _check_pos_order(self, pos_config, order, device_type, table=None):
        """
        Keep Odoo's secure self-order validation and add the restaurant table_id.

        Native Odoo records self_ordering_table_id. Setting table_id as well makes the
        order immediately visible on the correct table in the restaurant floor screen
        and keeps subsequent table operations consistent.
        """
        safe_data = super()._check_pos_order(pos_config, order, device_type, table)
        if table and device_type == "mobile":
            safe_data.update(
                {
                    "table_id": table.id,
                    "self_ordering_table_id": table.id,
                    "valhalla_qr_order": True,
                }
            )
        return safe_data

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self_order_table_id = vals.get("self_ordering_table_id")
            if self_order_table_id and not vals.get("table_id"):
                vals["table_id"] = self_order_table_id
            if vals.get("source") == "mobile" and self_order_table_id:
                vals.setdefault("valhalla_qr_order", True)
        return super().create(vals_list)

    def write(self, vals):
        vals = dict(vals)
        if vals.get("self_ordering_table_id") and not vals.get("table_id"):
            vals["table_id"] = vals["self_ordering_table_id"]
        return super().write(vals)
