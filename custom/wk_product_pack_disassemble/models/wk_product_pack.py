# -*- coding: utf-8 -*-
#################################################################################
# Author	  : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProductPack(models.Model):
    _inherit = "product.pack"

    wk_price = fields.Float(string="Price")


    @api.onchange("product_id")
    def _update_wk_price(self):
        self.wk_price = self.product_id.lst_price if self.product_id else 0.0


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def compute_discounted_pack_price(self):
        for product in self:
            product.p_has_discounted_amount = False
            product.pack_products_total_price = 0
            product.pack_products_current_price = 0
            if product.is_pack:
                price = 0
                price1 = 0
                for prod in product.wk_product_pack:
                    price = price + prod.product_id.lst_price * prod.product_quantity
                    price1 = price1 + prod.wk_price * prod.product_quantity
                rem_price = price - product.lst_price
                product.pack_products_total_price = price
                product.pack_products_current_price = price1
                if rem_price <= 0:
                    product.p_has_discounted_amount = True

    p_has_discounted_amount = fields.Boolean(
        compute="compute_discounted_pack_price", string="Remaning price"
    )
    pack_products_total_price = fields.Float(
        compute="compute_discounted_pack_price",
        string="Total Actual Price",
        help="Shows total actual price using the actual price of the products in pack.",
    )
    pack_products_current_price = fields.Float(
        compute="compute_discounted_pack_price",
        string="Total Product Price",
        help="Shows total price using the current price of the products in pack.",
    )
