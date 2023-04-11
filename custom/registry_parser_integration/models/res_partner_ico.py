# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PartnerICO(models.Model):
    _name = "res.partner.ico"

    name = fields.Char("ICO", required=True)
    partner_id = fields.Many2one("res.partner", "Related Partner")
    invalid = fields.Boolean("Invalid")

    @api.model
    def _cron_fetch_data_from_registry_parser(self):
        ico_ids = self.search(
            [("partner_id", "=", False), ("invalid", "=", False)], limit=500
        )
        for ico_id in ico_ids:
            if partner_id := self.env["res.partner"].search(
                [("company_registry", "=", ico_id.name)]
            ):
                partner_id.fetch_registry_data(raise_exception=False)
                ico_id.write({"partner_id": partner_id.id})
            else:
                partner_id = partner_id.create(
                    {
                        "name": ico_id.name,
                        "company_registry": ico_id.name,
                        "is_company": True,
                        "customer": True,
                    }
                )
                if valid := partner_id.fetch_registry_data(raise_exception=False):
                    ico_id.write({"partner_id": partner_id.id})
                    _logger.info(f"Company registry {partner_id.id} updated.")
                else:
                    partner_id.unlink()
                    ico_id.write({"invalid": True})
                    _logger.info(f"Company registry {ico_id.name} not found.")
            self.env.cr.commit()
