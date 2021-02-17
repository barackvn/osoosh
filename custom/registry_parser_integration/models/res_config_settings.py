# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    registry_parser_endpoint = fields.Char(
        string="Registry Endpoint",
        help="Endpoint for the registry parser where ICO is replaced by ***",
    )


    def set_values(self):
        super(ResConfigSettings, self).set_values()
        registry_parser_endpoint = self.registry_parser_endpoint or ""
        self.env["ir.config_parameter"].sudo().set_param(
            "registry_parser_endpoint", registry_parser_endpoint
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env["ir.config_parameter"].sudo()
        registry_parser_endpoint = params.sudo().get_param(
            "registry_parser_endpoint", default=""
        )
        res.update(registry_parser_endpoint=registry_parser_endpoint)
        return res
