# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    auth_oauth_microsoft_enabled = fields.Boolean(
        string="Allow users to sign in with Microsoft"
    )
    auth_oauth_microsoft_client_id = fields.Char(string="MicrosoftClient ID")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        google_provider = self.env.ref(
            "odoo_microsoft_account.provider_microsoft", False
        )
        res.update(
            auth_oauth_microsoft_enabled=google_provider.enabled,
            auth_oauth_microsoft_client_id=google_provider.client_id,
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        microsoft_provider = self.env.ref(
            "odoo_microsoft_account.provider_microsoft", False
        )
        microsoft_provider.write(
            {
                "enabled": self.auth_oauth_microsoft_enabled,
                "client_id": self.auth_oauth_microsoft_client_id,
            }
        )
