from odoo import api, models


class Attendee(models.Model):
    _inherit = "event.registration"


    def bulk_confirm_attendees(self):
        for att in self:
            if att.state == "draft":
                att.confirm_registration()


    def bulk_close_attendees(self):
        for att in self:
            try:
                att.button_reg_close()
            except Exception as e:
                pass
