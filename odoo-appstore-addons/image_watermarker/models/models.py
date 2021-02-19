# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import models, fields, api, _
from odoo.tools.safe_eval import test_python_expr
from odoo.exceptions import ValidationError,Warning
from odoo.tools.translate import _
from odoo.addons.base.models.ir_http import IrHttp
import re

Positioning = [
    ('horizontal','Horizontal'),
    ('vertical','Vertical'),
]

WatermarkerType = [
    ('text','Text'),
    ('image','Image'),
]
HELPTextFill = _(
"""Place the text color in RGBA(R,G,B,A) format like:
(50,0,0,50)
NOTE:RGBA must be in the range of (0,255)
0<=R<=255, 0<=G<=255, 0<=B<=255, 0<=A<=255

"""
)
class BaseWatermarker(models.Model):
    _name = 'base.watermarker'
    _description = 'Base Watermarker'

    watermarker_type = fields.Selection(
        selection = WatermarkerType,
        default='text',
    )
    image = fields.Binary(
        string='Watermarker  image',
    )
    name = fields.Char(
        string = 'Name',
    )
    active = fields.Boolean(
        string = 'Active',
        default = 1
    )
    scale =  fields.Float(
        string = 'Fraction Scale',
        default=0.5,
    )
    text_fill = fields.Char(
        string = 'RGBA',
        default = '(192,192,192,250)',
        help=HELPTextFill
    )
    margin_top =   fields.Integer(
        string = 'Margin Top',
        default=20,
    )
    margin_left =   fields.Integer(
        string = 'Margin Left',
        default=20,
    )
    positioning = fields.Selection(
        selection = Positioning,
        default = 'horizontal'
    )
    @api.constrains('text_fill')
    def _check_python_text_fill(self):
        for action in self.filtered('text_fill'):
            msg = test_python_expr(expr=action.text_fill.strip(), mode="exec")
            if msg:
                raise ValidationError(msg)
    @api.constrains('scale')
    def check_fraction_scale(self):
        if self.scale>1:
            raise Warning("""The fraction scale should be less than 1.""")

class ProductWatermarker(models.Model):
    _name = 'product.watermarker'
    _inherit = 'base.watermarker'
    _description = 'Product Watermarker'

    product_ids = fields.One2many(
        comodel_name = 'product.product',
        inverse_name='watermarker_id',
    )
    
    def archive_watermark(self):
        self.active = False

   
    def activate_watermark(self):
        self.active = True
    
class ProductProduct(models.Model):
    _inherit = 'product.product'

    watermarker_id = fields.Many2one(
        comodel_name = 'product.watermarker',
        default = lambda self:self.env['product.watermarker'].search([],limit=1).id
		
    )
