# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Event(models.Model):
    _inherit = "event.event"

    survey_id = fields.Many2one("survey.survey", string="Survey")
    response_id = fields.Many2one("survey.user_input", "Response", ondelete="set null")
    x_tag = fields.Char(string="Tags")  # Confirm field type from Josef


    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.response_id:
            response = self.env["survey.user_input"].create(
                {
                    "survey_id": self.survey_id.id,
                    "partner_id": self.sale_order_origin.partner_id.id,
                }
            )
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        return self.survey_id.with_context(
            survey_token=response.token
        ).action_start_survey()


class Attendee(models.Model):
    _inherit = "event.registration"

    survey_id = fields.Many2one("survey.survey", "Survey", related="event_id.survey_id")
    response_id = fields.Many2one("survey.user_input", "Response", ondelete="set null")


    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.response_id:
            response = self.env["survey.user_input"].create(
                {"survey_id": self.survey_id.id, "partner_id": self.partner_id.id}
            )
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        return self.survey_id.with_context(
            survey_token=response.token
        ).action_start_survey()
