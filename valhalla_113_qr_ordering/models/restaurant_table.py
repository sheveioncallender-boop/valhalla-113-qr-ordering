from odoo import fields, models, _
from odoo.exceptions import UserError


class RestaurantTable(models.Model):
    _inherit = "restaurant.table"

    valhalla_qr_enabled = fields.Boolean(
        string="Use Valhalla QR Ordering",
        default=True,
        help="Include this table when generating Valhalla self-order QR cards.",
    )
    valhalla_qr_label = fields.Char(
        string="Printed Table Label",
        help="Optional label printed instead of the numeric table number.",
    )
    valhalla_qr_print_count = fields.Integer(
        string="QR Print Count",
        readonly=True,
        copy=False,
    )
    valhalla_qr_last_printed_at = fields.Datetime(
        string="Last QR Print",
        readonly=True,
        copy=False,
    )

    def action_open_valhalla_qr_wizard(self):
        self.ensure_one()
        configs = self.floor_id.pos_config_ids.filtered(
            lambda config: config.module_pos_restaurant
        )
        if not configs:
            raise UserError(
                _(
                    "This table's floor is not assigned to a Restaurant Point of Sale."
                )
            )
        return {
            "name": _("Print Valhalla Table QR Card"),
            "type": "ir.actions.act_window",
            "res_model": "valhalla.qr.print.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_pos_config_id": configs[0].id,
                "default_floor_ids": [(6, 0, self.floor_id.ids)],
                "default_table_ids": [(6, 0, self.ids)],
                "valhalla_preserve_table_selection": True,
            },
        }
