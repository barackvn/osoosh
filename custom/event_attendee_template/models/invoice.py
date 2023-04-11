# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Invoice(models.Model):
    _inherit = "account.move"

    certificate_ids = fields.One2many("event.certificate", "invoice_id", "Certificates")
    certificates_count = fields.Integer(
        string="# of Certificates", readonly=True, compute="_get_certificates_count"
    )


    @api.depends("certificate_ids")
    def _get_certificates_count(self):
        for invoice_id in self:
            invoice_id.certificates_count = len(invoice_id.certificate_ids)


    def action_view_event_certificates(self):
        action = self.env.ref("event_custom_4devnet.action_event_certificate")
        result = action.read()[0]
        result["context"] = {}
        certificate_ids = sum((r.certificate_ids.ids for r in self), [])
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
        pass
