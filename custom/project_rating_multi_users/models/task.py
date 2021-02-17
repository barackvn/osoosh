# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Task(models.Model):
    _inherit = "project.task"


    def write(self, values):
        if "stage_id" in values and values.get("stage_id"):
            template = (
                self.env["project.task.type"]
                .browse(values.get("stage_id"))
                .rating_template_id
            )
            if template and self.users_id:
                rated_partner_id = self.users_id[0].partner_id
                partner_id = self.partner_id
                if partner_id and rated_partner_id:
                    self.rating_send_request(template, partner_id, rated_partner_id)
        return super(Task, self).write(values)
