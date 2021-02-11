from odoo import fields, models


class Task(models.Model):
    _inherit = "project.task"

    company_registry = fields.Char(
        string="Company Registry", related="partner_id.company_registry"
    )
