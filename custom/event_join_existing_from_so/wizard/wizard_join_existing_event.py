from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EventJoinExisting(models.TransientModel):
    _name = "event.join.existing.wizard"

    def _default_sale_order(self):
        return (
            self._context.get("active_model") == "sale.order"
            and self._context.get("active_ids")[0]
        )

    sale_order_id = fields.Many2one(
        "sale.order", "Sale Order", default=_default_sale_order
    )
    sale_order_line_id = fields.Many2one(
        "sale.order.line", "Sale Order Line", required=True
    )
    action = fields.Selection(
        [("create", "Create New Event"), ("join", "Join existing event")]
    )
    event_id = fields.Many2one("event.event", "Event to Join")
    ticket_id = fields.Many2one("event.event.ticket", "Ticket")


    @api.onchange("sale_order_id")
    def onchange_sale_order_id(self):
        return {
            "domain": {
                "sale_order_line_id": [
                    ("order_id.id", "=", self.sale_order_id.id),
                    ("product_id.event_template_id", "!=", False),
                ]
            }
        }


    @api.onchange("sale_order_line_id")
    def onchange_sale_order_line_id(self):
        if not self.sale_order_line_id:
            return {"domain": {"event_id": []}}
        return {
            "domain": {
                "event_id": [
                    (
                        "event_template_id.id",
                        "=",
                        self.sale_order_line_id.product_id.event_template_id.id,
                    ),
                    ("state", "!=", "cancel"),
                    ("date_begin", ">=", datetime.today().strftime("%Y-%m-%d")),
                ]
            }
        }


    @api.onchange("event_id")
    def onchange_event_id(self):
        if not self.event_id:
            return {"domain": {"ticket_id": []}}
        return {
            "domain": {"ticket_id": [("id", "in", self.event_id.event_ticket_ids.ids)]}
        }


    def button_manage_events(self):
        self.ensure_one()
        if self.action == "create":
            self.sale_order_line_id.create_event_from_order_line()
        if self.action == "join":
            if self.event_id:
                if self.ticket_id:
                    self.sale_order_line_id.join_event_from_order_line(
                        self.event_id, self.ticket_id
                    )
                else:
                    raise UserError(_("Please select a ticket."))
            else:
                raise UserError(_("Please select an event to join."))
        return {"type": "ir.actions.act_window_close"}
