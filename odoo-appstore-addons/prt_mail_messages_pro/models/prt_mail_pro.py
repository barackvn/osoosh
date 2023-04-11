###################################################################################
# 
#    Copyright (C) 2020 Cetmix OÜ
#
#   Odoo Proprietary License v1.0
# 
#   This software and associated files (the "Software") may only be used (executed,
#   modified, executed after modifications) if you have purchased a valid license
#   from the authors, typically via Odoo Apps, or if you have received a written
#   agreement from the authors of the Software (see the COPYRIGHT file).
# 
#   You may develop Odoo modules that use the Software as a library (typically
#   by depending on it, importing it and using its resources), but without copying
#   any source code or material from the Software. You may distribute those
#   modules under the license of your choice, provided that this license is
#   compatible with the terms of the Odoo Proprietary License (For example:
#   LGPL, MIT, or proprietary licenses similar to this one).
# 
#   It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#   or modified copies of the Software.
# 
#   The above copyright notice and this permission notice must be included in all
#   copies or substantial portions of the Software.
# 
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#   ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#
###################################################################################

from odoo import _, api, fields, models
from odoo.exceptions import AccessError


###############
# Mail.Thread #
###############
class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    hide_notifications = fields.Boolean(
        string="Hide notifications", help="Hide notifications"
    )
    hide_notes = fields.Boolean(string="Hide notes", help="Hide notes")
    hide_messages = fields.Boolean(string="Hide messages", help="Hide messages")

    def save_thread_filter(self, vals):
        """
        Save thread filter and send notifications to current user threads
        """
        self.ensure_one()
        self.write(vals)
        bus_obj = self.env["bus.bus"]
        db_name = self._cr.dbname
        partner_id = self.env.user.partner_id.id
        thread_id = self.id
        thread_model = self._name
        for key, val in vals.items():
            notification = {
                "type": "filter_updated",
                "filter": key,
                "value": val,
                "thread_id": thread_id,
                "thread_model": thread_model,
            }
            bus_obj.sendone((db_name, "res.partner", partner_id), notification)


################
# Mail.Message #
################
class MailMessage(models.Model):
    _inherit = "mail.message"

    # -- Unlink
    def unlink(self):
        # Avoid triggering for inheriting models
        if self._name != "mail.message":
            return super(MailMessage, self).unlink()

        # Deleted from parent record?
        if self._context.get("force_delete", False):
            return super(MailMessage, self).unlink()

        # Delete messages linked with emails
        email_messages = self.filtered("is_mail_mail")
        len_email_messages = len(email_messages)
        if len_email_messages > 0:
            return super(MailMessage, email_messages.sudo()).unlink()
        if len(self) == len_email_messages:
            return
        # TODO: move the method to base module (check unlink for mail.mail)

        # Check access rights
        self.unlink_rights_check()

        partner_ids = [partner.id for partner in self.mapped("ref_partner_ids")]
        if self.env.user.partner_id.id not in partner_ids:
            partner_ids.append(self.env.user.partner_id.id)
        notifications = [
            [
                (self._cr.dbname, "res.partner", partner_id),
                {"type": "deletion", "message_ids": self.ids},
            ]
            for partner_id in partner_ids
        ]
        self.env["bus.bus"].sendmany(notifications)

        lead_ids = [rec.res_id for rec in self.sudo() if rec.model == "crm.lead"]
        # Unlink
        if self.env.user.has_group("prt_mail_messages_pro.group_lost"):
            # Check is deleting lost messages
            all_lost = True
            for rec in self.sudo():

                # Not lost? Unlink using actual user
                if rec.model and rec.res_id:
                    super(MailMessage, self).unlink()
                    all_lost = False
                    break

            # All lost. Unlink using sudo
            if all_lost:
                super(MailMessage, self.sudo()).unlink()
        else:
            super(MailMessage, self).unlink()

        # All done if CRM Lead is not presented in models (eg CRM not installed)
        if (
            not self.env["ir.model"]
            .sudo()
            .search([("model", "=", "crm.lead")], limit=1)
        ):
            return

        # Delete empty leads
        leads = (
            self.env["crm.lead"]
            .browse(lead_ids)
            .filtered(lambda l: l.company_id.lead_delete and l.type == "lead")
        )

        # Add opportunities to delete
        leads += (
            self.env["crm.lead"]
            .browse(lead_ids)
            .filtered(lambda l: l.company_id.opp_delete and l.type == "opportunity")
        )

        leads_2_delete = self.env["crm.lead"]

        for lead in leads:
            message_count = self.env["mail.message"].search_count(
                [
                    ("res_id", "=", lead.id),
                    ("model", "=", "crm.lead"),
                    ("message_type", "!=", "notification"),
                ]
            )
            if message_count == 0:
                leads_2_delete += lead

        # Delete leads with no messages
        if len(leads_2_delete) > 0:
            leads_2_delete.unlink()

    # -- Fields for frontend
    def _get_message_format_fields(self):
        res = super(MailMessage, self)._get_message_format_fields()
        res.append("cx_edit_message")
        return res

    # -- Move messages
    def message_move(
        self, dest_model, dest_res_id, notify="0", lead_delete=False, opp_delete=False
    ):
        """
        Moves messages to a new record
        :return:
        :param Char dest_model: name of the new record model
        :param Integer dest_res_id: id of the new record
        :param Char notify: add notification to destination thread
            '0': 'Do not notify'
            '1': 'Log internal note'
            '2': 'Send message'
        :param Boolean lead_delete: delete CRM Leads with no messages left
        :param Boolean opp_delete: delete CRM Opportunities with no messages left
        :return: nothing, just return)
        """

        # -- Can move messages?
        if not self.env.user.has_group("prt_mail_messages.group_move"):
            raise AccessError(_("You cannot move messages!"))

        old_records = [
            {
                "message_id": message.id,
                "originalThread": {
                    "thread_id": message.res_id,
                    "thread_model": message.model,
                },
                "movedThread": {
                    "thread_id": dest_res_id,
                    "thread_model": dest_model,
                },
            }
            for message in self
        ]
        # Store leads from messages in case we want to delete empty leads later
        leads = False
        if lead_delete:
            lead_messages = self.env["mail.message"].search(
                [("id", "in", self.ids), ("model", "=", "crm.lead")]
            )

            # Check if Opportunities are deleted as well
            if opp_delete:
                domain = [("id", "in", lead_messages.mapped("res_id"))]
            else:
                domain = [
                    ("id", "in", lead_messages.mapped("res_id")),
                    ("type", "=", "lead"),
                ]

            leads = self.env["crm.lead"].search(domain)

        # Get Conversations. Will check and delete empty ones later
        conversations = False
        conversation_messages = self.filtered(
            lambda m: m.model == "cetmix.conversation"
        )
        if len(conversation_messages) > 0:
            conversations = self.env["cetmix.conversation"].search(
                [("id", "in", conversation_messages.mapped("res_id"))]
            )

        if parent_message := self.env["mail.message"].search(
            [
                ("model", "=", dest_model),
                ("res_id", "=", dest_res_id),
                ("parent_id", "=", False),
            ],
            order="id asc",
            limit=1,
        ):
            self.sudo().write(
                {
                    "model": dest_model,
                    "res_id": dest_res_id,
                    "parent_id": parent_message.id,
                }
            )
        else:
            self.sudo().write(
                {"model": dest_model, "res_id": dest_res_id, "parent_id": False}
            )

        # Move attachments. Use sudo() to override access rules issues
        self.mapped("attachment_ids").sudo().write(
            {"res_model": dest_model, "res_id": dest_res_id}
        )

        # Notify followers of destination record
        if notify and notify != "0":
            subtype = "mail.mt_note" if notify == "1" else "mail.mt_comment"
            body = _("%s messages moved to this record:") % (str(len(self)))
            url = (
                self.env["ir.config_parameter"].sudo().get_param("web.base.url")
                + "/web#id="
            )
            for i, message in enumerate(self, start=1):
                body += (
                    f' <a target="_blank" href="{url + str(message.id) + "&model=mail.message&view_type=form"}">'
                    + _("Message %s") % (str(i))
                    + "</a>"
                )
            self.env[dest_model].browse([dest_res_id]).message_post(
                body=body,
                subject=_("Messages moved"),
                message_type="notification",
                subtype=subtype,
            )
        # Delete empty Conversations
        if conversations:
            self.env["mail.message"]._delete_conversations(conversations.ids)

        partner_ids = [partner.id for partner in self.mapped("ref_partner_ids")]
        if self.env.user.partner_id.id not in partner_ids:
            partner_ids.append(self.env.user.partner_id.id)
        notifications = [
            [
                (self._cr.dbname, "res.partner", partner_id),
                {
                    "type": "message_updated",
                    "action": "move",
                    "message_ids": old_records,
                },
            ]
            for partner_id in partner_ids
        ]
        self.env["bus.bus"].sendmany(notifications)

        # Update Conversation last message data if moved to Conversation
        if dest_model == "cetmix.conversation":
            conversation = self.env["cetmix.conversation"].browse(dest_res_id)
            if conversation.message_ids:  # To ensure
                messages = conversation.message_ids.sorted(
                    key=lambda m: m.id, reverse=True
                )
                conversation.update(
                    {
                        "last_message_post": messages[0].date,
                        "last_message_by": messages[0].author_id.id,
                    }
                )

        # Delete empty leads
        if not leads:
            return

        # Compose list of leads to unlink
        leads_2_delete = self.env["crm.lead"]
        for lead in leads:
            message_count = self.env["mail.message"].search_count(
                [
                    ("res_id", "=", lead.id),
                    ("model", "=", "crm.lead"),
                    ("message_type", "!=", "notification"),
                ]
            )
            if message_count == 0:
                leads_2_delete += lead

        # Delete leads with no messages
        if len(leads_2_delete) > 0:
            leads_2_delete.unlink()


#####################
# Mail Move Message #
#####################
class MailMove(models.TransientModel):
    _inherit = "prt.message.move.wiz"

    # -- Move messages
    def message_move(self):
        # -- Can move messages?
        if not self.env.user.has_group("prt_mail_messages.group_move"):
            raise AccessError(_("You cannot move messages!"))

        self.ensure_one()
        if not self.model_to:
            return

        # Check call source.
        # If conversation take all conversation messages.
        # If thread then take active ids
        if self.is_conversation:
            messages = self.env["mail.message"].search(
                [
                    ("model", "=", "cetmix.conversation"),
                    ("res_id", "in", self._context.get("active_ids", False)),
                    ("message_type", "!=", "notification"),
                ]
            )
        else:
            thread_message_id = self._context.get("thread_message_id", False)
            message_ids = (
                [thread_message_id]
                if thread_message_id
                else self._context.get("active_ids", False)
            )
            if not message_ids or len(message_ids) < 1:
                return
            messages = self.env["mail.message"].browse(message_ids)

        # Move messages
        messages.message_move(
            self.model_to._name,
            self.model_to.id,
            lead_delete=self.is_lead and self.lead_delete,
            opp_delete=self.is_lead and self.opp_delete,
        )


###############
# Res.Company #
###############
class Company(models.Model):
    _inherit = "res.company"

    lead_delete = fields.Boolean(
        string="Delete empty leads",
        help="If all messages are moved from lead and there are no other messages"
        " left except for notifications lead will be deleted",
        readonly=False,
    )
    opp_delete = fields.Boolean(
        string="Delete empty opportunities",
        help="If all messages are moved from lead and there are no other messages"
        " left except for notifications opportunity will be deleted",
        readonly=False,
    )


#################
# Author assign #
#################
class MessagePartnerAssign(models.TransientModel):
    _inherit = "cx.message.partner.assign.wiz"

    # -- Change Same Email only
    @api.onchange("same_email", "email")
    def is_same(self):
        if self.same_email:
            return {"domain": {"partner_id": [("email", "=", self.email)]}}
        else:
            return {"domain": {"partner_id": []}}

    # -- Assign current message
    def assign_one(self):
        self._cr.execute(
            """
        UPDATE mail_message
        SET author_id=%s
        WHERE id=%s""",
            (self.partner_id.id, self._context.get("active_id"),),
        )

    # -- Assign all unassigned messages with same email in 'From'
    def assign_all(self):
        self._cr.execute(
            """
        UPDATE mail_message
        SET author_id=%s
        WHERE (email_from LIKE %s OR email_from=%s) AND (author_id IS NULL)""",
            (self.partner_id.id, "".join(["%<", self.email, ">"]), self.email,),
        )


#################
# Edit message #
#################
class MessageEdit(models.TransientModel):
    _inherit = "cx.message.edit.wiz"

    # -- Save message
    def save(self):
        res = super(MessageEdit, self).save()

        partner_ids = [partner.id for partner in self.message_id.ref_partner_ids]
        if self.env.user.partner_id.id not in partner_ids:
            partner_ids.append(self.env.user.partner_id.id)
        notifications = [
            [
                (self._cr.dbname, "res.partner", partner_id),
                {
                    "type": "message_updated",
                    "action": "edit",
                    "message_ids": [{"message_id": self.message_id.id}],
                },
            ]
            for partner_id in partner_ids
        ]
        self.env["bus.bus"].sendmany(notifications)
        return res
