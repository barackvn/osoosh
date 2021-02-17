from odoo import api, fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    event_id = fields.Many2one("event.event", "Related Event")

    @api.model
    def create(self, vals):
        event = super(CalendarEvent, self).create(vals)
        if event.task_id:
            event.event_id.log_meeting(event.name, event.start, event.duration)
        return event
