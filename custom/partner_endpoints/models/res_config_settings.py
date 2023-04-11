# Part of Odoo. See LICENSE file for full copyright and licensing details.

import random

from odoo import api, fields, models


class BaseConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_endpoint_auth_token = fields.Char(
        string="Partner Endpoints Auth Token",
        help="Token for authenticating partner endpoint requests",
    )


    def set_values(self):
        res = super(BaseConfigSettings, self).set_values()
        partner_endpoint_auth_token = self.partner_endpoint_auth_token
        self.env["ir.config_parameter"].sudo().set_param(
            "partner_endpoint_auth_token", partner_endpoint_auth_token
        )
        return res

    @api.model
    def get_values(self):
        res = super(BaseConfigSettings, self).get_values()
        params = self.env["ir.config_parameter"].sudo()
        partner_endpoint_auth_token = params.sudo().get_param(
            "partner_endpoint_auth_token", default=""
        )
        res.update(partner_endpoint_auth_token=partner_endpoint_auth_token)
        return res


    def generate_new_endpoint_token(self):
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        token = "".join(random.SystemRandom().choice(chars) for _ in xrange(20))
        self.env["ir.config_parameter"].sudo().set_param(
            "partner_endpoint_auth_token", token
        )
