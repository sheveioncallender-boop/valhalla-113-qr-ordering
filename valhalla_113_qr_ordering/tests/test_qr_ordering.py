from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestValhallaQrOrdering(TransactionCase):
    def test_table_fields_are_available(self):
        table_model = self.env["restaurant.table"]
        self.assertIn("valhalla_qr_enabled", table_model._fields)
        self.assertIn("identifier", table_model._fields)

    def test_pos_order_has_qr_marker(self):
        self.assertIn("valhalla_qr_order", self.env["pos.order"]._fields)
