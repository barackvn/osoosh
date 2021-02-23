# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class AccountMove(models.Model):
    _inherit = 'account.move'

    #mpohoda