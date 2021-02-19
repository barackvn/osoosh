from odoo import api, fields, models, _


class Event(models.Model):
    _inherit = "event.event"

    meeting_count = fields.Integer("# Meetings", compute="_compute_meeting_count")

    def _compute_meeting_count(self):
        for event in self:
            event.meeting_count = self.env['calendar.event'].search_count([('event_id','=',event.id)])
        # meeting_data = self.env["calendar.event"].read_group(
        #     [("event_id", "in", self.ids)], ["event_id"], ["event_id"]
        # )
        # mapped_data = {m["event_id"][0]: m["event_id_count"] for m in meeting_data}
        # for event in self:
        #     event.meeting_count = mapped_data.get(event.id, 0)
        return True


    def log_meeting(self, meeting_subject, meeting_date, duration):
        if not duration:
            duration = _("unknown")
        else:
            duration = str(duration)
        meet_date = fields.Datetime.from_string(meeting_date)
        meeting_usertime = fields.Datetime.to_string(
            fields.Datetime.context_timestamp(self, meet_date)
        )
        html_time = "<time datetime='%s+00:00'>%s</time>" % (
            meeting_date,
            meeting_usertime,
        )
        message = _(
            "Meeting scheduled at '%s'<br> Subject: %s <br> Duration: %s hour(s)"
        ) % (html_time, meeting_subject, duration)
        return self.message_post(body=message)


    def action_schedule_meeting(self):
        self.ensure_one()
        description = "Event: " + self.name
        action = self.env.ref("calendar.action_calendar_event").read()[0]
        partner_ids = self.env.user.partner_id.ids
        if self.address_id:
            description += "\nLocation Information:\n%s" % self.address_id.name
            description += (
                ("\n" + self.address_id.street) if self.address_id.street else ""
            )
            description += (
                ("\n" + self.address_id.street2) if self.address_id.street2 else ""
            )
            description += ("\n" + self.address_id.city) if self.address_id.city else ""
            description += (
                ("\n" + self.address_id.state_id.name)
                if self.address_id.state_id
                else ""
            )
            description += (
                ("\n" + self.address_id.country_id.name)
                if self.address_id.country_id
                else ""
            )
            description += ("\n" + self.address_id.zip) if self.address_id.zip else ""
            description += (
                ("\n" + self.address_id.phone) if self.address_id.phone else ""
            )
            description += (
                ("\n" + self.address_id.email) if self.address_id.email else ""
            )
        action["context"] = {
            "search_default_event_id": self.id,
            "default_event_id": self.id,
            "default_partner_id": self.address_id.id,
            "default_partner_ids": partner_ids,
            "default_name": self.name,
            "default_description": description,
        }
        return action
