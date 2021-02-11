# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class TaskStage(models.Model):
    _inherit = "project.task.type"

    survey_id = fields.Many2one("survey.survey", string="Survey")


class Task(models.Model):
    _inherit = "project.task"

    survey_id = fields.Many2one("survey.survey", "Survey", related="stage_id.survey_id")
    response_id = fields.Many2one("survey.user_input", "Response", ondelete="set null")
    survey_result_ids = fields.One2many(
        "project.task.survey.result", "task_id", "Survey Results"
    )
    survey_result_count = fields.Integer(
        "Surveys", compute="_compute_survey_results_count"
    )


    @api.depends("survey_result_ids")
    def _compute_survey_results_count(self):
        for task in self:
            task.survey_result_count = len(task.survey_result_ids)


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


    def button_new_survey(self):
        survey_result = self.env["project.task.survey.result"].create(
            {"task_id": self.id, "name": "New", "survey_id": self.survey_id.id}
        )
        return survey_result.action_start_survey()


class TaskSurvey(models.Model):
    _name = "project.task.survey.result"

    name = fields.Char("Description", default="New", required=True)
    task_id = fields.Many2one("project.task", "Task")
    response_id = fields.Many2one("survey.user_input", "Response", ondelete="set null")
    survey_id = fields.Many2one("survey.survey", string="Survey", required=True)


    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.task_id.survey_id:
            raise UserError(_("Sorry, you cannot perform survey at this stage."))
        if not self.response_id:
            response = self.env["survey.user_input"].create(
                {
                    "survey_id": self.survey_id.id,
                    "partner_id": self.task_id.partner_id.id,
                }
            )
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        return self.survey_id.with_context(
            survey_token=response.token
        ).action_start_survey()
