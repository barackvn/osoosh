# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)
# from odoo.osv.orm import setup_modifiers


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    event_ids = fields.Many2many(
        "event.event",
        "account_invoice_send_event_rel",
        "invoice_id",
        "event_id",
        "Events",
    )

    generate_certificates = fields.Boolean(
        string='Generate Certificates')

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
        result = super(AccountInvoiceSend, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        _logger.info('Context %s'%self.env.context)
        active_id = self.env.context.get('active_id', False)
        if self.env.context.get('params', False):
            params = self.env.context.get('params', False)
            if params['model'] == 'account.move':
                active_id = params['id']

        invoice_id = self.env["account.move"].browse(active_id)
        _logger.info('Invoice ID %s'%invoice_id)
        _logger.info('Invoice Lines IDs %s'%invoice_id.invoice_line_ids)
        if invoice_id.invoice_line_ids: 
            so_line_ids = []
            for inv_line in invoice_id.invoice_line_ids:
                so_line_ids += inv_line.sale_line_ids.ids
                _logger.info('SO Lines IDs %s'%so_line_ids)
            att_ids = self.env["event.registration"].search([("sale_order_line_id", "in", so_line_ids)])
            _logger.info('att_ids %s'%att_ids)
            event_ids = att_ids.mapped("event_id")
            _logger.info('event_ids %s'%event_ids)
            doc = etree.XML(result["arch"])
            node = doc.xpath("//field[@name='event_ids']")[0]
            node.set("domain", "[('id', 'in', %s)]" % event_ids.ids)
            # setup_modifiers(node, result["fields"]["event_ids"])
            result["arch"] = etree.tostring(doc)
        return result

    @api.onchange('generate_certificates')
    def button_generate_certificates(self):
        if self.event_ids:
            so_line_ids = []
            active_id = self.env.context.get('active_id', False)
            if self.env.context.get('params', False):
                params = self.env.context.get('params', False)
                if params['model'] == 'account.move':
                    active_id = params['id']
            invoice_id = self.env["account.move"].browse(active_id)
            for inv_line in invoice_id.invoice_line_ids:
                so_line_ids += inv_line.sale_line_ids.ids
            cert_ids = self.event_ids.generate_event_certificates(
                invoice_id.id, so_line_ids
            )
            _logger.info('Certificate %s'%cert_ids)
            if cert_ids:
                cert_attachment_ids = self.env["ir.attachment"].search(
                    [
                        ("res_model", "in", ["event.certificate"]),
                        ("res_id", "in", cert_ids.ids),
                    ]
                )
                if cert_attachment_ids:
                    self.attachment_ids = [(6,0,self.attachment_ids.ids + cert_attachment_ids.ids)]
                        
        return True