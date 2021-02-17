from odoo import api, fields, models


class EventCertificate(models.Model):
    """Event Certificate"""

    _name = "event.certificate"
    _inherit = ["mail.thread"]
    _description = "Event Certificate"

    name = fields.Char(string="Reference", required=True, default="New")
    attendee_id = fields.Many2one(
        "event.registration", string="Attendee", required=True
    )
    event_id = fields.Many2one("event.event", related="attendee_id.event_id")
    accreditation_id = fields.Many2one(
        "event.accreditation", related="attendee_id.event_id.accreditation_id"
    )
    invoice_id = fields.Many2one("account.move", string="Invoice")
    release_date = fields.Datetime(
        string="Release date", help="Date invoice is sent to customer"
    )
    x_company_registry = fields.Char(
        related="attendee_id.partner_id.company_registry", string="ICO"
    )
    # attendee_id = fields.Many2one(
    #     "event.registration", string="Attendee Name", required=True
    # )

    @api.onchange("attendee_id")
    def _onchange_attendee_id(self):
        for r in self:
            if r.attendee_id:
                r.certificate_attendee = r.attendee_id.name

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = (
                self.env["ir.sequence"].sudo().next_by_code("event.certificate")
                or "New"
            )
        result = super(EventCertificate, self).create(vals)
        return result

    @api.model
    def get_report_values(self, docids, data=None):
        pass
