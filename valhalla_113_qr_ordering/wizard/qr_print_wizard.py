from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ValhallaQrPrintWizard(models.TransientModel):
    _name = "valhalla.qr.print.wizard"
    _description = "Valhalla Table QR Card Printing"

    pos_config_id = fields.Many2one(
        "pos.config",
        string="Restaurant Point of Sale",
        required=True,
    )
    available_floor_ids = fields.Many2many(
        "restaurant.floor",
        relation="valhalla_qr_wizard_available_floor_rel",
        column1="wizard_id",
        column2="floor_id",
        compute="_compute_available_records",
    )
    available_table_ids = fields.Many2many(
        "restaurant.table",
        relation="valhalla_qr_wizard_available_table_rel",
        column1="wizard_id",
        column2="table_id",
        compute="_compute_available_records",
    )
    floor_ids = fields.Many2many(
        "restaurant.floor",
        relation="valhalla_qr_wizard_floor_rel",
        column1="wizard_id",
        column2="floor_id",
        string="Floors",
        domain="[('id', 'in', available_floor_ids)]",
    )
    table_ids = fields.Many2many(
        "restaurant.table",
        relation="valhalla_qr_wizard_table_rel",
        column1="wizard_id",
        column2="table_id",
        string="Tables",
        domain="[('id', 'in', available_table_ids)]",
    )
    include_inactive = fields.Boolean(string="Include Inactive Tables", default=False)
    layout = fields.Selection(
        [
            ("four_up", "4 Cards per A4 Page"),
            ("single", "1 Large Card per Page"),
        ],
        string="Print Layout",
        required=True,
        default="four_up",
    )
    heading = fields.Char(
        string="Heading",
        required=True,
        default="SCAN • ORDER • ENJOY",
    )
    instruction = fields.Char(
        string="Instruction",
        required=True,
        default="Scan the code to view the menu and place your order.",
    )
    footer_text = fields.Char(
        string="Footer",
        default="Your order goes directly to the Valhalla 113 team.",
    )
    show_url = fields.Boolean(string="Show URL")
    table_count = fields.Integer(compute="_compute_table_count")
    setup_ready = fields.Boolean(compute="_compute_setup_ready")

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        config = self.env["pos.config"]
        if values.get("pos_config_id"):
            config = config.browse(values["pos_config_id"]).exists()
        if not config:
            config = self.env["pos.config"].search(
                [("module_pos_restaurant", "=", True)], limit=1
            ) or self.env["pos.config"].search([], limit=1)
            if config:
                values["pos_config_id"] = config.id
        if config:
            if "default_heading" not in self.env.context:
                values["heading"] = config.valhalla_qr_heading
            if "default_instruction" not in self.env.context:
                values["instruction"] = config.valhalla_qr_instruction
            if "default_footer_text" not in self.env.context:
                values["footer_text"] = config.valhalla_qr_footer
            if "default_show_url" not in self.env.context:
                values["show_url"] = config.valhalla_qr_show_url

            floors = config.floor_ids.filtered("active")
            tables = floors.table_ids.filtered(
                lambda table: table.active and table.valhalla_qr_enabled
            )
            if "default_floor_ids" not in self.env.context:
                values["floor_ids"] = [(6, 0, floors.ids)]
            if "default_table_ids" not in self.env.context:
                values["table_ids"] = [(6, 0, tables.ids)]
        return values

    @api.depends("pos_config_id", "include_inactive", "floor_ids")
    def _compute_available_records(self):
        Floor = self.env["restaurant.floor"]
        for wizard in self:
            floors = wizard.pos_config_id.floor_ids if wizard.pos_config_id else Floor
            tables = floors.table_ids
            if not wizard.include_inactive:
                floors = floors.filtered("active")
                tables = tables.filtered("active")
            if wizard.floor_ids:
                tables = tables.filtered(
                    lambda table: table.floor_id in wizard.floor_ids
                )
            tables = tables.filtered("valhalla_qr_enabled")
            wizard.available_floor_ids = floors
            wizard.available_table_ids = tables

    @api.depends("table_ids")
    def _compute_table_count(self):
        for wizard in self:
            wizard.table_count = len(wizard.table_ids)

    @api.depends(
        "pos_config_id.module_pos_restaurant",
        "pos_config_id.self_ordering_mode",
        "pos_config_id.self_ordering_service_mode",
        "pos_config_id.self_ordering_pay_after",
    )
    def _compute_setup_ready(self):
        for wizard in self:
            config = wizard.pos_config_id
            wizard.setup_ready = bool(
                config
                and config.module_pos_restaurant
                and config.self_ordering_mode == "mobile"
                and config.self_ordering_service_mode == "table"
                and config.self_ordering_pay_after == "meal"
            )

    @api.onchange("pos_config_id")
    def _onchange_pos_config_id(self):
        if not self.pos_config_id:
            self.floor_ids = [(5, 0, 0)]
            self.table_ids = [(5, 0, 0)]
            return
        floors = self.pos_config_id.floor_ids
        tables = floors.table_ids
        if not self.include_inactive:
            floors = floors.filtered("active")
            tables = tables.filtered("active")
        tables = tables.filtered("valhalla_qr_enabled")
        if not self.env.context.get("valhalla_preserve_table_selection"):
            self.floor_ids = floors
            self.table_ids = tables
        self.heading = self.pos_config_id.valhalla_qr_heading
        self.instruction = self.pos_config_id.valhalla_qr_instruction
        self.footer_text = self.pos_config_id.valhalla_qr_footer
        self.show_url = self.pos_config_id.valhalla_qr_show_url

    @api.onchange("include_inactive")
    def _onchange_include_inactive(self):
        if not self.pos_config_id:
            return
        floors = self.pos_config_id.floor_ids
        tables = floors.table_ids
        if not self.include_inactive:
            floors = floors.filtered("active")
            tables = tables.filtered("active")
        tables = tables.filtered("valhalla_qr_enabled")
        if not self.env.context.get("valhalla_preserve_table_selection"):
            self.floor_ids = floors
            self.table_ids = tables

    @api.onchange("floor_ids")
    def _onchange_floor_ids(self):
        if self.env.context.get("valhalla_preserve_table_selection") and self.table_ids:
            return
        tables = self.floor_ids.table_ids
        if not self.include_inactive:
            tables = tables.filtered("active")
        self.table_ids = tables.filtered("valhalla_qr_enabled")

    def action_apply_setup(self):
        self.ensure_one()
        if not self.pos_config_id:
            raise UserError(_("Select a Point of Sale first."))
        self.pos_config_id.action_apply_valhalla_qr_setup()
        return {
            "name": _("Print Valhalla Table QR Cards"),
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
            "context": dict(self.env.context),
        }

    def action_preview_menu(self):
        self.ensure_one()
        if not self.pos_config_id:
            raise UserError(_("Select a Point of Sale first."))
        return self.pos_config_id.preview_self_order_app()

    def _selected_tables(self):
        self.ensure_one()
        tables = self.table_ids.filtered("valhalla_qr_enabled")
        if not self.include_inactive:
            tables = tables.filtered("active")
        return tables.sorted(
            key=lambda table: (
                table.floor_id.sequence,
                table.floor_id.name or "",
                table.table_number,
                table.id,
            )
        )

    def _validate_printing(self):
        self.ensure_one()
        config = self.pos_config_id
        if not config:
            raise UserError(_("Select a Restaurant Point of Sale."))
        if not self.setup_ready:
            raise UserError(
                _(
                    "The selected POS is not configured for QR menu + ordering at "
                    "tables. Click 'Apply Valhalla QR Setup' first."
                )
            )
        if not config.floor_ids:
            raise UserError(_("Add at least one restaurant floor to the POS."))
        if not self._selected_tables():
            raise UserError(_("Select at least one QR-enabled restaurant table."))

    def action_print(self):
        self.ensure_one()
        self._validate_printing()
        now = fields.Datetime.now()
        for table in self._selected_tables():
            table.write(
                {
                    "valhalla_qr_print_count": table.valhalla_qr_print_count + 1,
                    "valhalla_qr_last_printed_at": now,
                }
            )
        return self.env.ref(
            "valhalla_113_qr_ordering.action_report_valhalla_qr_cards"
        ).report_action(self)

    def _get_report_cards(self):
        self.ensure_one()
        self._validate_printing()
        return [
            {
                "table_id": table.id,
                "table_number": table.table_number,
                "table_label": table.valhalla_qr_label
                or _("TABLE %(number)s", number=table.table_number),
                "floor_name": table.floor_id.name,
                "seats": table.seats,
                "url": self.pos_config_id._get_self_order_url(table.id),
            }
            for table in self._selected_tables()
        ]
