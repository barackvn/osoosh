from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"


    def onchange_template_id(self, template_id, composition_mode, model, res_id):
        values = super(MailComposeMessage, self).onchange_template_id(
            template_id, composition_mode, model, res_id
        )
        if model == "account.move":
            invoice_id = self.env["account.move"].browse([res_id])
            if cert_attachment_ids := invoice_id.generate_event_certificates():
                values["value"]["attachment_ids"].extend(cert_attachment_ids.ids)
        return values
