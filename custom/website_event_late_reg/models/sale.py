# Part of Odoo. See LICENSE file for full copyright and licensing details.
import random
from datetime import datetime, timedelta
from urllib.parse import urljoin

import werkzeug

from odoo import api, fields, models
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT


def random_token():
    # the token has an entropy of about 120 bits (6 bits/char * 20 chars)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.SystemRandom().choice(chars) for _ in range(20))


def now(**kwargs):
    # dt = datetime.now() +
    # return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
    return fields.Datetime.now() + timedelta(**kwargs)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    attendee_ids = fields.One2many(
        "event.registration", "sale_order_id", string="Attendees"
    )
    event_token = fields.Char("Event Token", copy=False)
    event_token_expiration = fields.Datetime("Event Token Expiration", copy=False)
    event_token_valid = fields.Boolean(
        compute="_compute_event_token_validity", string="Token Valid?", store=True
    )
    event_token_url = fields.Char(
        compute="_compute_event_token_url", string="Signup URL", store=True
    )

    @api.depends("event_token")
    def _compute_event_token_url(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for order in self:
            params = {"token": order.event_token, "id": order.id}
            order.event_token_url = urljoin(
                base_url,
                f"/events/complete-registration?{werkzeug.url_encode(params)}",
            )

    @api.depends("event_token")
    def _compute_event_token_validity(self):
        dt = now()
        for order in self:
            order.event_token_valid = False
            if order.event_token and (
                not order.event_token_expiration or dt <= order.event_token_expiration
            ):
                order.event_token_valid = True


    def send_late_reg_event_notification(self):
        self.ensure_one()
        expiration = now(days=+7)
        token = random_token()
        self.sudo().write({"event_token": token, "event_token_expiration": expiration})
        message_template = self.sudo().env.ref("website_event_late_reg.late_reg_email")
        if message_template and self.partner_id.email:
            message_template.with_context(event_url=self.event_token_url).send_mail(
                self.partner_id.id, force_send=True
            )


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for a in order.attendee_ids:
                if not a.name:
                    order.send_late_reg_event_notification()


class SalesOrderLine(models.Model):
    _inherit = "sale.order.line"

    attendee_ids = fields.One2many(
        "event.registration", "sale_order_line_id", string="Attendees"
    )
