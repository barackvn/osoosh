# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Task(models.Model):
    _inherit = "project.task"

    joined_events_count = fields.Integer(
        string="Events Created", readonly=True, compute="_compute_joined_events_count"
    )
    joined_event_ids = fields.Many2many(
        "event.event",
        "event_task_join_rel",
        "task_id",
        "event_id",
        string="Joined Events",
        copy=False,
    )


    @api.depends("joined_event_ids")
    def _compute_joined_events_count(self):
        for task in self:
            task.joined_events_count = len(task.joined_event_ids)


    def create_event_from_task(self):
        line = self.sale_line_id
        product_id = line.product_id
        event_template = product_id.event_template_id
        if product_id.is_event_product:
            new_event = event_template.copy(default={"event_ticket_ids": False})
            template_ticket_id = self.env["event.event.ticket"]
            for ticket in event_template.event_ticket_ids:
                new_ticket = ticket.copy(default={"event_id": new_event.id})
                if product_id.ticket_id.id == ticket.id:
                    template_ticket_id = new_ticket

            if not template_ticket_id and new_event.event_ticket_ids:
                template_ticket_id = new_event.event_ticket_ids[0]

            line.write(
                {"event_id": new_event.id, "event_ticket_id": template_ticket_id.id}
            )

            for q in line.product_id.event_template_id.question_ids:
                new_question = self.env["event.question"].create(
                    {
                        "title": q.title,
                        "sequence": q.sequence,
                        "is_individual": q.is_individual,
                        "event_id": new_event.id,
                    }
                )
                for ans in q.answer_ids:
                    new_answer = self.env["event.answer"].create(
                        {
                            "name": ans.name,
                            "sequence": ans.sequence,
                            "question_id": new_question.id,
                        }
                    )
        new_event.write(
            {
                "sale_order_origin": line.order_id.id,
                "sale_order_line_origin": line.id,
                "task_id": self.id,
                "event_template_id": event_template.id,
            }
        )
        if template_ticket_id:
            counter = 0
            while counter < line.product_uom_qty:
                self.env["event.registration"].create(
                    {
                        "event_id": new_event.id,
                        "partner_id": line.order_id.partner_id.id,
                        "event_ticket_id": template_ticket_id.id,
                        "sale_order_id": line.order_id.id,
                        "sale_order_line_id": line.id,
                        "date_open": fields.Datetime.now(),
                    }
                )
                counter += 1


    def join_event_from_task(self, event_id, ticket_id):
        line = self.sale_line_id
        product_id = line.product_id
        event_template = product_id.event_template_id
        line.write({"event_id": event_id.id, "event_ticket_id": ticket_id.id})
        counter = 0
        while counter < line.product_uom_qty:
            att = self.env["event.registration"].create(
                {
                    "event_id": event_id.id,
                    "partner_id": self.partner_id.id,
                    "event_ticket_id": ticket_id.id,
                    "sale_order_id": line.order_id.id,
                    "sale_order_line_id": line.id,
                    "date_open": fields.Datetime.now(),
                }
            )
            counter += 1
        self.write({"joined_event_ids": [(4, event_id.id)]})
