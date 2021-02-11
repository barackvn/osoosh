# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    confirmation_date = fields.Datetime(
        string="Date Confirmed",
        readonly=True,
        help="Date on which the sale order is confirmed.",
    )


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for so in self:
            so.confirmation_date = fields.Datetime.now()
        return True
