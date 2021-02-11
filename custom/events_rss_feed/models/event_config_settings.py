from odoo import api, fields, models


class EventConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    rss_title = fields.Char(string="Title")
    rss_email = fields.Char(string="Web Master E-mail")
    rss_description = fields.Text(string="Description")


    def set_values(self):
        # rss_title = self[0].rss_title or ''
        self.env["ir.config_parameter"].sudo().set_param("rss_title", self.rss_title)
        # rss_description = self[0].rss_description or ''
        self.env["ir.config_parameter"].sudo().set_param(
            "rss_description", self.rss_description
        )
        # rss_email = self[0].rss_email or ''
        self.env["ir.config_parameter"].sudo().set_param("rss_email", self.rss_email)
        super(EventConfigSettings, self).set_values()

    @api.model
    def get_values(self):
        settings = super(EventConfigSettings, self).get_values()
        params = self.env["ir.config_parameter"].sudo()
        rss_title = params.sudo().get_param("rss_title", default="")
        rss_description = params.sudo().get_param("rss_description", default="")
        rss_email = params.sudo().get_param("rss_email", default="")
        settings["rss_title"] = rss_title
        settings["rss_description"] = rss_description
        settings["rss_email"] = rss_email
        return settings
