# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class Lead(models.Model):
    _inherit = "crm.lead"


    def create_quotation_from_lead(self):
        self.ensure_one()
        ctx = self._context.copy()
        ctx.update(
            {
                "default_partner_id": self.partner_id.parent_id.id
                or self.partner_id.id,
                "default_team_id": self.team_id.id,
                "default_opportunity_id": self.id,
            }
        )
        return {
            "name": _("New Quotation"),
            "view_type": "form",
            "view_mode": "form",
            "res_model": "sale.order",
            "view_id": False,
            "type": "ir.actions.act_window",
            "context": ctx,
        }


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def cron_use_company_as_partner(self):
        sale_orders = self.search(
            [
                ("partner_id.is_company", "=", False),
                ("partner_id.parent_id", "!=", False),
            ]
        )
        _logger.info(f"Updating sale orders {sale_orders}")
        for sale_order in sale_orders:
            sale_order.write({"partner_id": sale_order.partner_id.parent_id.id})
            self.env.cr.commit()

        attendees = self.env["event.registration"].search(
            [
                ("partner_id.is_company", "=", False),
                ("partner_id.parent_id", "!=", False),
            ]
        )
        _logger.info(f"Updating attendees {attendees}")
        for att in attendees:
            att.write({"partner_id": att.partner_id.parent_id.id})
            self.env.cr.commit()

        tasks = self.env["project.task"].search(
            [
                ("partner_id.is_company", "=", False),
                ("partner_id.parent_id", "!=", False),
            ]
        )
        _logger.info(f"Updating tasks {tasks}")
        for task in tasks:
            task.write({"partner_id": task.partner_id.parent_id.id})
            self.env.cr.commit()
