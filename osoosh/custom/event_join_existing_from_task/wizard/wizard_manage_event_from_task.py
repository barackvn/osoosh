# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EventJoinExisting(models.TransientModel):
    _name = "event.manage.from.task.wizard"

    def _default_task(self):
        return (
            self._context.get("active_model") == "project.task"
            and self._context.get("active_ids")[0]
        )

    task_id = fields.Many2one("project.task", "Task", default=_default_task)
    action = fields.Selection(
        [("create", "Create New Event"), ("join", "Join existing event")]
    )
    event_id = fields.Many2one("event.event", "Event to Join")
    ticket_id = fields.Many2one("event.event.ticket", "Ticket")


    @api.onchange("task_id")
    def onchange_sale_order_line_id(self):
        if not self.task_id:
            return {"domain": {"event_id": []}}
        return {
            "domain": {
                "event_id": [
                    (
                        "event_template_id.id",
                        "=",
                        self.task_id.sale_line_id.product_id.event_template_id.id,
                    ),
                    ("state", "!=", "cancel"),
                    ("date_begin", ">=", datetime.today()),
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


    def button_manage_event(self):
        self.ensure_one()
        now = datetime.now()
        if self.action == "create":
            self.task_id.create_event_from_task()
        if self.action == "join":
            if self.event_id:
                if self.ticket_id:
                    self.task_id.join_event_from_task(self.event_id, self.ticket_id)
                else:
                    raise UserError(_("Please select a ticket."))
            else:
                raise UserError(_("Please select an event to join."))
        return {"type": "ir.actions.act_window_close"}
