# Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo import api, fields, models


# class Attendee(models.Model):
#     _inherit = "event.registration"

#     certificate_id = fields.Many2one("event.certificate", "Certificate Issued")

#     @api.multi
#     def generate_certificate(self):
#         for att in self:
#             if (
#                 not att.event_id.is_event_certificate
#                 or att.state != "done"
#                 or att.certificate_id
#             ):
#                 continue

#             invoice_id = False
#             if att.sale_order_line_id.invoice_lines:
#                 invoice_id = att.sale_order_line_id.invoice_lines[0].invoice_id
#             vals = {
#                 "certificate_product": att.sale_order_line_id.product_id.name,
#                 "certificate_reference": invoice_id.id,
#                 "certificate_name": att.partner_id.id,
#                 "certificate_attendee": att.name,
#                 "attendee_id": att.id,
#                 "certificate_dob": att.attendee_dob,
#                 "email": att.email,
#                 "certificate_place": att.event_id.address_id.id,
#                 "certificate_event": att.event_id.id,
#                 "certificate_accreditation": att.event_id.accreditation_name.id,
#                 "company_id": att.event_id.company_id.id,
#                 # 'certificate_description': i.description,
#             }
#             certicate_id = self.env["event.certificate"].create(vals)
#             att.write({"certicate_id": certicate_id.id})


# class EventCertficate(models.Model):
#     _inherit = "event.certificate"

# attendee_id = fields.Many2one(
#     "event.registration", string="Attendee Name", required=True
# )

# @api.onchange("attendee_id")
# def _onchange_attendee_id(self):
#     for r in self:
#         if r.attendee_id:
#             r.certificate_attendee = r.attendee_id.name
