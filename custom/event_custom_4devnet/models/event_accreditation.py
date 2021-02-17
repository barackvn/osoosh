from odoo import api, fields, models


class EventAccreditation(models.Model):
    """."""

    _description = "Event Accreditation"
    _name = "event.accreditation"

    name = fields.Char(string="Name of accreditation", required=True)
    reference = fields.Char(string="Reference")
    accreditation_id = fields.Char(string="Accreditation ID")
    code = fields.Char(string="Accreditation Code")
    target = fields.Char(string="Target")
    hours = fields.Float(string="No. of Hours", digits=0)
    release_date = fields.Date(string="Date Issued")
    valid_until = fields.Date(string="Valid Until")

    @api.model
    def create(self, vals):
        if vals.get("reference", "New") == "New":
            vals["reference"] = (
                self.env["ir.sequence"].sudo().next_by_code("event.accreditation")
                or "New"
            )
        result = super(EventAccreditation, self).create(vals)
        return result
