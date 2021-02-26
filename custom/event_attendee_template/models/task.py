# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Task(models.Model):
    _inherit = "project.task"


    def create_event_from_task(self):
        line = self.sale_line_id
        product_id = line.product_id
        event_template = product_id.event_template_id
        if product_id.product_tmpl_id.is_event_product:
            new_event = event_template.copy(default={"event_ticket_ids": False})
            template_ticket_id = self.env["event.event.ticket"]
            for ticket in event_template.event_ticket_ids:
                new_ticket = ticket.copy(default={"event_id": new_event.id})
                if product_id.ticket_id.id == ticket.id:
                    template_ticket_id = new_ticket

            if not template_ticket_id and new_event.event_ticket_ids:
                template_ticket_id = new_event.event_ticket_ids[0]

            # Only write on the event_id field for the first event that will be linked to the sales order line
            if not line.event_id:
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

        # If new event is not the same as the event linked to order line,
        # it means that attendee records to be created are no longer templates
        # and should be linked to the template attendees

        AttendeeObj = self.env["event.registration"]

        template_attendee_ids = AttendeeObj.search(
            [("sale_order_line_id", "=", line.id), ("is_a_template", "=", True)]
        )

        if not template_attendee_ids:
            counter = 0
            while counter < line.product_uom_qty:
                vals = {
                    "event_id": event_template.id,
                    "partner_id": line.order_id.partner_id.id,
                    "event_ticket_id": product_id.ticket_id.id,
                    "sale_order_id": line.order_id.id,
                    "sale_order_line_id": line.id,
                    "is_a_template": True,
                    "name": "",
                    "email": "",
                    "phone": "",
                    "attendee_dob": "",
                    "attendee_title": "",
                    "date_open": fields.Datetime.now(),
                }
                new_attendee_template_id = AttendeeObj.create(vals)
                template_attendee_ids |= new_attendee_template_id
                counter += 1

        vals = {
            "event_id": new_event.id,
            "event_ticket_id": template_ticket_id.id,
            "is_a_template": False,
            "task_id": self.id,
            "sale_order_id": self.sale_line_id.order_id.id,
            "sale_order_line_id": self.sale_line_id.id,
        }
        for att_id in template_attendee_ids:
            vals["template_id"] = att_id.id
            att_id.copy(vals)


    def join_event_from_task(self, event_id, ticket_id):
        line = self.sale_line_id
        product_id = line.product_id
        event_template = product_id.product_tmpl_id.event_template_id

        # Only write on the event_id field for the first event that will be linked to the sales order line
        if not line.event_id:
            line.write({"event_id": event_id.id, "event_ticket_id": ticket_id.id})

        AttendeeObj = self.env["event.registration"]

        template_attendee_ids = AttendeeObj.search(
            [("sale_order_line_id", "=", line.id), ("is_a_template", "=", True)]
        )

        if not template_attendee_ids:
            counter = 0
            while counter < line.product_uom_qty:
                vals = {
                    "event_id": event_template.id,
                    "partner_id": self.partner_id.id,
                    "event_ticket_id": product_id.ticket_id.id,
                    "sale_order_id": line.order_id.id,
                    "sale_order_line_id": line.id,
                    "is_a_template": True,
                    "name": "",
                    "email": "",
                    "phone": "",
                    "attendee_dob": "",
                    "attendee_title": "",
                    "date_open": fields.Datetime.now(),
                }
                new_attendee_template_id = AttendeeObj.create(vals)
                template_attendee_ids |= new_attendee_template_id
                counter += 1

        vals = {
            "event_id": event_id.id,
            "event_ticket_id": ticket_id.id,
            "is_a_template": False,
            "task_id": self.id,
        }

        for att_id in template_attendee_ids:
            vals["template_id"] = att_id.id
            att_id.copy(vals)

        self.write({"joined_event_ids": [(4, event_id.id)]})
