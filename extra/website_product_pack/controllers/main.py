# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class WebsiteStock(http.Controller):
    @http.route("/website/product_pack/", type="json", auth="public", website=True)
    def product_pack(self, id, *args, **kwargs):
        product_id = int(id)
        record = self.env["product.product"].sudo().browse(product_id).product_tmpl_id
        return record.image
