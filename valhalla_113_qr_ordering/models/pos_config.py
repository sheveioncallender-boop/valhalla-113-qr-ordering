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

    @api.model
    def _valhalla_mobile_landing_url(self):
        return (
            "/valhalla_113_qr_ordering/static/src/img/"
            "valhalla_mobile_landing.jpg"
        )

    def _get_or_create_valhalla_mobile_landing_attachment(self):
        """Create a public URL attachment usable by Odoo's native landing carousel."""
        self.ensure_one()
        attachment_model = self.env["ir.attachment"].sudo()
        landing_url = self._valhalla_mobile_landing_url()
        attachment = attachment_model.search(
            [
                ("res_model", "=", "pos.config"),
                ("res_id", "=", self.id),
                ("type", "=", "url"),
                ("url", "=", landing_url),
            ],
            limit=1,
        )
        if not attachment:
            attachment = attachment_model.create(
                {
                    "name": "Valhalla 113 Mobile Self-Order Landing",
                    "type": "url",
                    "url": landing_url,
                    "res_model": "pos.config",
                    "res_id": self.id,
                    "public": True,
                }
            )
        elif not attachment.public:
            attachment.write({"public": True})
        return attachment

    def _ensure_valhalla_mobile_landing(self):
        """Prevent a blank native landing page on fresh mobile browsers.

        Odoo 19's LandingPage only renders its main content when at least one
        ``self_ordering_image_home_ids`` attachment exists. Desktop browsers may
        appear to work because they retain a previously visited product route,
        while a new phone opens the empty landing route.
        """
        for config in self:
            if config.self_ordering_image_home_ids:
                config._ensure_public_attachments()
                config._prepare_self_order_custom_btn()
                continue
            attachment = config._get_or_create_valhalla_mobile_landing_attachment()
            config.sudo().write(
                {"self_ordering_image_home_ids": [(6, 0, attachment.ids)]}
            )
        return True

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
        configs = super().create(vals_list)
        configs.filtered(
            lambda config: config.self_ordering_mode not in (False, "nothing")
        )._ensure_valhalla_mobile_landing()
        return configs

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
            default_user = self.env.user

        landing_attachment = (
            self._get_or_create_valhalla_mobile_landing_attachment()
        )
        self.write(
            {
                "module_pos_restaurant": True,
                "self_ordering_mode": "mobile",
                "self_ordering_service_mode": "table",
                "self_ordering_pay_after": "meal",
                "self_ordering_default_user_id": default_user.id,
                "self_ordering_image_brand": self._valhalla_brand_binary(),
                "self_ordering_image_brand_name": "Valhalla 113 Bar & Grill",
                "self_ordering_image_home_ids": [
                    (6, 0, landing_attachment.ids)
                ],
            }
        )
        self._ensure_valhalla_mobile_landing()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Valhalla QR Ordering Ready"),
                "message": _(
                    "Mobile table ordering and the branded phone landing screen "
                    "are enabled. Refresh the QR page on the phone."
                ),
                "type": "success",
                "sticky": False,
            },
        }

    def action_repair_valhalla_mobile_landing(self):
        """Repair existing configurations without rebuilding floors or QR codes."""
        self.ensure_one()
        if not self.env.user.has_group("point_of_sale.group_pos_manager"):
            raise UserError(_("Only a Point of Sale manager can repair this setup."))
        self._ensure_valhalla_mobile_landing()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Mobile Landing Screen Repaired"),
                "message": _(
                    "A public Valhalla landing image and the native Order Now "
                    "link are now attached to this Point of Sale."
                ),
                "type": "success",
                "sticky": False,
            },
        }

    @api.model
    def _valhalla_repair_existing_self_order_configs(self):
        """Upgrade-time repair for configurations created by version 19.0.1.0.0."""
        configs = self.sudo().search(
            [("self_ordering_mode", "not in", [False, "nothing"])]
        )
        configs._ensure_valhalla_mobile_landing()
        return True

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
