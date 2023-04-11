# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Task(models.Model):
    _inherit = "project.task"

    product_id = fields.Many2one("product.product", "Product", store=True)
    zip_first_two_digits = fields.Char(
        "Zip [First 2 Digits]", store=True, compute="_get_zip_first_two_digits"
    )


    @api.depends("partner_id.zip")
    def _get_zip_first_two_digits(self):
        for task in self:
            task.zip_first_two_digits = (
                task.partner_id.zip[:2]
                if task.partner_id.zip and len(task.partner_id.zip) >= 2
                else ""
            )
