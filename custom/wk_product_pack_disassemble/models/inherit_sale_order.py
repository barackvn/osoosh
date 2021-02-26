# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
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


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_product_lines_from_pack(self, pack_line):
        pack_product = pack_line.product_id
        if pack_product.wk_product_pack:
            for prod in pack_product.wk_product_pack:

                # Update description of Sale Order Line
                name = prod.product_id.name_get()[0][1]
                if prod.product_id.description_sale:
                    name += "\n" + prod.product_id.description_sale
                name = (
                    "Item disassembled from " + pack_line.product_id.name + "\n" + name
                )

                # Order line values
                values = {
                    "product_id": prod.product_id.id,
                    "name": name,
                    "product_uom_qty": prod.product_quantity
                    * pack_line.product_uom_qty,
                    "order_id": pack_line.order_id.id,
                    "product_uom": prod.uom_id.id,
                    "price_unit": prod.wk_price,
                    "discount": pack_line.discount or 0.0,
                    "customer_lead": prod.product_id.sale_delay,
                    "tax_id": [(6, 0, prod.product_id.taxes_id.ids)],
                }
                try:
                    self.env["sale.order.line"].sudo().create(values)
                except Exception as e:
                    raise UserError(_("Error :" + str(e)))
        return True

    def check_sol_contains_service_products_pack(self, order_line):
        product_obj = order_line.product_id
        if product_obj.is_pack and len(
            product_obj.wk_product_pack.filtered(
                lambda rec: rec.product_id.type == "service"
            )
        ):
            return True
        else:
            return False


    def action_disassemble_pack(self):
        for rec in self:
            so_pack_line_ids = rec.order_line.filtered(
                lambda line: self.check_sol_contains_service_products_pack(line) == True
            )
            if so_pack_line_ids:
                for pack_line in so_pack_line_ids:
                    rec._create_product_lines_from_pack(pack_line)
                    pack_line.unlink()


    def action_confirm(self):
        self.action_disassemble_pack()
        return super(SaleOrder, self).action_confirm()
