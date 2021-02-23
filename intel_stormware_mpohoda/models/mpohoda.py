# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class MpohodaPaymentType(models.Model):
    _name = 'mpohoda.payment.type'

    journal_id = fields.Many2one(
        comodel_name='account.journal', 
        string='Odoo Payment Method')
    
    mpohoda_journal = fields.Char(
        string='Mpohoda Payment Method', 
        readonly=True)



class MpohodaInvoiceType(models.Model):
    _name = 'mpohoda.invoice.type'

    journal_id = fields.Many2one(
        comodel_name='account.journal', 
        string='Odoo Journal')
    
    mpohoda_journal = fields.Char(
        string='Mpohoda Journal', 
        readonly=True)




