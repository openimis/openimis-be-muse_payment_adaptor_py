import json
import unittest
from unittest.mock import patch

from core.models import User
from muse_payment_adaptor.api_interface.muse_api_client import BulkPaymentSubmissionClient, MuseApiClient
from openIMIS.openimisapps import openimis_apps
from django.test import TestCase

from muse_payment_adaptor.api_interface.signature import verify_signature_b64_string
from muse_payment_adaptor.apps import MusePaymentAdaptorConfig
from muse_payment_adaptor.tests.helpers.signature_data import test_certificate

imis_modules = openimis_apps()


class BulkyPaymentApiClientTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(BulkyPaymentApiClientTests, cls).setUpClass()
        cls.api_client = BulkPaymentSubmissionClient()
        if not User.objects.filter(username='admin_muse').exists():
            User.objects.create_superuser(username='admin_muse', password='S\/pe®Pąßw0rd™')
        cls.user = User.objects.filter(username='admin_muse').first()

    def _get_bill(self):
        required_modules = ['invoice', 'calcrule_unconditional_cash_payment', 'contribution_plan']
        if not all([module in imis_modules for module in required_modules]):
            raise unittest.SkipTest('Required modules not installed')

        from invoice.models import Bill
        from calcrule_unconditional_cash_payment.calculation_rule import UnconditionalCashPaymentCalculationRule
        from policy.models import Policy
        from contribution_plan.models import PaymentPlan
        policy = Policy.objects.filter(validity_to=None).first()
        payment_plan = PaymentPlan(**{
            'code': 'TestCode',
            'name': 'TestName',
            'periodicity': 12,
            'calculation': '16bca786-1c12-4e8e-9cbf-e33c2a6d9f4f',
            'benefit_plan': policy.product,
            'json_ext': {'calculation_rule': {'lumpsum_to_be_paid': '50', 'invoice_label': 'invoice label'}},
        })
        payment_plan.save(username=self.user.username)
        UnconditionalCashPaymentCalculationRule.active_for_object(instance=policy, context='PolicyCreated',
                                                                  type='account_payable', sub_type='cash_payment')
        UnconditionalCashPaymentCalculationRule.calculate(instance=policy, context='PolicyCreated', user=self.user)
        return Bill.objects.first()

    @patch.object(MusePaymentAdaptorConfig, 'certificate', new=test_certificate)
    def test_generate_message_from_bill(self):
        bill = self._get_bill()
        payload = self.api_client._build_request(bill, 'test_description')
        self.assertTrue(payload)

    @patch.object(MuseApiClient, '_submit', new=lambda self, x: None)
    @patch.object(MusePaymentAdaptorConfig, 'certificate', new=test_certificate)
    def test_generate_payment_request_model(self):
        bill = self._get_bill()
        payment_request, _ = self.api_client.submit_bulky_payment(bill, 'test_description')
        self.assertTrue(payment_request)

    @patch.object(MusePaymentAdaptorConfig, 'certificate', new=test_certificate)
    def test_generate_valid_message_signature(self):
        bill = self._get_bill()
        payload = self.api_client._build_request(bill, 'test_description').dict()
        signature_b64 = payload.pop('digitalSignature', None)
        self.assertTrue(verify_signature_b64_string(str.encode(json.dumps(payload)), signature_b64))
