# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class ProcurementOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def cron_update_so_line(self):
        procurements = self.search([("sale_line_id", "=", False)])
        _logger.info(f"Updating procurements {procurements}")
        for p in procurements:
            if tasks := self.env["project.task"].search(
                [("procurement_id", "=", p.id)]
            ):
                p.write({"sale_line_id": tasks[0].sale_line_id.id})
                self.env.cr.commit()
                _logger.info(f"Updated procurement {p}")
