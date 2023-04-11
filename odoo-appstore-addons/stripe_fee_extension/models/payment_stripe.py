# -*- coding: utf-8 -*-

import pprint
import logging
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_round

from odoo.addons.payment_stripe.controllers.main import StripeController

_logger = logging.getLogger(__name__)

INT_CURRENCIES = [
    u'BIF', u'XAF', u'XPF', u'CLP', u'KMF', u'DJF', u'GNF', u'JPY', u'MGA', u'PYG', u'RWF', u'KRW',
    u'VUV', u'VND', u'XOF'
]


class PaymentAcquirerStripe(models.Model):
    _inherit = 'payment.acquirer'

    def _get_feature_support(self):
        """Get advanced feature support by provider.

        Each provider should add its technical in the corresponding
        key for the following features:
            * fees: support payment fees computations
            * authorize: support authorizing payment (separates
                         authorization and capture)
            * tokenize: support saving payment data in a payment.tokenize
                        object
        """
        res = super(PaymentAcquirerStripe, self)._get_feature_support()
        res['fees'].append('stripe')
        return res

    def stripe_compute_fees(self, amount, currency_id, country_id):
        """ Compute stripe fees.

            :param float amount: the amount to pay
            :param integer country_id: an ID of a res.country, or None. This is
                                       the customer's country, to be compared to
                                       the acquirer company country.
            :return float fees: computed fees
        """
        if not self.fees_active:
            return 0.0
        country = self.env['res.country'].browse(country_id)
        if country and self.company_id.country_id.id == country.id:
            percentage = self.fees_dom_var
            fixed = self.fees_dom_fixed
        else:
            percentage = self.fees_int_var
            fixed = self.fees_int_fixed
        return (percentage / 100.0 * amount + fixed) / (1 - percentage / 100.0)

    def stripe_form_generate_values(self, tx_values):
        self.ensure_one()
        if not self.fees_active:
            return super(PaymentAcquirerStripe, self).stripe_form_generate_values(tx_values)
        base_url = self.get_base_url()
        stripe_session_data = {
            'payment_method_types[]': 'card',
            'line_items[][amount]': int(
                (tx_values['amount'] + tx_values['fees'])
                if tx_values['currency'].name in INT_CURRENCIES
                else float_round(
                    (tx_values['amount'] + tx_values['fees']) * 100, 2
                )
            ),
            'line_items[][currency]': tx_values['currency'].name,
            'line_items[][quantity]': 1,
            'line_items[][name]': tx_values['reference'],
            'client_reference_id': tx_values['reference'],
            'success_url': f"{urls.url_join(base_url, StripeController._success_url)}?reference={tx_values['reference']}",
            'cancel_url': f"{urls.url_join(base_url, StripeController._cancel_url)}?reference={tx_values['reference']}",
            'customer_email': tx_values['partner_email'],
        }
        tx_values['session_id'] = self._create_stripe_session(stripe_session_data)
        return tx_values


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _stripe_create_payment_intent(self, acquirer_ref=None, email=None):
        if not self.payment_token_id.stripe_payment_method:
            self.payment_token_id._stripe_sca_migrate_customer()

        charge_params = {
            'amount': int((self.amount + self.fees) if self.currency_id.name in INT_CURRENCIES else float_round((self.amount + self.fees) * 100, 2)),
            'currency': self.currency_id.name.lower(),
            'off_session': True,
            'confirm': True,
            'payment_method': self.payment_token_id.stripe_payment_method,
            'customer': self.payment_token_id.acquirer_ref,
            'description': self.reference,
        }
        if not self.env.context.get('off_session'):
            charge_params.update(setup_future_usage='off_session', off_session=False)
        _logger.info('_stripe_create_payment_intent: Sending values to stripe, values:\n%s', pprint.pformat(charge_params))

        res = self.acquirer_id._stripe_request('payment_intents', charge_params)
        if res.get('charges') and res.get('charges').get('total_count'):
            res = res.get('charges').get('data')[0]

        _logger.info('_stripe_create_payment_intent: Values received:\n%s', pprint.pformat(res))
        return res

    def _stripe_form_get_invalid_parameters(self, data):
        if self.provider != 'stripe' or not self.acquirer_id.fees_active:
            return super(PaymentTransaction, self)._stripe_form_get_invalid_parameters(data)
        invalid_parameters = []
        if data.get('amount') != int((self.amount + self.fees) if self.currency_id.name in INT_CURRENCIES else float_round((self.amount + self.fees) * 100, 2)):
            invalid_parameters.append(('Amount', data.get('amount'), self.amount * 100))
        if data.get('currency').upper() != self.currency_id.name:
            invalid_parameters.append(('Currency', data.get('currency'), self.currency_id.name))
        if data.get('payment_intent') and data.get('payment_intent') != self.stripe_payment_intent:
            invalid_parameters.append(('Payment Intent', data.get('payment_intent'), self.stripe_payment_intent))
        return invalid_parameters
