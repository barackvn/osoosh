from datetime import datetime

from odoo import api, models, _
from odoo.exceptions import UserError


class Invoice(models.Model):
    _inherit = "account.move"


    def generate_event_certificates(self):
        self.ensure_one
        so_line_ids = []
        for inv_line in self.invoice_line_ids:
            so_line_ids += inv_line.sale_line_ids.ids
        cert_ids, attachment_ids = self.env[
            "event.registration"
        ].generate_event_certificates_by_so_lines(so_line_ids)
        cert_ids.write(
            {
                "invoice_id": self.id,
                "release_date": datetime.now().strftime("%Y-%m-%d"),
            }
        )
        return attachment_ids


    def invoice_validate(self):
        for invoice in self:
            if (
                invoice.type in ("in_invoice", "in_refund")
                and invoice.reference
                and self.search(
                    [
                        ("type", "=", invoice.type),
                        ("reference", "=", invoice.reference),
                        ("company_id", "=", invoice.company_id.id),
                        (
                            "commercial_partner_id",
                            "=",
                            invoice.commercial_partner_id.id,
                        ),
                        ("id", "!=", invoice.id),
                    ]
                )
            ):
                raise UserError(
                    _(
                        "Duplicated vendor reference detected. You probably encoded twice the same vendor bill/refund."
                    )
                )
        return self.write({"state": "open"})


    def generate_certificate(self):
        for invoice in self:
            sale_line_ids = self.env["sale.order.line"]
            for line in invoice.invoice_line_ids:
                for sale_line in line.sale_line_ids:
                    sale_line_ids |= sale_line

            attendees = self.env["event.registration"].search(
                [("sale_order_line_id", "in", sale_line_ids.ids)]
            )

            for att in attendees:
                if att.state == "open":
                    att.button_reg_close()

            for att in attendees:
                att.generate_certificate()

            invoice.write({"certificate_gen": True})
