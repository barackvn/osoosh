# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    product_ids = fields.Many2many(
        "product.product", string="Products", compute="_compute_products", store=True
    )


    @api.depends("sale_order_ids")
    def _compute_products(self):
        product_ids = []
        for sale_order_id in self.sale_order_ids:
            for line in sale_order_id.order_line:
                product_ids.append(line.product_id.id)
        self.product_ids = self.env["product.product"].browse(list(set(product_ids)))
