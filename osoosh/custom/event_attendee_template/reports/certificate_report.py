# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

import pytz
from pytz import timezone

from odoo import _, api, models


class CertificateReport(models.AbstractModel):
    _name = "report.event_custom_4devnet.report_certificate"

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env["ir.actions.report"]
        report = report_obj._get_report_from_name(
            "event_custom_4devnet.report_certificate"
        )
        docs = self.env[report.model].browse(docids)

        events_dict = {}

        for doc in docs:
            a = doc.attendee_id
            attendee_template_id = a.template_id if a.template_id else a
            attendee_ids = a
            event_ids = a.event_id

            if a.is_a_template or a.template_id:
                attendee_ids = a.sale_order_line_id.attendee_ids.filtered(
                    lambda r: r.template_id.id == attendee_template_id.id
                )
                if (
                    not a.sale_order_line_id.product_id.product_tmpl_id.is_learning_product
                ):
                    attendee_ids = attendee_template_id | attendee_ids
            else:
                attendee_ids = a.sale_order_line_id.attendee_ids.filtered(
                    lambda r: r.name == attendee_template_id.name
                )

            event_ids = attendee_ids.mapped("event_id").sorted(
                key=lambda r: r.date_begin
            )

            date_begin = event_ids[0].date_begin if event_ids else None
            date_end = event_ids[-1].date_end if event_ids else None

            events_dict[doc.id] = {
                "event_ids": event_ids,
                "date_begin": date_begin,
                "date_end": date_end,
            }

        return {
            "doc_ids": docids,
            "doc_model": report.model,
            "docs": docs,
            "events_dict": events_dict,
        }
        return report_obj.render("event_custom_4devnet.report_certificate", docargs)
