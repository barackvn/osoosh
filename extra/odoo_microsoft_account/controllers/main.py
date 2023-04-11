# See LICENSE file for full copyright and licensing details.

import logging
import json
import odoo

# import httplib
from http import client as httplib
import simplejson
import werkzeug.utils
from odoo import http
from odoo import SUPERUSER_ID
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.auth_oauth.controllers.main import OAuthLogin as Home
from odoo.addons.web.controllers.main import set_cookie_and_redirect, login_and_redirect
from odoo.addons.auth_oauth.controllers.main import fragment_to_query_string, OAuthLogin

_logger = logging.getLogger(__name__)


class OAuthLogin(Home):
    def list_providers(self):
        try:
            providers = (
                request.env["auth.oauth.provider"]
                .sudo()
                .search_read([("enabled", "=", True)])
            )
        except Exception:
            providers = []
        provider_microsoft = request.env.ref(
            "odoo_microsoft_account.provider_microsoft"
        )
        base_url = request.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for provider in providers:
            if provider.get("id") == provider_microsoft.id:
                return_url = f"{base_url}/auth_oauth/microsoft/signin"
                params = dict(
                    client_id=provider["client_id"],
                    response_type="code",
                    redirect_uri=return_url,
                )
            else:
                return_url = f"{base_url}/auth_oauth/signin"
                state = self.get_state(provider)
                params = dict(
                    response_type="token",
                    client_id=provider["client_id"],
                    redirect_uri=return_url,
                    scope=provider["scope"],
                    state=json.dumps(state),
                )
            provider[
                "auth_link"
            ] = f'{provider["auth_endpoint"]}?{werkzeug.url_encode(params)}'
        return providers


class OAuthController(http.Controller):
    @http.route(
        "/auth_oauth/microsoft/signin",
        type="http",
        auth="none",
        csrf=False,
        website=True,
    )
    def microsoft_signin(self, **kw):
        pool = request.env
        root_url = (
            request.env["ir.config_parameter"].sudo().get_param("web.base.url") + "/"
        )
        oauth_provider_rec = (
            pool["ir.model.data"]
            .sudo()
            .get_object_reference("odoo_microsoft_account", "provider_microsoft")[1]
        )
        provider = pool["auth.oauth.provider"].sudo().browse(oauth_provider_rec)
        authorization_data = (
            pool["auth.oauth.provider"]
            .sudo()
            .oauth_token(
                "authorization_code", provider, kw.get("code"), refresh_token=None
            )
        )
        access_token = authorization_data.get("access_token")
        resource = authorization_data.get("resource")
        id_token = authorization_data.get("id_token")
        expires_in = authorization_data.get("expires_in")
        token_type = authorization_data.get("token_type")
        refresh_token = authorization_data.get("refresh_token")
        scope = authorization_data.get("scope")
        not_before = authorization_data.get("not_before")
        expires_on = authorization_data.get("expires_on")
        mail = ""
        user_id = None
        displayName = ""
        try:
            import requests

            # conn = httplib.HTTPSConnection(provider.data_endpoint)
            # conn.request("GET", "/v1.0/me", "",
            # {'Authorization': access_token, 'Accept': 'application/json'})
            # response = conn.getresponse()
            # data = simplejson.loads(response.read())
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }

            data = requests.get(provider.data_endpoint, headers=headers)
            data = simplejson.loads(data.text)
            displayName = data.get("displayName")
            givenName = data.get("givenName")
            mail = data.get("userPrincipalName")
            mobilePhone = data.get("mobilePhone")
            surname = data.get("surname")
            user_id = data.get("id")
            userPrincipalName = data.get("userPrincipalName")
            conn.close()
        except Exception as e:
            pass

        try:
            credentials = (
                pool["res.users"]
                .sudo()
                .microsoft_auth_oauth(
                    provider.id,
                    {
                        "access_token": access_token,
                        "user_id": user_id,
                        "email": mail,
                        "name": displayName,
                        "microsoft_refresh_token": refresh_token,
                    },
                )
            )
            request.cr.commit()
            return login_and_redirect(*credentials, redirect_url=f"{root_url}web?")
        except AttributeError:
            # auth_signup is not installed
            _logger.error(
                f"auth_signup not installed on database {request.cr.dbname}: oauth sign up cancelled."
            )
            url = "/web/login?oauth_error=1"
        except odoo.exceptions.AccessDenied:
            # oauth credentials not valid, user could be on a temporary session
            _logger.info(
                "OAuth2: access denied, redirect to main page in case a valid session exists, without setting cookies"
            )
            url = "/web/login?oauth_error=3"
            redirect = werkzeug.utils.redirect(url, 303)
            redirect.autocorrect_location_header = False
            return redirect
        except Exception as e:
            # signup error
            _logger.exception(f"OAuth2: {str(e)}")
            url = "web/login?oauth_error=2"
        return set_cookie_and_redirect(root_url + url)
