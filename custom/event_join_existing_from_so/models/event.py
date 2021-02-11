from odoo import fields, models


class Events(models.Model):
    _inherit = "event.event"

    event_template_id = fields.Many2one("event.event", "Event template")
    joined_sale_order_ids = fields.Many2many(
        "sale.order",
        "event_sale_order_join_rel",
        "event_id",
        "sale_order_id",
        string="Joined Sale Orders",
    )
