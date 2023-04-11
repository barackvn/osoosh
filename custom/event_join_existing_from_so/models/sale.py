from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    joined_events_count = fields.Integer(
        string="Events Created", readonly=True, compute="_compute_joined_events_count"
    )
    joined_event_ids = fields.Many2many(
        "event.event",
        "event_sale_order_join_rel",
        "sale_order_id",
        "event_id",
        string="Joined Events",
        copy=False,
    )


    @api.depends("joined_event_ids")
    def _compute_joined_events_count(self):
        for order in self:
            order.joined_events_count = len(order.joined_event_ids)


    def _compute_has_event_product(self):
        for order in self:
            order.has_event_product = any(
                (
                    line.product_id.is_event_product
                    and line.product_id.event_template_id
                    and not line.linked_to_event
                )
                for line in order.order_line
            )

    def event_create_from_so_show_created_events(self):
        return {
            "name": "Event",
            "type": "ir.actions.act_window",
            "res_model": "event.event",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["sale_order_origin", "=", self.id]],
        }


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    linked_to_event = fields.Boolean("Linked to an Event")


    def create_event_from_order_line(self):
        product_id = self.product_id
        if product_id.is_event_product:
            event_template = product_id.event_template_id
            new_event = event_template.copy(default={"event_ticket_ids": False})
            template_ticket_id = self.env["event.event.ticket"]
            for ticket in event_template.event_ticket_ids:
                new_ticket = ticket.copy(default={"event_id": new_event.id})
                if product_id.ticket_id.id == ticket.id:
                    template_ticket_id = new_ticket

            if not template_ticket_id and new_event.event_ticket_ids:
                template_ticket_id = new_event.event_ticket_ids[0]

            self.write(
                {
                    "event_id": new_event.id,
                    "event_ticket_id": template_ticket_id.id,
                    "linked_to_event": True,
                }
            )

            for q in self.product_id.event_template_id.question_ids:
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
                    "sale_order_origin": self.order_id.id,
                    "sale_order_line_origin": self.id,
                    "event_template_id": event_template.id,
                }
            )
            if template_ticket_id:
                counter = 0
                while counter < self.product_uom_qty:
                    self.env["event.registration"].create(
                        {
                            "event_id": new_event.id,
                            "partner_id": self.order_id.partner_id.id,
                            "event_ticket_id": template_ticket_id.id,
                            "sale_order_id": self.order_id.id,
                            "sale_order_line_id": self.id,
                        }
                    )
                    counter += 1


    def join_event_from_order_line(self, event_id, ticket_id):
        self.write(
            {
                "event_id": event_id.id,
                "event_ticket_id": ticket_id.id,
                "linked_to_event": True,
            }
        )
        counter = 0
        while counter < self.product_uom_qty:
            self.env["event.registration"].create(
                {
                    "event_id": event_id.id,
                    "partner_id": self.order_id.partner_id.id,
                    "event_ticket_id": ticket_id.id,
                    "sale_order_id": self.order_id.id,
                    "sale_order_line_id": self.id,
                }
            )
            counter += 1
        self.order_id.write({"joined_event_ids": [(4, event_id.id)]})
