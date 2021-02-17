# ©  2016 BOXED, s.r.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json
import logging
import os
import sys
# from cgi import escape, parse_qs

from odoo import _, api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

try:
    from ares_util.ares import call_ares
except ImportError:
    _logger.debug("Cannot import call_ares method from python stdnum.")


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_ares_data(self, company_registry):
        res = {}

        result = call_ares(company_registry)
        if not result:
            raise ValidationError(_("The partner is not listed on ARES Webservice."))

        company = result.get("legal")
        address = result.get("address")

        if company.get("company_vat_id"):
            res["vat"] = company.get("company_vat_id")

        if company.get("company_name"):
            res["name"] = company.get("company_name")

        if address.get("zip_code"):
            res["zip"] = address.get("zip_code")

        if address.get("street"):
            res["street"] = address.get("street")

        if address.get("city"):
            res["city"] = address.get("city")

        # Get country by country code
        # country = self.env['res.country'].search(
        #    [('code', 'ilike', vat_country)])
        # if country:
        #    res['country_id'] = country[0].id
        return res


    def company_registry_change(self, value):
        res = super(ResPartner, self).company_registry_change(value)
        # Update fields with the values available in the upper method
        # Skip required name error
        with self.env.do_in_onchange():
            if value:
                result = self._get_ares_data(value)
                res["value"].update(result)
        return res


    def get_ares_data_from_crn(self):
        if self.company_registry:
            res = self._get_ares_data(self.company_registry)
            self.update(res)
