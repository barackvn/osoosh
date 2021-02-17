# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class Attendees(models.Model):
    _inherit = "event.registration"

    event_token_valid = fields.Boolean(
        string="Token is Valid?", related="sale_order_id.event_token_valid", store=True
    )
    event_token_url = fields.Char(
        string="Token URL", related="sale_order_id.event_token_url", store=True
    )
    sale_order_state = fields.Selection(
        string="Sale Order State", related="sale_order_id.state", store=True
    )


    def button_send_reminder(self):
        for record in self:
            record.sale_order_id.send_late_reg_event_notification()

    @api.model
    def _cron_send_reminder_to_complete_registration(self):
        incomplete_attendees = self.search(
            [("name", "=", False), ("sale_order_id.state", "in", ["sale", "done"])]
        )
        so_ids = incomplete_attendees.mapped("sale_order_id")
        for order in so_ids:
            order.send_late_reg_event_notification()
