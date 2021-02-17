from odoo import api, fields, models


class Task(models.Model):
    _inherit = "project.task"

    can_create_event = fields.Boolean(
        "Can create event", compute="compute_can_create_event"
    )
    event_ids = fields.One2many("event.event", "task_id", "Events")
    events_count = fields.Integer("Events Count", compute="compute_event_ids_count")


    @api.depends("event_ids")
    def compute_event_ids_count(self):
        for task in self:
            task.events_count = len(task.event_ids)


    @api.depends("sale_line_id.product_id.is_event_product")
    def compute_can_create_event(self):
        for task in self:
            task.can_create_event = task.sale_line_id.product_id.is_event_product


    def button_create_event(self):
        self.ensure_one()
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
                    self.env["event.answer"].create(
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
                    }
                )
                counter += 1
