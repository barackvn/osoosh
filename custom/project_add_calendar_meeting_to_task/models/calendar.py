# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    task_id = fields.Many2one("project.task", "Related Task")

    @api.model
    def create(self, vals):
        event = super(CalendarEvent, self).create(vals)
        if event.task_id:
            event.task_id.log_meeting(event.name, event.start, event.duration)
        return event
