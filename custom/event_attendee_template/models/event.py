# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import UserError



class Event(models.Model):
    _inherit = "event.event"

    joined_sale_orders_count = fields.Integer(
        string="Joined SO", readonly=True, compute="_compute_joined_sale_orders_count"
    )
    joined_tasks_count = fields.Integer(
        string="Joined Tasks", readonly=True, compute="_compute_joined_tasks_count"
    )


    @api.depends("joined_sale_order_ids")
    def _compute_joined_sale_orders_count(self):
        for event in self:
            event.joined_sale_orders_count = len(event.joined_sale_order_ids)


    @api.depends("joined_task_ids")
    def _compute_joined_tasks_count(self):
        for event in self:
            event.joined_tasks_count = len(event.joined_task_ids)


    def generate_event_certificates(self, invoice_id, so_line_ids):
        """
            Generates certificates for possibly multiple events with sale order line in so_line_ids (a list) and invoice id (an int)
        """
        cert_ids = False
        att_ids = self.mapped("registration_ids").filtered(
            lambda r: r.sale_order_line_id.id in so_line_ids and r.state == "done"
        )
        if att_ids:
            for att_id in att_ids:
                if not att_id.certificate_ids and att_id.event_id.is_event_certificate:
                    cert_id = self.env["event.certificate"].create(
                        {
                            "attendee_id": att_id.id,
                            "invoice_id": invoice_id,
                            "release_date": datetime.now().strftime("%Y-%m-%d"),
                        }
                    )
                    self.env.cr.commit()
            cert_ids = att_ids.mapped("certificate_ids")
            for c in cert_ids:
                # self.env["ir.actions.report"].get_pdf(c, "event_custom_4devnet.report_certificate")
                self.env.ref(
                    "event_custom_4devnet.event_certificate_report"
                )._render_qweb_pdf(c.ids)
        return cert_ids


class Attendee(models.Model):
    _inherit = "event.registration"

    is_a_template = fields.Boolean("Is a Template")
    task_id = fields.Many2one(comodel_name='project.task', string='Task')
    template_id = fields.Many2one(
        "event.registration", "Template", domain=[("is_a_template", "=", True)]
    )


    @api.model
    def _synchronize_so_line_values(self, so_line):
        att_data = super(Attendee, self)._synchronize_so_line_values(so_line)
        # line_id = registration.get('sale_order_line_id')
        if so_line:
            att_data.update({'is_a_template': True})
            # if not so_line.product_id.event_template_id.id:
            #     raise UserError(_("Please define event template in ({0} , {1})".format(so_line.product_id.name, so_line.product_id.id)))
            if so_line.product_id.event_template_id.id:
                att_data.update({
                    'event_id': so_line.product_id.event_template_id.id,
                    'event_ticket_id': so_line.product_id.ticket_id.id,
                    'name': '',
                    'email': '',
                    'phone': ''
                })
        return att_data


    def write(self, vals):
        res = super(Attendee, self).write(vals)
        template_fields = ("name", "attendee_dob", "attendee_title", "phone", "email")
        if (
            self.is_a_template or ("is_a_template" in vals and vals["is_a_template"])
        ) and any(f in vals for f in template_fields):
            att_ids_to_update = self.search([("template_id", "=", self.id)])
            values_to_update = {}
            for f in template_fields:
                if f in vals:
                    values_to_update[f] = vals[f]
            for att_id in att_ids_to_update:
                att_id.write(values_to_update)
        return res


    def confirm_registration(self):
        self.state = "open"

        # auto-trigger after_sub (on subscribe) mail schedulers, if needed
        if self.sale_order_line_id.product_id.event_template_id.id != self.event_id.id:
            onsubscribe_schedulers = self.event_id.event_mail_ids.filtered(
                lambda s: s.interval_type == "after_sub"
            )
            onsubscribe_schedulers.execute()

    @api.depends(
        "name",
        "attendee_dob",
        "attendee_title",
        "event_id.is_event_certificate",
        "email",
        "sale_order_state",
        "is_a_template",
        "template_id",
    )
    def get_can_send_reminder(self):
        # A reminder can be sent if attendee is a template, check if attendee data is complete
        # If attendee is not a template, check if data on the template is complete
        # Migration reqt: Current attendees in db should be marked as a template or if not, assign a template
        for att in self:
            if att.sale_order_state not in ["draft", "cancel"]:
                if att.is_a_template:
                    can_send_reminder = not (att.name and att.email)
                    if can_send_reminder and att.event_id.is_event_certificate:
                        can_send_reminder = not (
                            att.attendee_title and att.attendee_dob
                        )
                    att.can_send_reminder = can_send_reminder
                elif att.template_id:
                    template_id = att.template_id
                    can_send_reminder = not (template_id.name and template_id.email)
                    event_template_id = (
                        att.sale_order_line_id.product_id.event_template_id
                    )
                    if can_send_reminder and event_template_id.is_event_certificate:
                        can_send_reminder = not (
                            template_id.attendee_title and template_id.attendee_dob
                        )
                    att.can_send_reminder = can_send_reminder
                else:
                    att.can_send_reminder = False
            else:
                att.can_send_reminder = False


    def action_sync_linked_attendees(self):
        for att_id in self:
            values = {
                "name": att_id.name,
                "attendee_dob": att_id.attendee_dob,
                "attendee_title": att_id.attendee_title,
                "phone": att_id.phone,
                "email": att_id.email,
            }
            if att_id.is_a_template:
                att_ids_to_update = self.search([("template_id", "=", self.id)])
                for att_id_to_update in att_ids_to_update:
                    att_id_to_update.write(values)
            elif not att_id.is_a_template and att_id.template_id:
                att_id.template_id.write(values)
