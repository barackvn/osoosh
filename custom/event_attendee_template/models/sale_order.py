# Part of Odoo. See LICENSE file for full copyright and licensing details.

import random
from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT


def random_token():
    # the token has an entropy of about 120 bits (6 bits/char * 20 chars)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.SystemRandom().choice(chars) for i in range(20))


def now(**kwargs):
    dt = datetime.now() + timedelta(**kwargs)
    return fields.Datetime.from_string(dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT))


class SaleOrder(models.Model):
    _inherit = "sale.order"


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        # for so in self:
        #     if any(so.order_line.filtered(lambda line: line.event_id)):
        #         return (
        #             self.env["ir.actions.act_window"]
        #             .with_context(default_sale_order_id=so.id)
        #             .for_xml_id("event_sale", "action_sale_order_event_registration")
        #         )
        return res


    def _compute_has_event_product(self):
        for order in self:
            order.has_event_product = False
            for line in order.order_line:
                if (
                    line.product_id.product_tmpl_id.is_event_product
                    and line.product_id.event_template_id
                ):
                    order.has_event_product = True
                    break


    def _cart_update(
        self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs
    ):
        values = super(SaleOrder, self)._cart_update(
            product_id, line_id, int(add_qty), set_qty, **kwargs
        )
        OrderLine = self.env["sale.order.line"]
        if line_id:
            line = OrderLine.browse(line_id)
            if line and line.product_id.product_tmpl_id.is_learning_product:
                old_qty = int(line.product_uom_qty)
                new_qty = set_qty if set_qty else (add_qty or 0 + old_qty)
                if line.product_id.event_template_id:
                    event_template_id = line.product_id.event_template_id
                    if not line.event_id:
                        line.write({"event_id": event_template_id.id})
                    if event_template_id and event_template_id.event_ticket_ids:
                        ticket_id = event_template_id.event_ticket_ids[0]
                        # removing attendees
                        if ticket_id and new_qty < old_qty:
                            attendees = self.env["event.registration"].search(
                                [
                                    ("state", "!=", "cancel"),
                                    # To avoid break on multi record set
                                    ("sale_order_id", "in", self.ids),
                                    ("event_ticket_id", "=", ticket_id.id),
                                ],
                                offset=new_qty,
                                limit=(old_qty - new_qty),
                                order="create_date asc",
                            )
                            attendees.button_reg_cancel()
                        elif ticket_id and new_qty > old_qty:
                            data = [
                                {
                                    "name": "",
                                    "event_ticket_id": ticket_id.id,
                                    "is_a_template": True,
                                    "sale_order_line_id": line.id,
                                }
                            ]
                            line._update_registrations(
                                confirm=False, registration_data=data
                            )
                            # add in return values the registrations, to display them on website (or not)
                            values["attendee_ids"] = (
                                self.env["event.registration"]
                                .search(
                                    [
                                        ("sale_order_line_id", "=", line.id),
                                        ("state", "!=", "cancel"),
                                    ]
                                )
                                .ids
                            )

        return values


    def action_send_late_reg_event_notification(self):
        attendee_ids = self.env["event.registration"].search(
            [("sale_order_id", "=", self.id), ("can_send_reminder", "=", True),]
        )
        if attendee_ids:
            self.send_late_reg_event_notification()
            message = _(
                "A reminder containing the following link has been sent to this partner: %s"
                % self.event_token_url
            )
            self.message_post(body=message)
        else:
            raise UserError(
                _("This sales order has no pending required details of registration.")
            )


    def send_late_reg_event_notification(self):
        self.ensure_one()
        if not self.event_token or (
            self.event_token_expiration and now(days=1) >= self.event_token_expiration
        ):
            expiration = now(days=360)
            token = random_token()
            self.sudo().write(
                {"event_token": token, "event_token_expiration": expiration}
            )
            self.env.cr.commit()
        message_template = self.sudo().env.ref("website_event_late_reg.late_reg_email")
        if message_template and self.partner_id.email:
            message_template.with_context(event_url=self.event_token_url).send_mail(
                self.partner_id.id, force_send=True
            )
        att_ids = self.env["event.registration"].search(
            [("sale_order_id.id", "=", self.id)]
        )
        for att_id in att_ids:
            message = _(
                "A reminder containing the following link has been sent to the attendee's related partner: %s"
                % self.event_token_url
            )
            att_id.message_post(body=message)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    def create_event_from_order_line(self):
        product_id = self.product_id
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
            if not self.event_id:
                self.write(
                    {
                        "event_id": new_event.id,
                        "event_ticket_id": template_ticket_id.id,
                        "linked_to_event": True,
                    }
                )

            for q in event_template.question_ids:
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

            AttendeeObj = self.env["event.registration"]

            template_attendee_ids = AttendeeObj.search(
                [("sale_order_line_id", "=", self.id), ("is_a_template", "=", True)]
            )

            if not template_attendee_ids:
                counter = 0
                while counter < self.product_uom_qty:
                    vals = {
                        "event_id": event_template.id,
                        "partner_id": self.order_id.partner_id.id,
                        "event_ticket_id": product_id.ticket_id.id,
                        "sale_order_id": self.order_id.id,
                        "sale_order_line_id": self.id,
                        "is_a_template": True,
                        "name": "",
                        "email": "",
                        "phone": "",
                        "attendee_dob": "",
                        "attendee_title": "",
                    }
                    new_attendee_template_id = AttendeeObj.create(vals)
                    template_attendee_ids |= new_attendee_template_id
                    counter += 1

            vals = {
                "event_id": new_event.id,
                "event_ticket_id": template_ticket_id.id,
                "is_a_template": False,
            }

            for att_id in template_attendee_ids:
                vals["template_id"] = att_id.id
                att_id.copy(vals)


    def join_event_from_order_line(self, event_id, ticket_id):
        product_id = self.product_id
        event_template = product_id.event_template_id

        # Only write on the event_id field for the first event that will be linked to the sales order line
        if not self.event_id:
            self.write(
                {
                    "event_id": event_id.id,
                    "event_ticket_id": ticket_id.id,
                    "linked_to_event": True,
                }
            )

        # If new event is not the same as the event linked to order line,
        # it means that attendee records to be created are no longer templates
        # and should be linked to the template attendees

        AttendeeObj = self.env["event.registration"]

        template_attendee_ids = AttendeeObj.search(
            [("sale_order_line_id", "=", self.id), ("is_a_template", "=", True)]
        )

        if not template_attendee_ids:
            counter = 0
            while counter < self.product_uom_qty:
                vals = {
                    "event_id": event_template.id,
                    "partner_id": self.order_id.partner_id.id,
                    "event_ticket_id": product_id.ticket_id.id,
                    "sale_order_id": self.order_id.id,
                    "sale_order_line_id": self.id,
                    "is_a_template": True,
                    "name": "",
                    "email": "",
                    "phone": "",
                    "attendee_dob": "",
                    "attendee_title": "",
                }
                new_attendee_template_id = AttendeeObj.create(vals)
                template_attendee_ids |= new_attendee_template_id
                counter += 1

        vals = {
            "event_id": event_id.id,
            "event_ticket_id": ticket_id.id,
            "is_a_template": False,
        }

        for att_id in template_attendee_ids:
            vals["template_id"] = att_id.id
            att_id.copy(vals)

        self.order_id.write({"joined_event_ids": [(4, event_id.id)]})


    def _update_registrations(
        self, confirm=True, cancel_to_draft=False, registration_data=None
    ):
        """ Create or update registrations linked to a sales order line. A sale
        order line has a product_uom_qty attribute that will be the number of
        registrations linked to this line. This method update existing registrations
        and create new one for missing one. """
        for order_line in self:
            event_template_id = (
                order_line.event_id
                or order_line.product_id.product_tmpl_id.event_template_id
            )
            Registration = self.env["event.registration"].sudo()
            registrations = Registration.search(
                [("sale_order_line_id", "in", self.ids)]
            )
            # for so_line in self.filtered('product_id.event_template_id'):
            #     existing_registrations = registrations.filtered(lambda r: r.sale_order_line_id.id == so_line.id)
            #     if confirm:
            #         existing_registrations.filtered(lambda r: r.state not in ['open', 'cancel']).confirm_registration()
            #     if cancel_to_draft:
            #         existing_registrations.filtered(lambda r: r.state == 'cancel').do_draft()

            for count in range(int(order_line.product_uom_qty)):
                registration = {}
                if registration_data:
                    registration = registration_data.pop()
                # TDE CHECK: auto confirmation
                registration["event_id"] = event_template_id
                registration["sale_order_line_id"] = order_line
                registration['is_a_template'] = True
                Registration.with_context(registration_force_draft=True).create(
                    Registration._synchronize_so_line_values(order_line)
                )
        return True
