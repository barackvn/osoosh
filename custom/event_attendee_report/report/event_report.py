from datetime import datetime

from pytz import timezone

from odoo import api, models


class EventAttendeeReport(models.AbstractModel):
    _name = "report.event_attendee_report.report_event_attendees"

    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     report = self.env.ref('event_attendee_report.event_attendees')
    #     docs = self.env[report.model].browse(docids)
    #     date_dicts = {}
    #     for doc in docs:
    #         tz = doc.date_tz
    #         user_tz = timezone(tz or 'utc')
    #         date_begin = doc.date_begin.astimezone(user_tz)
    #         date_end = doc.date_end.astimezone(user_tz)
    #         date_dicts[doc.id] = {
    #             'date_begin': date_begin,
    #             'date_end': date_end,
    #         }
    #     return {
    #         'doc_ids': docids,
    #         'doc_model': report.model,
    #         'docs': docs,
    #         'date_dicts': date_dicts
    #     }
    #     return report_obj.render('event_attendee_report.report_event_attendees', docargs)

    @api.model
    def _get_report_values(self, docids, data=None):
        date_dicts = {}
        report_obj = self.env["ir.actions.report"]
        report = report_obj._get_report_from_name(
            "event_attendee_report.report_event_attendees"
        )
        docs = self.env[report.model].browse(docids)
        for doc in docs:
            tz = doc.date_tz
            user_tz = timezone(tz or "utc")
            date_begin = doc.date_begin.astimezone(user_tz)
            date_end = doc.date_end.astimezone(user_tz)
            date_dicts[doc.id] = {"date_begin": date_begin, "date_end": date_end}
        return {
            "doc_ids": docids,
            "doc_model": report.model,
            "docs": self.env[report.model].browse(docids),
            "date_dicts": date_dicts,
            "report_type": data.get("report_type") if data else "",
        }
        # return report_obj.render('event_attendee_report.report_event_attendees', docargs)
