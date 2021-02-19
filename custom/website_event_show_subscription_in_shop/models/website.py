# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class Website(models.Model):
    _inherit = "website"

    def sale_product_domain(self):
        # remove product event from the website content grid and list view (not removed in detail view)
        domain = super(Website, self).sale_product_domain()
        if "&" in domain:
            domain.remove("&")
        if ("event_ok", "=", False) in domain:
            domain.remove(("event_ok", "=", False))
        return domain
