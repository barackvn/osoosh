# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
from datetime import date, datetime, timedelta

import pytz
from werkzeug import wrappers

from odoo import http
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class PartnerEndpoints(http.Controller):
    def validate_request(self, token):
        if token and token == request.env["ir.config_parameter"].sudo().get_param(
            "partner_endpoint_auth_token"
        ):
            return True
        return False

    def prepare_partner_data(self, partner_id):
        return {
            "id": partner_id.id,
            "company_registry": partner_id.company_registry
            if partner_id.company_registry
            else "",
            "name": partner_id.name,
            "street": partner_id.street,
            "street2": partner_id.street2 if partner_id.street2 else "",
            "city": partner_id.city if partner_id.city else "",
            "zip": partner_id.zip if partner_id.city else "",
            "country": partner_id.country_id.name if partner_id.country_id else "",
            "state": partner_id.state_id.name if partner_id.state_id else "",
            "active": partner_id.active,
            "website": partner_id.website if partner_id.website else "",
            "email": partner_id.email if partner_id.email else "",
            "phone": partner_id.phone if partner_id.phone else "",
            "mobile": partner_id.mobile if partner_id.mobile else "",
            "director": partner_id.director if partner_id.director else "",
            "write_date": partner_id.write_date.strftime(DATETIME_FORMAT),
            "partner_latitude": partner_id.partner_latitude
            if partner_id.partner_latitude
            else "",
            "partner_longitude": partner_id.partner_longitude
            if partner_id.partner_longitude
            else "",
            "categories": partner_id.category_id.mapped("name"),
        }

    @http.route("/data/partner", type="http", auth="none", methods=["POST"], csrf=False)
    def data_partner(self, **post):
        """
        Get a partner by id

        :param str token: Authentication token
        :param str id: A partner record id
        :return: json object with http response code
        """
        valid = self.validate_request(post.get("token", False))
        if not valid:
            return wrappers.Response(json.dumps({"error": "Invalid token."}), 400)
        result = {}
        partner_id = post.get("id", False)
        if partner_id:
            partner_id = (
                request.env["res.partner"]
                .sudo()
                .search([("id", "=", int(partner_id)), ("is_company", "=", True)])
            )
            if partner_id:
                result = self.prepare_partner_data(partner_id)

        return request.make_response(
            json.dumps(result), headers={"content_type": "application/json"}
        )

    @http.route(
        "/data/partners", type="http", auth="none", methods=["POST"], csrf=False
    )
    def data_partners(self, **post):
        """
        Get a list of partners

        :param str token: Authentication token
        :param str tag: Exact match of an existing tag
        :param int limit: Number of records to return
        :param int offset: Number of records to skip
        :return: json object with http response code
        """
        valid = self.validate_request(post.get("token", False))
        if not valid:
            return wrappers.Response(json.dumps({"error": "Invalid token."}), 400)
        limit = post.get("limit", 10000)
        offset = post.get("offset", 0)
        tag = post.get("tag", False)

        result = []

        search_domain = [("is_company", "=", True)]
        search_domain += [("director", "!=", "")]
        if tag:
            tag_ids = (
                request.env["res.partner.category"]
                .sudo()
                .search([("name", "=ilike", tag)])
            )
            if tag_ids:
                search_domain += [("category_id", "in", tag_ids.ids)]
            else:
                return request.make_response(
                    json.dumps({"partners": [], "pages": 0}),
                    headers={"content_type": "application/json"},
                )
        count = request.env["res.partner"].sudo().search_count(search_domain)
        pages = (count + (limit - 1)) / limit
        partner_ids = (
            request.env["res.partner"]
            .sudo()
            .search(search_domain, limit=limit, offset=offset)
        )
        for partner_id in partner_ids:
            result.append(self.prepare_partner_data(partner_id))
        return request.make_response(
            json.dumps({"partners": result, "count": count, "pages": pages}),
            headers={"content_type": "application/json"},
        )

    def prepare_event_data(self, event_id, partner_id, count_attendees=False):
        address = {}
        if event_id.address_id:
            address_id = event_id.address_id
            address = {
                "name": address_id.name,
                "street": address_id.street,
                "street2": address_id.street2 if address_id.street2 else "",
                "city": address_id.city if address_id.city else "",
                "zip": address_id.zip if address_id.city else "",
                "country": address_id.country_id.name if address_id.country_id else "",
                "state": address_id.state_id.name if address_id.state_id else "",
            }
        return {
            "id": event_id.id,
            "address": address,
            "active": event_id.active,
            "date_begin": event_id.date_begin.strftime(DATETIME_FORMAT),
            "date_end": event_id.date_end.strftime(DATETIME_FORMAT)
            if event_id.date_end
            else "",
            "state": event_id.state,
            "event_type": event_id.event_type_id.name if event_id.event_type_id else "",
            "name": event_id.name,
            "lectore": event_id.user_id.name if event_id.user_id else "",
            "template_id": event_id.sale_order_line_origin.product_id.id
            if event_id.sale_order_line_origin.product_id
            else "",
            "seats_availability": event_id.seats_availability
            if event_id.seats_availability
            else 0,
            "seats_reserved": count_attendees if count_attendees else 0,
            "organizer": event_id.organizer_id.name if event_id.organizer_id else "",
            "organizer_id": event_id.organizer_id.id if event_id.organizer_id else "",
            "is_event_certificate": event_id.is_event_certificate
            if event_id.is_event_certificate
            else "",
            "partner_id": partner_id.id if partner_id else "",
            "event_description": event_id.event_description
            if event_id.event_description
            else "",
        }

    def convert_sdt_to_utc_sdt(self, t):
        res = datetime.strptime(t[0:19], "%Y-%m-%dT%H:%M:%S")
        if t[-6] == "+":
            res += timedelta(hours=int(t[-5:-3]), minutes=int(t[-2:]))
        elif t[-6] == "-":
            res -= timedelta(hours=int(t[-5:-3]), minutes=int(t[-2:]))
        return res.strftime("%Y-%m-%d %H:%M:%S")

    @http.route("/data/course", type="http", auth="none", methods=["POST"], csrf=False)
    def data_course(self, **post):
        """
        Get an event by id

        :param str token: Authentication token
        :param str id: An event record id
        :return: json object with http response code
        """
        valid = self.validate_request(post.get("token", False))
        if not valid:
            return wrappers.Response(json.dumps({"error": "Invalid token."}), 400)
        result = {}
        event_id = post.get("id", False)
        if event_id:
            now = datetime.now()
            event_id = (
                request.env["event.event"]
                .sudo()
                .search(
                    [
                        ("id", "=", int(event_id)),
                        ("website_published", "=", True),
                        ("date_begin", ">=", now),
                    ]
                )
            )
            if event_id:
                result = self.prepare_event_data(
                    event_id, partner_id=False, count_attendees=False
                )
        return request.make_response(
            json.dumps(result), headers={"content_type": "application/json"}
        )

    @http.route("/data/courses", type="http", auth="none", methods=["POST"], csrf=False)
    def data_courses(self, **post):
        """
        Get a list of events

        :param str token: Authentication token
        :param str partner_id: A partner record id
        :param int limit: Number of records to return
        :param int offset: Number of records to skip
        :return: json object with http response code
        """
        valid = self.validate_request(post.get("token", False))
        if not valid:
            return wrappers.Response(json.dumps({"error": "Invalid token."}), 400)

        limit = post.get("limit", 20)
        offset = post.get("offset", 0)
        partner_id = post.get("partner_id", False)
        result, pages = [], 0

        now = datetime.now()
        search_domain = [("website_published", "=", True), ("date_begin", ">=", now)]
        if partner_id:
            try:
                partner_id = (
                    request.env["res.partner"]
                    .sudo()
                    .search([("id", "=", int(partner_id)), ("is_company", "=", True)])
                )
                if partner_id.sale_order_ids:
                    search_domain += [
                        ("sale_order_origin", "in", partner_id.sale_order_ids.ids)
                    ]
                    count = (
                        request.env["event.event"].sudo().search_count(search_domain)
                    )
                    pages = (count + (limit - 1)) / limit
                    event_ids = (
                        request.env["event.event"]
                        .sudo()
                        .search(search_domain, limit=limit, offset=offset)
                    )
                    for event_id in event_ids:
                        result.append(
                            self.prepare_event_data(
                                event_id, partner_id=False, count_attendees=False
                            )
                        )
            except:
                return wrappers.Response(
                    json.dumps({"error": "Invalid partner ID."}), 400
                )
        return request.make_response(
            json.dumps({"courses": result, "count": count}),
            headers={"content_type": "application/json"},
        )

    @http.route("/data/courses", type="http", auth="none", methods=["POST"], csrf=False)
    def data_courses(self, **post):
        """
        Get a list of events

        :param str token: Authentication token
        :param str partner_id: A partner record id
        :param int limit: Number of records to return
        :param int offset: Number of records to skip
        :return: json object with http response code
        """
        valid = self.validate_request(post.get("token", False))
        if not valid:
            return wrappers.Response(json.dumps({"error": "Invalid token."}), 400)

        limit = post.get("limit", 20)
        offset = post.get("offset", 0)
        partner_id = post.get("partner_id", False)
        result, pages = [], 0

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        search_domain = [("website_published", "=", True), ("date_begin", ">=", now)]
        if partner_id:
            try:
                partner_id = (
                    request.env["res.partner"]
                    .sudo()
                    .search([("id", "=", int(partner_id)), ("is_company", "=", True)])
                )
                if partner_id:
                    attendee_ids = (
                        request.env["event.registration"]
                        .sudo()
                        .search([("partner_id", "=", partner_id.id)])
                    )
                    if attendee_ids:
                        search_domain += [
                            ("id", "in", attendee_ids.mapped("event_id").ids)
                        ]
                        count = (
                            request.env["event.event"]
                            .sudo()
                            .search_count(search_domain)
                        )
                        pages = (count + (limit - 1)) / limit
                        event_ids = (
                            request.env["event.event"]
                            .sudo()
                            .search(search_domain, limit=limit, offset=offset)
                        )
                        for event_id in event_ids:
                            result.append(
                                self.prepare_event_data(
                                    event_id, partner_id=False, count_attendees=False
                                )
                            )
            except:
                return wrappers.Response(
                    json.dumps({"error": "Invalid partner ID."}), 400
                )
        return request.make_response(
            json.dumps({"courses": result, "pages": pages}),
            headers={"content_type": "application/json"},
        )

    @http.route(
        "/data/coursesall", type="http", auth="none", methods=["POST"], csrf=False
    )
    def data_coursesall(self, **post):
        """
        Get a list of events

        :param str token: Authentication token
        :param str partner_id: A partner record id
        :param int limit: Number of records to return
        :param int offset: Number of records to skip
        :return: json object with http response code
        """
        """
        Get a list of partners

        :param str token: Authentication token
        :param str tag: Exact match of an existing tag
        :param int limit: Number of records to return
        :param int offset: Number of records to skip
        :return: json object with http response code
        """
        valid = self.validate_request(post.get("token", False))
        if not valid:
            return wrappers.Response(json.dumps({"error": "Invalid token."}), 400)
        limit = post.get("limit", 10000)
        offset = post.get("offset", 0)
        count_course = 0
        result = []
        search_domain = [
            ("is_company", "=", True),
            ("director", "!=", ""),
            ("sale_order_ids", "!=", False),
        ]
        count_partners = request.env["res.partner"].sudo().search_count(search_domain)
        partner_ids = (
            request.env["res.partner"]
            .sudo()
            .search(search_domain, limit=limit, offset=offset)
        )
        for partner_id in partner_ids:
            try:
                partner_id = (
                    request.env["res.partner"]
                    .sudo()
                    .search([("id", "=", int(partner_id)), ("is_company", "=", True)])
                )
                if partner_id:
                    cr = request.env.cr
                    sql_res = """
                        SELECT cast(CONCAT(SO.partner_id::text,SOL.id::text,EVENT.id::text)as int8) as uniq_number,SO.partner_id as partner_id,PT.id, PT.name, PROJECT.analytic_account_id as project_id, AAA.name as project, (SOL.product_uom_qty - SOL.qty_invoiced) as qty, PPUBLICCAT.id as category_id, PPUBLICCAT.name as category_name, CASE WHEN EVENTREG.event_id is null THEN EVENTREG.event_id = 0 END, EVENTREG.event_id as registration_event_id, COUNT(EVENTREG.event_id) as count_registrated,EMP.id as lectore_id, EMP.name_related as lectore_name, EVENT.active as event_active, to_char(EVENT.date_begin,'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') as date_begin, to_char(EVENT.date_end,'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') as date_end, EVENT.state as state, event.event_type_id as event_type_id, EVTYPE.name as event_type_name, EVENT.seats_availability as event_seats_availability, EVENT.organizer_id as organizer_id, EVENT.is_event_certificate as is_certificated, EVENT.event_description as description, ADDRESS.id as address_id,ADDRESS.name as address_name,ADDRESS.street as address_street,ADDRESS.street2 as address_street2,ADDRESS.city as address_city,ADDRESS.zip as address_zip,ADDRESS.country_id as address_country
                        FROM sale_order_line SOL
                        LEFT JOIN sale_order SO on SO.id = SOL.order_id
                        LEFT JOIN product_product PP on PP.id = SOL.product_id
                        LEFT JOIN product_template PT on PT.id = PP.product_tmpl_id
                        LEFT JOIN project_project PROJECT on PROJECT.id = PT.project_id
                        LEFT JOIN product_public_category_product_template_rel PPUBLICCATREL on PPUBLICCATREL.product_template_id = PP.product_tmpl_id
                        LEFT JOIN product_public_category PPUBLICCAT on PPUBLICCAT.id = PPUBLICCATREL.product_public_category_id
                        LEFT JOIN event_registration EVENTREG on EVENTREG.sale_order_line_id = SOL.id
                        LEFT JOIN event_event EVENT on EVENT.id = EVENTREG.event_id
                        LEFT JOIN res_users USERS on USERS.id = EVENT.user_id
                        LEFT JOIN hr_employee EMP on EMP.id = USERS.employee_id
                        LEFT JOIN event_type EVTYPE on EVTYPE.id = EVENT.event_type_id
                        LEFT JOIN res_partner ADDRESS on ADDRESS.id = EVENT.address_id
                        LEFT JOIN account_analytic_account AAA on AAA.id = PROJECT.analytic_account_id
                        WHERE SO.partner_id = %s AND SO.state NOT IN ('draft', 'cancel', 'sent') AND PT.is_learning_product = True AND SOL.qty_invoiced < SOL.product_uom_qty AND PPUBLICCAT.parent_id = 21 AND (EVENT.date_begin >= now() OR EVENT.date_begin is NULL)
                        GROUP BY event.id,so.partner_id,PT.id,project.analytic_account_id,AAA.name,sol.product_uom_qty,sol.qty_invoiced,category_id,sol.id,eventreg.event_id,event.date_begin,EMP.id,EMP.name_related,event.active,event.date_end,event.state,event.event_type_id,evtype.name,event.seats_availability,event.organizer_id,event.is_event_certificate,event.event_description,address.id
                        ORDER BY SOL.id
                    """
                    params = [partner_id.id]
                    cr.execute(sql_res, params)
                    sql_res = cr.dictfetchall()
                    for r in sql_res:
                        count_course = count_course + 1
                        result.append(r)
            except:
                return wrappers.Response(
                    json.dumps({"error": "Invalid partner ID."}), 400
                )
        return request.make_response(
            json.dumps(
                {
                    "courses": result,
                    "searched over partners": count_partners,
                    "count_course": count_course,
                }
            ),
            headers={"content_type": "application/json"},
        )

    def prepare_project_data(self, project_id):
        return {"id": project_id.id, "name": project_id.analytic_account_id.name}

    @http.route(
        "/data/projects", type="http", auth="none", methods=["POST"], csrf=False
    )
    def data_projects(self, **post):
        """
        Get a list of events

        :param str token: Authentication token
        :param str partner_id: A partner record id
        :param int limit: Number of records to return
        :param int offset: Number of records to skip
        :return: json object with http response code
        """
        """
        Get a list of partners

        :param str token: Authentication token
        :param str tag: Exact match of an existing tag
        :param int limit: Number of records to return
        :param int offset: Number of records to skip
        :return: json object with http response code
        """
        result = []
        valid = self.validate_request(post.get("token", False))
        if not valid:
            return wrappers.Response(json.dumps({"error": "Invalid token."}), 400)
        project_ids = (
            request.env["project.project"].sudo().search([("active", "=", True)])
        )
        for project_id in project_ids:
            result.append(self.prepare_project_data(project_id))
        return request.make_response(
            json.dumps({"projects": result}),
            headers={"content_type": "application/json"},
        )
