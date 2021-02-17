from odoo import fields, models


class Event(models.Model):
    _inherit = "event.event"

    task_id = fields.Many2one("project.task", "Source Task")
