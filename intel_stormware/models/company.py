# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class res_company(models.Model):
    _inherit = 'res.company'

    is_vat_payer = fields.Boolean(
        string='Is VAT Payer?', 
        readonly=False)
    
    mserver_port = fields.Integer(
        string='mServer Port', 
        digits=(4,0), 
        default=1000,
        readonly=False)
    
    mserver_user = fields.Char(
        string='mServer User',
        readonly=False)
    
    mserver_password = fields.Char(
        string='mServer Password',
        readonly=False)
    
    # Map payment types to mpohoda (list ea active payment method at odoo and map it into selected mpohoda types, list of mpohoda types is with request bellow)
# Chose invoice serie (list of mpohoda invoice series and select what is for creating invoices and map it info invoice series at odoo)
# Chose credit note serie (list of mpohoda invoice series and select what is for creating credit notes map it info invoice series at odoo)
# Chose proformaInvoice serie (list of mpohoda invoice series and select what is for creating credit notes map it info proforma invoice series at odoo)
# Creation atuomaticaly setting (select on what action will be sync done)
# Store documents on application (chose if PDF documents will be stored at server) (bolean)
# Store synced document and response to odoo
     
    mail_template_id = fields.Many2one(
        comodel_name='mail.template',
        string='Email template',
        help='Email template for sending invoices (select email template to send invoice)',
        readonly=False)
    
    mserver_document_path = fields.Text(
        string='mServer Document Path',
        size=255)
    # Trasnfered VAT PDP (select of product type what is needed for for PDP)
    # transferred_vat_pdp = fields.Many2one(comodel='product.categ')
    
    

