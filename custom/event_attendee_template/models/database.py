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

class Event(models.Model):
    _inherit = 'event.event'
    
    database_id_v9 = fields.Integer(string='Database ID V9', index=True)

class EventReg(models.Model):
    _inherit = 'event.registration'
    
    database_id_v9 = fields.Integer(string='Database ID V9', index=True)

class EventCer(models.Model):
    _inherit = 'event.certificate'
    
    database_id_v9 = fields.Integer(string='Database ID V9', index=True)

class EventAcc(models.Model):
    _inherit = 'event.accreditation'
    
    database_id_v9 = fields.Integer(string='Database ID V9', index=True)
