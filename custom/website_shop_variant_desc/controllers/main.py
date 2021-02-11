# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import http
from openerp.http import request


class WebsiteVariant(http.Controller):
    @http.route("/request-quote", type="json", auth="public", website=True)
    def request_quote(self, values):
        product = request.env["product.product"].search(
            [("id", "=", int(values["product_id"]))]
        )
        lead = {"name": product.display_name, "description": values.get("message")}
        if request.uid != request.website.user_id.id:
            lead["partner_id"] = request.env.user.partner_id.id
        else:
            lead["email_from"] = values.get("email")
            lead["contact_name"] = values.get("name")
            lead["phone"] = values.get("contact_number")
        request.env["crm.lead"].sudo().create(lead)
        return True
