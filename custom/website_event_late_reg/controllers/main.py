from odoo import http
from odoo.http import request


class WebsiteEvents(http.Controller):
    @http.route(
        ["/events/complete-registration"], type="http", auth="public", website=True
    )
    def website_registration_complete(self, **kwargs):
        valid = False
        sale_order = request.env["sale.order"]
        res = {}

        so_id = int(kwargs.get("id"))
        token = kwargs.get("token")

        public_partner = request.env.ref("base.public_partner")

        if so_id:
            sale_order = (
                request.env["sale.order"]
                .sudo()
                .search([("id", "=", so_id), ("state", "in", ["sale", "done"])])
            )
            if (
                sale_order
                and token
                and sale_order.event_token == token
                and sale_order.event_token_valid
            ):
                valid = True
                attendee_ids = sale_order.attendee_ids.filtered(lambda r: not r.name)
                # When the attendee_ids record is missing, fetch from event.registration table.
                if not attendee_ids:
                    domain = [("sale_order_id", "=", so_id)]
                    attendee_ids = (
                        attendee_ids.sudo()
                        .search(domain)
                        .filtered(lambda r: not r.name)
                    )
                event_ids = attendee_ids.mapped("event_id")
                for event in event_ids:
                    res[event.id] = {"event_obj": event, "tickets": {}}
                    # tickets = attendee_ids.mapped("event_ticket_id").filtered(
                    #     lambda r: r.event_id.id == event.id
                    # )
                    tickets = attendee_ids.mapped("event_ticket_id").search(
                        [("event_id", "=", event.id)]
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

    @http.route(
        ["/events/complete-registration/submit"],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def website_registration_complete_submit(self, **post):
        registrations = {}
        sale_order_id = post.get("sale_order_id")
        post.pop("sale_order_id")
        for key, value in post.items():
            att_id, field_name = key.split("-", 1)
            registrations.setdefault(att_id, {})[field_name] = value
        for att_id in registrations:
            temp_values = registrations[att_id].copy()
            answer_ids = []
            for key, value in temp_values.items():
                if key.startswith("answer_ids-"):
                    answer_ids.append([4, int(value)])
                    registrations[att_id]["answer_ids"] = answer_ids
                    registrations[att_id].pop(key)
        if "0" in registrations:
            for att_id in registrations:
                registrations[att_id]["answer_ids"] += registrations["0"]["answer_ids"]
            registrations.pop("0")
        for att_id in registrations:
            attendee = request.env["event.registration"].sudo().browse([int(att_id)])
            attendee.write(registrations[att_id])
        sale_order = request.env["sale.order"].sudo().browse([int(sale_order_id)])
        sale_order.write({"event_token": "", "event_token_expiration": False})
        return request.render("website_event_late_reg.complete_registration_submit")
