from odoo import api, fields, models


class CertificateTemplateSetting(models.TransientModel):
    _name = "certificate.template.setting"
    _inherit = "res.config.settings"

    def _get_about_us(self, context=None):
        cr = self.env.cr
        uid = self.env.user.id
        cr.execute("select max(id) from certificate_template_setting")
        if abts := cr.fetchone():
            req_id = abts[0]
            return self.browse(cr, uid, req_id, context=context).template
        else:
            return ""

    template = fields.Html(string="Certificate Template", default=_get_about_us)
