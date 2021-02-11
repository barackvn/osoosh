from odoo import fields, models, tools


class event_question_report_new(models.Model):
    _name = "event.question.report.new"
    _auto = False

    ans = fields.Char("Answer", size=228, readonly=True)
    title = fields.Char("Title", size=228, readonly=True)
    attendee_id = fields.Many2one("event.registration", "Registration", readonly=True)
    no = fields.Integer(string="#No")

    def init(self):
        """ Event Question main report """
        cr = self._cr
        tools.drop_view_if_exists(cr, "event_question_report_new")
        cr.execute(
            """ CREATE VIEW event_question_report_new AS (
            SELECT
                att_question.id AS id,
                att_question.registration_id as attendee_id,
                att_question.ans as ans,
                att_question.title as title,
                count(att_question.title) as no
            FROM
                event_question_new as att_question
                
            GROUP BY
                id,
                attendee_id,
                ans,
                title
                )"""
        )
