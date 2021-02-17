# See LICENSE file for full copyright and licensing details.

import urllib
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import simplejson
from odoo.http import request
from odoo import api, fields, models, _

import requests as req


class auth_oauth_provider(models.Model):
    """Class defining the configuration values of an OAuth2 provider"""

    _inherit = "auth.oauth.provider"

    secret_key = fields.Char("Secret Key")

    def oauth_token(
        self, type_grant, oauth_provider_rec, code=None, refresh_token=None
    ):
        data = dict(
            grant_type=type_grant,
            redirect_uri=self.env["ir.config_parameter"]
            .sudo()
            .get_param("web.base.url")
            + "/auth_oauth/microsoft/signin",
            client_id=oauth_provider_rec.client_id,
            client_secret=oauth_provider_rec.secret_key,
            resource="https://graph.microsoft.com/",
            code="",
        )
        if code:
            data.update({"code": code})
        elif refresh_token:
            data.update({"refresh_token": refresh_token})
        # data = urlencode(data).encode('utf-8')
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        get_res = req.post(
            oauth_provider_rec.validation_endpoint, data=data, headers=headers
        )
        # res =  simplejson.loads(urlopen(Request(oauth_provider_rec.validation_endpoint, data)).read())
        res = simplejson.loads(get_res.text)
        return res
