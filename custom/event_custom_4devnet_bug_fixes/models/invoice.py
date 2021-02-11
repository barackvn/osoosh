# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


# class Invoice(models.Model):
#     _inherit = "account.invoice"

# @api.multi
# def invoice_validate(self):
#     for invoice in self:
#         if invoice.type in ("in_invoice", "in_refund") and invoice.reference:
#             if self.search(
#                 [
#                     ("type", "=", invoice.type),
#                     ("reference", "=", invoice.reference),
#                     ("company_id", "=", invoice.company_id.id),
#                     (
#                         "commercial_partner_id",
#                         "=",
#                         invoice.commercial_partner_id.id,
#                     ),
#                     ("id", "!=", invoice.id),
#                 ]
#             ):
#                 raise UserError(
#                     _(
#                         "Duplicated vendor reference detected. You probably encoded twice the same vendor bill/refund."
#                     )
#                 )
#     return self.write({"state": "open"})

# @api.multi
# def generate_certificate(self):
#     for invoice in self:
#         sale_line_ids = self.env["sale.order.line"]
#         for line in invoice.invoice_line_ids:
#             for sale_line in line.sale_line_ids:
#                 sale_line_ids |= sale_line

#         attendees = self.env["event.registration"].search(
#             [("sale_order_line_id", "in", sale_line_ids.ids)]
#         )

#         for att in attendees:
#             if att.state == "open":
#                 att.button_reg_close()

#         for att in attendees:
#             att.generate_certificate()

#         invoice.write({"certificate_gen": True})
