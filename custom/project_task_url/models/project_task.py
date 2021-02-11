#! -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Odooveloper (BOXED, s.r.o.) All Rights Reserved
#    http://www.boxed.cz
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models

CAPACITY_JOIN_DETAIL = [
    ("dont_have_2", "Nemá prostor - 2 učastníci"),
    ("dont_have_4", "Nemá prostor - 4 učastníci"),
    ("dont_have_6", "Nemá prostor - 6 učastníků"),
    ("10_have_2", "Prostor do 10 - 2 učastníci"),
    ("10_have_4", "Prostor do 10 - 4 učastníci"),
    ("10_have_6", "Prostor do 10 - 6 učastníci"),
    ("15_have_2", "Prostor do 15 - 2 učastníci"),
    ("15_have_4", "Prostor do 15 - 4 učastníci"),
    ("15_have_6", "Prostor do 15 - 6 učastníci"),
    ("20_have_2", "Prostor do 20 - 2 učastníci"),
    ("20_have_4", "Prostor do 20 - 4 učastníci"),
    ("20_have_6", "Prostor do 20 - 6 učastníci"),
]


class ProjectTask(models.Model):
    _inherit = "project.task"

    url = fields.Char(string="URL", help="Where you can find more info on the task?")
    sale_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")
    qty_to_invoice = fields.Float(
        string="Quantity to invoice", related="sale_line_id.qty_to_invoice"
    )
    qty_invoiced = fields.Float(
        string="Quantity invoiced", related="sale_line_id.qty_invoiced"
    )
    x_capacity_join_detail = fields.Selection(
        selection=CAPACITY_JOIN_DETAIL, string="Vlastnosti"
    )
    x_date = fields.Date(string="Start Date")
    company_registry = fields.Char(
        related="company_id.company_registry", string="Company Registry"
    )
