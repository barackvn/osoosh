# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models


class Task(models.Model):
    _inherit = "project.task"

    meeting_count = fields.Integer("# Meetings", compute="_compute_meeting_count")


    def _compute_meeting_count(self):
        meeting_data = self.env["calendar.event"].read_group(
            [("task_id", "in", self.ids)], ["task_id"], ["task_id"]
        )
        mapped_data = {m["task_id"][0]: m["task_id_count"] for m in meeting_data}
        for task in self:
            task.meeting_count = mapped_data.get(task.id, 0)


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
        description = "Task: " + self.name
        action = self.env.ref("calendar.action_calendar_event").read()[0]
        partner_ids = self.env.user.partner_id.ids
        if self.partner_id:
            partner_ids.append(self.partner_id.id)
            description += "\nPartner Information:\n%s" % self.partner_id.name
            description += (
                ("\n" + self.partner_id.street) if self.partner_id.street else ""
            )
            description += (
                ("\n" + self.partner_id.street2) if self.partner_id.street2 else ""
            )
            description += ("\n" + self.partner_id.city) if self.partner_id.city else ""
            description += (
                ("\n" + self.partner_id.state_id.name)
                if self.partner_id.state_id
                else ""
            )
            description += (
                ("\n" + self.partner_id.country_id.name)
                if self.partner_id.country_id
                else ""
            )
            description += ("\n" + self.partner_id.zip) if self.partner_id.zip else ""
            description += (
                ("\n" + self.partner_id.phone) if self.partner_id.phone else ""
            )
            description += (
                ("\n" + self.partner_id.email) if self.partner_id.email else ""
            )
        action["context"] = {
            "search_default_task_id": self.id,
            "default_task_id": self.id,
            "default_partner_id": self.partner_id.id,
            "default_partner_ids": partner_ids,
            "default_name": self.name,
            "default_description": description,
        }
        return action
