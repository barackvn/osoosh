from odoo import http
from odoo.exceptions import _logger
from odoo.addons.website_event_cert_shop.controllers.main import (
    ExtendedLateReg,
    ExtendedWebsiteEventController,
)
from odoo.http import request
import re


class AttTemplateWebsiteEvent(ExtendedWebsiteEventController):
    def _process_registration_details(self, details):
        return super(
            ExtendedWebsiteEventController, self
        )._process_registration_details(details)


class AttTemplateLateReg(ExtendedLateReg):
    @http.route()
    def website_registration_complete(self, **kwargs):
        valid = False
        sale_order_lines = request.env["sale.order.line"]
        sale_order = request.env["sale.order"]
        res = {}

        so_id = request.params.get("id")
        token = request.params.get("token")

        if so_id:
            sale_order = (
                request.env["sale.order"]
                .sudo()
                .search(
                    [
                        ("id", "=", int(so_id)),
                        ("state", "in", ["sale", "done", "in_progress"]),
                    ]
                )
            )
            if (
                sale_order
                and token
                and sale_order.event_token == token
                and sale_order.event_token_valid
            ):
                valid = True
                # Get attendee records that are not related to a learning product
                all_attendee_ids = sale_order.attendee_ids
                attendee_ids = all_attendee_ids.filtered(
                    lambda a: not a.sale_order_line_id.product_id.product_tmpl_id.is_learning_product
                )
                # attendee_events = attendee_ids.mapped("event_id")
                _logger.info(
                    f"Available Events:{all_attendee_ids.ids} - {all_attendee_ids.mapped('event_id')}"
                )
                for event in sale_order.order_line.mapped('product_id.event_template_id'):
                    res[event.id] = {"event_obj": event, "tickets": {}}
                    tickets = attendee_ids.mapped("event_ticket_id").filtered(
                        lambda r: r.event_id.id == event.id
                    )
                    for ticket in tickets:
                        res[event.id]["tickets"][ticket.id] = {
                            "ticket_obj": ticket,
                            "attendees": event.registration_ids,
                        }
                _logger.info(f"Processed Available Events:{all_attendee_ids.ids} - {res}")
                        # learning_order_line_ids = sale_order.order_line.filtered(
                        #     lambda l: l.product_id.product_tmpl_id.is_learning_product
                        # )

                        # for l in learning_order_line_ids:
                        #     res["learning-so-line-id--" + str(l.id)] = {
                        #         "event_obj": l.product_id.event_template_id,
                        #         "tickets": {
                        #             l.product_id.ticket_id.id: {
                        #                 "ticket_obj": l.product_id.ticket_id,
                        #                 "attendees": all_attendee_ids.filtered(
                        #                     lambda a: a.is_a_template
                        #                     and a.sale_order_line_id.id == l.id
                        #                 ),
                        #             }
                        #         },
                        #     }
        return request.render(
            "website_event_late_reg.complete_registration",
            {"valid": valid, "res": res, "sale_order": sale_order},
        )

    @http.route()
    def website_registration_complete_submit(self, **post):
        registrations = {}
        sale_order_id = post.get("sale_order_id")
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
        sale_order = request.env["sale.order"].sudo().browse([int(sale_order_id)])
        return request.render("website_event_late_reg.complete_registration_submit")
