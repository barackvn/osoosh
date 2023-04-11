from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    learning_description = fields.Text(string="Course Description")
    learning_blocks = fields.Text(string="Course Blocks")
    learning_hours = fields.Text(string="Course Hours")
    learning_benefit = fields.Text(string="Course Benefits")
    learning_for = fields.Text(string="Course Useful For")
    learning_results = fields.Text(string="Course Results")
    is_learning_product = fields.Boolean(string="Is a Learning Product")

    @api.model
    def create(self, vals):
        product_template_id = super(ProductTemplate, self).create(vals)
        related_vals = {}
        if vals.get("learning_description"):
            related_vals["learning_description"] = vals["learning_description"]
        if vals.get("learning_blocks"):
            related_vals["learning_blocks"] = vals["learning_blocks"]
        if vals.get("learning_hours"):
            related_vals["learning_hours"] = vals["learning_hours"]
        if vals.get("learning_benefit"):
            related_vals["learning_benefit"] = vals["learning_benefit"]
        if vals.get("learning_for"):
            related_vals["learning_for"] = vals["learning_for"]
        if vals.get("learning_results"):
            related_vals["learning_results"] = vals["learning_results"]
        if vals.get("is_learning_product"):
            related_vals["is_learning_product"] = vals["is_learning_product"]
        if related_vals:
            product_template_id.write(related_vals)
        return product_template_id

    # @api.depends('is_learning_product')
    def check_if_product_is_learning_product(self):
        p = self.env["product.product"].search(
            [("product_tmpl_id", "=", self.id), ("is_learning_product", "=", True)]
        )
        return any(prod.is_learning_product for prod in p)


# class ProductVariant(models.Model):
#     _inherit = "product.product"

#     learning_description = fields.Text("Course Description")
#     learning_blocks = fields.Text("Course Blocks")
#     learning_hours = fields.Text("Course Hours")
#     learning_benefit = fields.Text("Course Benefits")
#     learning_for = fields.Text("Course Useful For")
#     learning_results = fields.Text("Course Results")
#     is_learning_product = fields.Boolean(string="Is an Learning Product")
