# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging

from requests import request as HTTPRequest
from requests.exceptions import HTTPError

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = "res.partner"

    eq_type_selection = [
        ("A00", "A00"),
        ("B00", "B00"),
        ("C00", "C00"),
        ("D00", "D00"),
        ("E00", "E00"),
        ("F00", "F00"),
        ("F10", "F10"),
        ("F20", "F20"),
        ("G00", "G00"),
        ("G11", "G11"),
        ("G12", "G12"),
        ("G21", "G21"),
        ("G22", "G22"),
        ("G40", "G40"),
        ("H00", "H00"),
        ("H10", "H10"),
        ("H21", "H21"),
        ("H22", "H22"),
        ("J00", "J00"),
        ("J11", "J11"),
        ("J12", "J12"),
        ("J13", "J13"),
        ("J14", "J14"),
        ("J21", "J21"),
        ("K00", "K00"),
        ("K10", "K10"),
        ("K20", "K20"),
        ("L00", "L00"),
        ("L11", "L11"),
        ("L12", "L12"),
        ("L13", "L13"),
        ("L19", "L19"),
        ("M00", "M00"),
        ("M10", "M10"),
        ("M20", "M20"),
        ("M30", "M30"),
        ("M40", "M40"),
        ("M49", "M49"),
        ("M50", "M50"),
        ("M60", "M60"),
        ("M79", "M79"),
    ]

    izo = fields.Char("IZO")
    director = fields.Char("Director")
    legal_form = fields.Char("Legal Form")
    founder_type = fields.Char("Founder Type")
    type = fields.Selection(
        selection_add=[("equipment", "Equipment"), ("founder", "Founder")]
    )
    eq_type = fields.Selection(eq_type_selection, "Type")
    eq_type_desc = fields.Char("Druh školy/zařízení")
    capacity = fields.Integer("Capacity")


    def fetch_registry_data(self, raise_exception=True):
        self.ensure_one()
        registry_parser_endpoint = (
            self.env["ir.config_parameter"].sudo().get_param("registry_parser_endpoint")
        )
        try:
            response = HTTPRequest(
                "GET", registry_parser_endpoint.replace("***", self.company_registry)
            )
            res = json.loads(response.content)
            data = res["data"]

            category_id = []

            legal_form = (
                str(data["legalForm"])
                if "legalForm" in data and data["legalForm"]
                else ""
            )
            if legal_form:
                legal_form_id = self.env["res.partner.category"].search(
                    [("name", "=", legal_form)]
                )
                if not legal_form_id:
                    legal_form_id = self.env["res.partner.category"].create(
                        {"name": legal_form}
                    )
                category_id.append([4, legal_form_id.id])

            founder_type = (
                str(data["founderType"])
                if "founderType" in data and data["founderType"]
                else ""
            )
            if founder_type:
                founder_type_id = self.env["res.partner.category"].search(
                    [("name", "=", founder_type)]
                )
                if not founder_type_id:
                    founder_type_id = self.env["res.partner.category"].create(
                        {"name": founder_type}
                    )
                category_id.append([4, founder_type_id.id])

            projects_type = (
                str(data["projects"]) if "projects" in data and data["projects"] else ""
            )
            if projects_type:
                for projects_type in data["projects"]:
                    projects_type_id = self.env["res.partner.category"].search(
                        [("name", "=", projects_type)]
                    )
                    if not projects_type_id:
                        projects_type_id = self.env["res.partner.category"].create(
                            {"name": projects_type}
                        )
                    category_id.append([4, projects_type_id.id])

            values = {
                "name": str(data["name"])
                if "name" in data and data["name"]
                else self.company_registry,
                "website": str(data["web"]) if "web" in data and data["web"] else "",
                "izo": str(data["izo"]) if "izo" in data and data["izo"] else "",
                "legal_form": legal_form,
                "founder_type": founder_type,
                "director": str(data["director"])
                if "director" in data and data["director"]
                else "",
                "email": str(data["email"][0])
                if "email" in data and data["email"]
                else "",
                "phone": str(data["phone"][0])
                if "phone" in data and data["phone"][0]
                else "",
                "mobile": str(data["phone"][1])
                if "phone" in data and len(data["phone"]) > 1 and data["phone"][1]
                else "",
            }

            if "address" in data:
                address = data["address"]
                values["zip"] = (
                    str(address["zip"]) if "zip" in address and address["zip"] else ""
                )
                values["street"] = (
                    str(address["street"])
                    if "street" in address and address["street"]
                    else ""
                )
                city = (
                    str(address["city"])
                    if "city" in address and address["city"]
                    else ""
                )
                cityPart = (
                    street(address["cityPart"])
                    if "cityPart" in address and address["cityPart"]
                    else ""
                )
                if cityPart:
                    city = city + " - " + cityPart
                values["city"] = city

            if category_id:
                values["category_id"] = category_id

            self.write(values)

            if "founder" in data:
                founder = data["founder"]

                city = (
                    str(founder["city"])
                    if "city" in founder and founder["city"]
                    else ""
                )
                cityPart = (
                    str(founder["cityPart"])
                    if "cityPart" in founder and founder["cityPart"]
                    else ""
                )
                if cityPart:
                    city = city + " - " + cityPart
                founder_values = {
                    "name": "Founder - " + str(founder["name"])
                    if "name" in founder and founder["name"]
                    else "",
                    "email": str(founder["email"])
                    if "email" in founder and founder["email"]
                    else "",
                    "zip": str(founder["zip"])
                    if "zip" in founder and founder["zip"]
                    else "",
                    "street": str(founder["street"])
                    if "street" in founder and founder["street"]
                    else "",
                    "city": city,
                    "type": "founder",
                    "parent_id": self.id,
                }
                existing_founder_address_id = self.search(
                    [("parent_id", "=", self.id), ("type", "=", "founder")]
                )
                if existing_founder_address_id:
                    existing_founder_address_id.write(founder_values)
                else:
                    self.create(founder_values)

            if "equipment" in res:
                for eq in res["equipment"]:
                    izo = str(eq["izo"]) if "izo" in eq and eq["izo"] else ""

                    city = str(eq["city"]) if "city" in eq and eq["city"] else ""
                    cityPart = (
                        str(eq["cityPart"])
                        if "cityPart" in eq and eq["cityPart"]
                        else ""
                    )
                    if cityPart:
                        city = city + " - " + cityPart

                    street2 = (
                        str(eq["numberOfDescriptive"])
                        if "numberOfDescriptive" in eq and eq["numberOfDescriptive"]
                        else ""
                    )
                    orientation_number = (
                        str(eq["orientationNumber"])
                        if "cityPart" in eq and eq["orientationNumber"]
                        else ""
                    )
                    if orientation_number:
                        street2 = street2 + "/" + orientation_number

                    category_id = []
                    eq_type = str(eq["type"]) if "street" in eq and eq["type"] else ""
                    if eq_type:
                        eq_type_id = self.env["res.partner.category"].search(
                            [("name", "=", eq_type)]
                        )
                        if not eq_type_id:
                            eq_type_id = self.env["res.partner.category"].create(
                                {"name": eq_type}
                            )
                        category_id.append([4, eq_type_id.id])

                    eq_type_desc = (
                        str(eq["kind"]) if "kind" in eq and eq["kind"] else ""
                    )
                    if eq_type_desc:
                        eq_type_desc_id = self.env["res.partner.category"].search(
                            [("name", "=", eq_type_desc)]
                        )
                        if not eq_type_desc_id:
                            eq_type_desc_id = self.env["res.partner.category"].create(
                                {"name": eq_type_desc}
                            )
                        category_id.append([4, eq_type_desc_id.id])

                    eq_values = {
                        "name": "Equipment - "
                        + (
                            str(data["name"])
                            if "name" in data and data["name"]
                            else self.company_registry
                        )
                        + " - "
                        + eq_type_desc,
                        "izo": izo,
                        "capacity": int(eq["capacity"])
                        if "capacity" in eq and eq["capacity"]
                        else "",
                        "zip": str(eq["zip"]) if "zip" in eq and eq["zip"] else "",
                        "street": str(eq["street"])
                        if "street" in eq and eq["street"]
                        else "",
                        "street2": street2,
                        "city": city,
                        "eq_type": eq_type,
                        "eq_type_desc": eq_type_desc,
                        "type": "equipment",
                        "parent_id": self.id,
                    }

                    existing_equipment_id = self.search(
                        [
                            ("parent_id", "=", self.id),
                            ("izo", "=", izo),
                            ("type", "=", "equipment"),
                        ]
                    )
                    if existing_equipment_id:
                        existing_equipment_id.write(eq_values)
                    else:
                        self.create(eq_values)

                    if category_id:
                        self.write({"category_id": category_id})
            # self.geo_localize()
            return True

        except Exception as e:
            if raise_exception:
                raise UserError("Company registry not found.")
            else:
                _logger.info("Company registry %s not found." % self.company_registry)
                _logger.info("Company fetched data %s" % res)
                return False
