import json

import werkzeug

from odoo import SUPERUSER_ID, http, tools
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.http import request


class WebsiteEventController(WebsiteEventController):
    @http.route(
        ['/event/<model("event.event"):event>/registration/new'],
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def registration_new(self, event, **post):
        tickets = self._process_tickets_details(post)
        request.session["event_id"] = event.id
        question = event.question_ids
        return (
            request.env["ir.ui.view"].render_template(
                "website_event.registration_attendee_details",
                {"tickets": tickets, "event": event[0], "question": question},
            )
            if tickets
            else False
        )

    def _process_registration_details(self, details):
        """ Process data posted from the attendee details form. """
        #        registrations = super(website_event, self)._process_registration_details(details)
        cr, uid, context, event_ids = request.cr, request.uid, request.context, []
        registrations = {}
        global_values = {}
        for key, value in details.items():
            if key in ["events", "_event_id"]:
                continue
            counter, field_name = key.split("-", 1)
            if counter == "0":
                global_values[field_name] = value
            else:
                registrations.setdefault(counter, {})[field_name] = value
        for key, value in global_values.items():
            for registration in registrations.values():
                registration[key] = value
        registrations = registrations.values()
        for registration in registrations:
            vals = {
                "name": registration.get("name"),
                "email": registration.get("email"),
                "phone": registration.get("phone"),
                "event_id": int(request.session.get("event_id")),
            }
            attendee_id = request.env["event.registration"].sudo().create(vals)
            question_ids = []
            answ_ids = []
            value = ""
            for key, value in registration.items():
                if key.startswith("answer_ids-"):
                    que_id = key.split("-")
                    que_ids = que_id[1]
                    que_data = request.env["event.question"].browse([int(que_ids)])
                    value = value
                    ans_data = request.env["event.answer"].browse([int(value)])
                    value = ans_data.name
                    answ_data = {
                        "title": que_data.title,
                        "ans": value,
                        "registration_id": attendee_id.id,
                    }
                    question_ids = (
                        request.env["event.question.new"].sudo().create(answ_data)
                    )
                if key.startswith("answer_id-"):
                    que_id = key.split("-")
                    que_ids = que_id[1]
                    que_data = (
                        request.env["event.question"].sudo().browse([int(que_ids)])
                    )
                    value = value

                    answ_data = {
                        "title": que_data.title,
                        "ans": value,
                        "registration_id": attendee_id,
                    }
                    question_ids = request.env["event.question.new"].create(answ_data)
            registration["questin_ids"] = [question_ids]
            registration["attendees"] = [attendee_id]
        return registrations

    @http.route(
        [
            """/event/<model("event.event", "[('website_id', 'in', (False, current_website_id))]"):event>/registration/confirm"""
        ],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def registration_confirm(self, event, **post):

        if not event.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        Attendees = request.env["event.registration"]
        registrations = self._process_registration_details(post)

        for registration in registrations:
            registration["event_id"] = int(event)
            # Attendees = Attendees.sudo().create(
            # Attendees._prepare_attendee_values(registration))
            for reg in registration.get("attendees"):
                Attendees += reg

        urls = event._get_event_resource_urls(Attendees.ids)
        # return request.render("website_event.registration_complete", {
        #     'attendees': Attendees.sudo(),
        #     'event': event,
        #     'google_url': urls.get('google_url'),
        #     'iCal_url': urls.get('iCal_url')
        # })

        event = request.env["event.event"].browse(event)
        template = f"/page/confirm_reg/{Attendees[0].sudo().id}"
        return werkzeug.utils.redirect(template)

    # @http.route(
    #     ["/event/registration/confirm"],
    #     type="http",
    #     auth="public",
    #     methods=["POST"],
    #     website=True,
    # )
    # def registration_confirm(self, **post):
    #     # cr, uid, context = request.cr, request.uid, request.context
    #     Registration = request.env["event.registration"]
    #     event = int(post.get("events"))
    #     registrations = self._process_registration_details(post)

    #     registration_ids = []
    #     for registration in registrations:
    #         registration["event_id"] = event
    #     attendees = Registration.browse(registration.get("attendees"))
    #     event = request.env["event.event"].browse(event)
    #     template = "/page/confirm_reg/%s" % (attendees.id.id,)
    #     return werkzeug.utils.redirect(template)

    @http.route(
        "/page/confirm_reg/<int:attendees_id>", type="http", auth="public", website=True
    )
    def ack_issue(self, attendees_id, **post):
        cr, uid, context, registry = (
            request.cr,
            request.uid,
            request.context,
            request.env,
        )
        values = {}
        attendee_orm = request.env["event.registration"].sudo()
        iobj = attendee_orm.sudo().search([("id", "=", int(attendees_id))])
        values = {"attendees": iobj}
        return (
            json.dumps({"success": "Successfully created"})
            if iobj
            else json.dumps({"success": "Successfully Error created"})
        )

    @http.route(["/page/feedback"], type="http", auth="public", website=True)
    def feedback(self, page=1, **searches):
        cr, uid, context = request.cr, request.uid, request.context
        values = {}
        return request.render("event_questions.registration_feedback", values)
