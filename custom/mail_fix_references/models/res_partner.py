from odoo import api, models


class Partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _notify_prepare_email_values(self, message):
        # compute email references
        references = message.parent_id.message_id if message.parent_id else False

        # custom values
        custom_values = dict()
        if (
            message.res_id
            and message.model in self.env
            and hasattr(self.env[message.model], "message_get_email_values")
        ):
            custom_values = (
                self.env[message.model]
                .browse(message.res_id)
                .message_get_email_values(message)
            )

        mail_values = {
            "mail_message_id": message.id,
            "mail_server_id": message.mail_server_id.id,
            "auto_delete": self._context.get("mail_auto_delete", True),
            "references": references or message.message_id,
        }
        mail_values.update(custom_values)
        return mail_values
