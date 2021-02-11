import base64

# import odoo.addons.decimal_precision as dp
# from odoo.exceptions import UserError, AccessError
import email
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models, tools
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = "account.move"
    # _inherit = ['mail.thread', 'ir.needaction_mixin']
    # _inherit = 'mail.thread'
    # _inherit = 'ir.needaction_mixin'


#     def send_email_certificte(self, cr, uid, template_id, res_ids, context=None, fields=None):
#         """Generates an email from the template for given the given model based on
#         records given by res_ids.
#
#         :param template_id: id of the template to render.
#         :param res_id: id of the record to use for rendering the template (model
#                        is taken from template definition)
#         :returns: a dict containing all relevant fields for creating a new
#                   mail.mail entry, with one extra key ``attachments``, in the
#                   format [(report_name, data)] where data is base64 encoded.
#         """
#         if context is None:
#             context = {}
#         if fields is None:
#             fields = ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to']
#
#         report_xml_pool = self.pool.get('ir.actions.report.xml')
#         res_ids_to_templates = self.get_email_template_batch(cr, uid, template_id, res_ids, context)
#
#         # templates: res_id -> template; template -> res_ids
#         templates_to_res_ids = {}
#         for res_id, template in res_ids_to_templates.iteritems():
#             templates_to_res_ids.setdefault(template, []).append(res_id)
#
#         results = dict()
#         for template, template_res_ids in templates_to_res_ids.iteritems():
#             # generate fields value for all res_ids linked to the current template
#             for field in fields:
#                 generated_field_values = self.render_template_batch(
#                     cr, uid, getattr(template, field), template.model, template_res_ids,
#                     post_process=(field == 'body_html'),
#                     context=context)
#                 for res_id, field_value in generated_field_values.iteritems():
#                     results.setdefault(res_id, dict())[field] = field_value
#             # compute recipients
#             results = self.generate_recipients_batch(cr, uid, results, template.id, template_res_ids, context=context)
#             # update values for all res_ids
#             for res_id in template_res_ids:
#                 values = results[res_id]
#                 # body: add user signature, sanitize
#                 if 'body_html' in fields and template.user_signature:
#                     signature = self.pool.get('res.users').browse(cr, uid, uid, context).signature
#                     values['body_html'] = tools.append_content_to_html(values['body_html'], signature, plaintext=False)
#                 if values.get('body_html'):
#                     values['body'] = tools.html_sanitize(values['body_html'])
#                 # technical settings
#                 values.update(
#                     mail_server_id=template.mail_server_id.id or False,
#                     auto_delete=template.auto_delete,
#                     model=template.model,
#                     res_id=res_id or False,
#                     attachment_ids=[attach.id for attach in template.attachment_ids],
#                 )
#
#             # Add report in attachments: generate once for all template_res_ids
#             if template.report_template:
#                 for res_id in template_res_ids:
#                     attachments = []
#                     report_name = self.render_template(cr, uid, template.report_name, template.model, res_id, context=context)
#                     report = report_xml_pool.browse(cr, uid, template.report_template.id, context)
#                     report_service = report.report_name
#                     # Ensure report is rendered using template's language
#                     ctx = context.copy()
#                     if template.lang:
#                         ctx['lang'] = self.render_template_batch(cr, uid, template.lang, template.model, [res_id], context)[res_id]  # take 0 ?
#
#                     if report.report_type in ['qweb-html', 'qweb-pdf']:
#                         result, format = self.pool['report'].get_pdf(cr, uid, [res_id], report_service, context=ctx), 'pdf'
#                     else:
#                         result, format = odoo.report.render_report(cr, uid, [res_id], report_service, {'model': template.model}, ctx)
#
#                     # TODO in trunk, change return format to binary to match message_post expected format
#                     result = base64.b64encode(result)
#                     if not report_name:
#                         report_name = 'report.' + report_service
#                     ext = "." + format
#                     if not report_name.endswith(ext):
#                         report_name += ext
#                     attachments.append((report_name, result))
#                     results[res_id]['attachments'] = attachments
#
#         return results
