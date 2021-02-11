# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Events(models.Model):
    _inherit = "event.event"

    joined_task_ids = fields.Many2many(
        "project.task",
        "event_task_join_rel",
        "event_id",
        "task_id",
        string="Joined Tasks",
    )
