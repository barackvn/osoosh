# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    description_variant = fields.Text(
        "Variant Description", related="product_variant_ids.description_variant"
    )
    qv_description_variant = fields.Text(
        "Quickview Variant Description",
        related="product_variant_ids.qv_description_variant",
    )
    # @api.model
    # def create(self, vals):
    #     product_template_id = super(ProductTemplate, self).create(vals)
    #     related_vals = {}
    #     if vals.get("description_variant"):
    #         related_vals = {"description_variant": vals.get("description_variant")}
    #     if vals.get("qv_description_variant"):
    #         related_vals = {
    #             "qv_description_variant": vals.get("qv_description_variant")
    #         }
    #         res.write(related_vals)
    #     return product_template_id


class ProductVariant(models.Model):
    _inherit = "product.product"

    description_variant = fields.Text("Variant Description")
    qv_description_variant = fields.Text("Quickview Variant Description")
