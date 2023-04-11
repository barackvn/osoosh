from odoo import http
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.website_event_late_reg.controllers.main import WebsiteEvents as LateReg
from odoo.http import request


class ExtendedWebsiteEventController(WebsiteEventController):
    def _process_registration_details(self, details):
        registrations = super(
            ExtendedWebsiteEventController, self
        )._process_registration_details(details)
        for registration in registrations:
            if not registration.get("attendee_dob"):
                registration["attendee_dob"] = None
            answer_ids = [
                [4, int(value)]
                for key, value in registration.items()
                if key.startswith("answer_ids-")
            ]
            registration["answer_ids"] = answer_ids
        return registrations


class ExtendedLateReg(LateReg):
    @http.route()
    def website_registration_complete(self, **kwargs):
        valid = False
        sale_order = request.env["sale.order"]
        res = {}

        so_id = kwargs.get("id")
        token = kwargs.get("token")

        if so_id:
            sale_order = (
                request.env["sale.order"]
                .sudo()
                .search([("id", "=", int(so_id)), ("state", "in", ["sale", "done"])])
            )
            if (
                sale_order
                and token
                and sale_order.event_token == token
                and sale_order.event_token_valid
            ):
                valid = True
                attendee_ids = sale_order.attendee_ids
                event_ids = attendee_ids.mapped("event_id")
                for event in event_ids:
                    res[event.id] = {"event_obj": event, "tickets": {}}
                    tickets = attendee_ids.mapped("event_ticket_id").filtered(
                        lambda r: r.event_id.id == event.id
                    )
                    for ticket in tickets:
                        res[event.id]["tickets"][ticket.id] = {
                            "ticket_obj": ticket,
                            "attendees": [],
                        }
                        att_filtered = attendee_ids.filtered(
                            lambda r: r.event_id.id == event.id
                            and r.event_ticket_id.id == ticket.id
                        )
                        for a in att_filtered:
                            res[event.id]["tickets"][ticket.id]["attendees"].append(a)
        return request.render(
            "website_event_late_reg.complete_registration",
            {"valid": valid, "res": res, "sale_order": sale_order},
        )

    @http.route()
    def website_registration_complete_submit(self, **post):
        registrations = {}
        post.pop("sale_order_id")
        for key, value in post.items():
            att_id, field_name = key.split("-", 1)
            registrations.setdefault(att_id, {})[field_name] = value
        for att_id in registrations:
            if (
                "attendee_dob" in registrations[att_id]
                and not registrations[att_id]["attendee_dob"]
            ):
                registrations[att_id]["attendee_dob"] = None
            temp_values = registrations[att_id].copy()
            answer_ids = []
            for key, value in temp_values.items():
                if key.startswith("answer_ids-"):
                    answer_ids.append([4, int(value)])
                    registrations[att_id]["answer_ids"] = answer_ids
                    registrations[att_id].pop(key)
        if "0" in registrations:
            for att_id in registrations:
                if "answer_ids" in registrations[att_id]:
                    registrations[att_id]["answer_ids"] += registrations["0"][
                        "answer_ids"
                    ]
            registrations.pop("0")
        for att_id in registrations:
            attendee = request.env["event.registration"].sudo().browse([int(att_id)])
            attendee.write(registrations[att_id])
        return request.render("website_event_late_reg.complete_registration_submit")
