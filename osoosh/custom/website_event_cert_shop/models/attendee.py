from datetime import datetime

from odoo import api, fields, models


class Attendee(models.Model):
    _inherit = "event.registration"

    attendee_title = fields.Char(string="Attendee Title")
    can_send_reminder = fields.Boolean(
        string="Can send reminder", compute="get_can_send_reminder", store=True
    )


    @api.depends(
        "name",
        "attendee_dob",
        "attendee_title",
        "event_id.is_event_certificate",
        # "event_id.state",
        "event_id.date_begin",
        "email",
        "sale_order_state",
    )
    def get_can_send_reminder(self):
        now = datetime.now()
        for att in self:
            if (
                att.sale_order_state not in ["draft", "cancel", "done"]
                # and att.event_id.state not in ["draft", "cancel", "done"]
                and att.event_id.date_begin >= now
            ):
                can_send_reminder = not (att.name and att.email)
                if can_send_reminder and att.event_id.is_event_certificate:
                    can_send_reminder = not att.attendee_dob
                att.can_send_reminder = can_send_reminder
            else:
                att.can_send_reminder = False

    @api.model
    def _cron_send_reminder_to_complete_registration(self):
        incomplete_attendees = self.search([("can_send_reminder", "=", True)])
        so_ids = incomplete_attendees.mapped("sale_order_id")
        for order in so_ids:
            order.send_late_reg_event_notification()

    @api.model
    def cron_update_send_reminder_field_of_attendees(self):
        atts = self.search([])
        now = fields.Datetime.now()
        for att in atts:
            if (
                att.sale_order_state not in ["draft", "cancel", "done"]
                # and att.event_id.state not in ["draft", "cancel", "done"]
                and att.event_id.date_begin >= now
            ):
                can_send_reminder = not att.name
                if can_send_reminder and att.event_id.is_event_certificate:
                    can_send_reminder = not att.attendee_dob
                att.write({"can_send_reminder": can_send_reminder})
            else:
                att.write({"can_send_reminder": False})
