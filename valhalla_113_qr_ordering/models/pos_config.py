import base64

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import file_open


class PosConfig(models.Model):
    _inherit = "pos.config"

    valhalla_qr_heading = fields.Char(
        string="QR Card Heading",
        default="SCAN • ORDER • ENJOY",
        translate=True,
    )
    valhalla_qr_instruction = fields.Char(
        string="QR Card Instruction",
        default="Scan the code to view the menu and place your order.",
        translate=True,
    )
    valhalla_qr_footer = fields.Char(
        string="QR Card Footer",
        default="Your order goes directly to the Valhalla 113 team.",
        translate=True,
    )
    valhalla_qr_show_url = fields.Boolean(
        string="Show URL on Printed Cards",
        default=False,
        help="Print the self-order URL beneath each QR code for troubleshooting.",
    )

    @api.model
    def _valhalla_brand_binary(self):
        """Return the web-optimized official brand image for an Odoo Image field."""
        with file_open(
            "valhalla_113_qr_ordering/static/src/img/valhalla_self_order_brand.png",
            "rb",
        ) as brand_file:
            return base64.b64encode(brand_file.read())

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("module_pos_restaurant") and not vals.get(
                "self_ordering_image_brand"
            ):
                vals.setdefault(
                    "self_ordering_image_brand", self._valhalla_brand_binary()
                )
                vals.setdefault(
                    "self_ordering_image_brand_name", "Valhalla 113 Bar & Grill"
                )
        return super().create(vals_list)

    def action_apply_valhalla_qr_setup(self):
        """Configure Odoo's native mobile self-ordering for table service."""
        self.ensure_one()
        if not self.env.user.has_group("point_of_sale.group_pos_manager"):
            raise UserError(_("Only a Point of Sale manager can change this setup."))
        if self.has_active_session:
            raise UserError(
                _(
                    "Close the active Point of Sale session before changing the "
                    "restaurant self-ordering configuration."
                )
            )

        default_user = self.self_ordering_default_user_id
        if not default_user or not (
            default_user.sudo().has_group("point_of_sale.group_pos_user")
            or default_user.sudo().has_group("point_of_sale.group_pos_manager")
        ):
            # The setup action itself is manager-only, so the current user is a
            # dependable native self-order security user when an older POS config
            # does not yet have one assigned.
            default_user = self.env.user

        self.write(
            {
                "module_pos_restaurant": True,
                "self_ordering_mode": "mobile",
                "self_ordering_service_mode": "table",
                "self_ordering_pay_after": "meal",
                "self_ordering_default_user_id": default_user.id,
                "self_ordering_image_brand": self._valhalla_brand_binary(),
                "self_ordering_image_brand_name": "Valhalla 113 Bar & Grill",
            }
        )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Valhalla QR Ordering Ready"),
                "message": _(
                    "Mobile table ordering is enabled. Add floors and tables, print "
                    "the QR cards, then open the POS session."
                ),
                "type": "success",
                "sticky": False,
            },
        }

    def action_open_valhalla_qr_wizard(self):
        self.ensure_one()
        return {
            "name": _("Print Valhalla Table QR Cards"),
            "type": "ir.actions.act_window",
            "res_model": "valhalla.qr.print.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_pos_config_id": self.id,
            },
        }
