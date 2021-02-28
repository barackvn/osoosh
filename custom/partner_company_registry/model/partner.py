# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ICTSTUDIO (<http://www.ictstudio.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    company_registry = fields.Char(string="Company Registry")
    database_id_v9 = fields.Integer(string='Database ID V9', index=True)


class ResCompany(models.Model):
    _inherit = "res.company"

    x_acreditation = fields.Char(string="Akreditace Organizace ")


class Project(models.Model):
    _inherit = 'project.task'

    database_id_v9 = fields.Integer(string='Database ID V9', index=True)

class Template(models.Model):
    _inherit = 'product.template'

    database_id_v9 = fields.Integer(string='Database ID V9', index=True)

class Product(models.Model):
    _inherit = 'product.product'

    database_id_v9 = fields.Integer(string='Database ID V9', index=True)

