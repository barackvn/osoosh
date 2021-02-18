# -*- coding: utf-8 -*-

from odoo import models, fields, api
class timesheet_on_task(models.Model):
     _inherit = 'project.task'
     users_ids = fields.Many2many('res.users', 'task_users_rel','task_id', 'users_id', string="Assigned to")



