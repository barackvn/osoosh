from odoo import api, fields, models


class Attendee(models.Model):
    _inherit = "event.registration"

    @api.model
    def create(self, vals):
        """set attendee_dob to none if it has not passed value"""
        if not vals.get("attendee_dob"):
            vals.update(attendee_dob=None)
        return super(Attendee, self).create(vals)

    attendee_dob = fields.Date(string="Date of Birth")
    certificate_ids = fields.One2many(
        "event.certificate", "attendee_id", string="Certificate"
    )
    certificate_count = fields.Integer(
        string="# of Certificates", compute="_get_certificate_count"
    )
    certificate_id = fields.Many2one("event.certificate", "Certificate Issued")


    @api.depends("certificate_ids")
    def _get_certificate_count(self):
        for att_id in self:
            att_id.certificate_count = len(att_id.certificate_ids)


    def action_view_event_certificate(self):
        action = self.env.ref("event_custom_4devnet.action_event_certificate")
        result = action.read()[0]
        # override the context to get rid of the default filtering on picking type
        result["context"] = {}
        certificate_ids = sum([r.certificate_ids.ids for r in self], [])
        # choose the view_mode accordingly
        if len(certificate_ids) > 1:
            result["domain"] = (
                "[('id','in',[" + ",".join(map(str, certificate_ids)) + "])]"
            )
        elif len(certificate_ids) == 1:
            res = self.env.ref(
                "event_custom_4devnet.view_event_certificate_form", False
            )
            result["views"] = [(res and res.id or False, "form")]
            result["res_id"] = certificate_ids and certificate_ids[0] or False
        return result


    def generate_event_certificates(self):
        for att_id in self:
            if not att_id.certificate_ids and att_id.event_id.is_event_certificate:
                self.env["event.certificate"].create({"attendee_id": att_id.id})

    @api.model
    def generate_event_certificates_by_so_lines(self, so_line_ids):
        cert_ids, attachment_ids = False, False
        att_ids = self.search([("sale_order_line_id", "in", so_line_ids)])
        att_ids = att_ids.filtered(lambda r: r.event_id.is_event_certificate)
        if att_ids:
            att_ids.generate_event_certificates()
            cert_ids = att_ids.mapped("certificate_ids")
            for c in cert_ids:
                self.env["ir.actions.report"].get_pdf(
                    c.ids, "event_custom_4devnet.report_certificate"
                )
            attachment_ids = self.env["ir.attachment"].search(
                [
                    ("res_model", "in", ["event.certificate"]),
                    ("res_id", "in", cert_ids.ids),
                ]
            )
        return cert_ids, attachment_ids


    def generate_certificate(self):
        for att in self:
            if (
                not att.event_id.is_event_certificate
                or att.state != "done"
                or att.certificate_id
            ):
                continue

            invoice_id = False
            if att.sale_order_line_id.invoice_lines:
                invoice_id = att.sale_order_line_id.invoice_lines[0].invoice_id
            vals = {
                "certificate_product": att.sale_order_line_id.product_id.name,
                "certificate_reference": invoice_id.id,
                "certificate_name": att.partner_id.id,
                "certificate_attendee": att.name,
                "attendee_id": att.id,
                "certificate_dob": att.attendee_dob,
                "email": att.email,
                "certificate_place": att.event_id.address_id.id,
                "certificate_event": att.event_id.id,
                "certificate_accreditation": att.event_id.accreditation_name.id,
                "company_id": att.event_id.company_id.id,
                # 'certificate_description': i.description,
            }
            certicate_id = self.env["event.certificate"].create(vals)
            att.write({"certicate_id": certicate_id.id})
