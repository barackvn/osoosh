from odoo import fields, models


class Events(models.Model):
    _inherit = "event.event"

    sale_order_origin = fields.Many2one("sale.order", string="Sale Order Origin")
    sale_order_line_origin = fields.Many2one(
        "sale.order.line", string="Sale Order Line Origin"
    )
