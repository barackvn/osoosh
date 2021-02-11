from odoo import fields, models, tools


class EventAnswer(models.Model):
    _inherit = "event.question.answer"

    name = fields.Char("Answer", required=False)
    question_id = fields.Many2one("event.question", required=False)


class EventQuestion(models.Model):
    _inherit = "event.question"

    ans = fields.Char("Answer", required=False)
    registration_id = fields.Many2one("event.registration")
    answer_ids = fields.One2many(
        "event.question.answer", "question_id", "Answers", required=False
    )
    reg_express = fields.Char("Regular Expression")
    error_msg = fields.Char("Error message")


class EventQuestionNew(models.Model):
    _name = "event.question.new"

    ans = fields.Char("Answer", required=False)
    registration_id = fields.Many2one("event.registration")
    title = fields.Char(required=False)


class EventRegistration(models.Model):
    """ Store answers on attendees. """

    _inherit = "event.registration"

    question_ids = fields.One2many(
        "event.question.new", "registration_id", string="Questions"
    )


# class ReportEventRegistrationQuestions(models.Model):
#     _inherit = "event.question.report"
#
#     answer_id = fields.Many2one(comodel_name="event.answer", string="Answer")
