from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_event_product = fields.Boolean(
        "Has event product", compute="_compute_has_event_product"
    )
    events_count = fields.Integer(
        string="Events Created", readonly=True, compute="_compute_events_count"
    )
    event_ids = fields.One2many("event.event", "sale_order_origin", "Events")


    @api.depends("event_ids")
    def _compute_events_count(self):
        for order in self:
            order.events_count = len(order.event_ids)


    def _compute_has_event_product(self):
        for order in self:
            order.has_event_product = False
            for line in order.order_line:
                if (
                    line.product_id.is_event_product
                    and line.product_id.event_template_id
                ):
                    order.has_event_product = True
                    break


    def button_create_event(self):
        self.ensure_one()
        for line in self.order_line:
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
                    {"sale_order_origin": self.id, "sale_order_line_origin": line.id}
                )
                counter = 0
                if template_ticket_id:
                    while counter < line.product_uom_qty:
                        self.env["event.registration"].create(
                            {
                                "event_id": new_event.id,
                                "partner_id": self.partner_id.id,
                                "event_ticket_id": template_ticket_id.id,
                                "sale_order_id": self.id,
                                "sale_order_line_id": line.id,
                            }
                        )
                        counter += 1


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_event_product = fields.Boolean(string="Is an Event Product")
    event_template_id = fields.Many2one("event.event", "Event template")
    ticket_id = fields.Many2one("event.event.ticket", "Event Ticket")

    @api.onchange("event_template_id")
    def onchange_event_template_id(self):
        if self.event_template_id:
            return {
                "domain": {"ticket_id": [("event_id", "=", self.event_template_id.id)]}
            }

    @api.model
    def create(self, vals):
        product_template_id = super(ProductTemplate, self).create(vals)
        related_vals = {}
        if vals.get("event_template_id"):
            related_vals["event_template_id"] = vals.get("event_template_id")
        if vals.get("ticket_id"):
            related_vals["ticket_id"] = vals.get("ticket_id")
        if related_vals:
            product_template_id.write(related_vals)
        return product_template_id


class ProductProduct(models.Model):
    _inherit = "product.product"

    event_template_id = fields.Many2one('event.event',related="product_tmpl_id.event_template_id", string='Event template')
    ticket_id = fields.Many2one("event.event.ticket", string="Event Ticket")

    # @api.onchange("event_template_id")
    # def onchange_event_template_id(self):
    #     if self.event_template_id:
    #         return {
    #             "domain": {"ticket_id": [("event_id", "=", self.event_template_id.id)]}
    #         }
