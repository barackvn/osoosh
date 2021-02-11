from odoo import api, fields, models


class Event(models.Model):
    _inherit = "event.event"

    is_event_certificate = fields.Boolean(string="Has Certificate?")
    accreditation_id = fields.Many2one("event.accreditation", string="Accreditation")
    event_description = fields.Text(
        "Event Description", help="This description is used in RSS Feed."
    )
