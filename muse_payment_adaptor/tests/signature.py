from unittest.mock import patch

from django.test import TestCase
from base64 import b64encode

from muse_payment_adaptor.api_interface.signature import create_signature, verify_signature
from muse_payment_adaptor.tests.helpers.signature_data import test_message, test_certificate, test_signature, \
    test_wrong_signature
from muse_payment_adaptor.apps import MusePaymentAdaptorConfig


class SignatureTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SignatureTests, cls).setUpClass()

    @patch.object(MusePaymentAdaptorConfig, 'certificate', new=test_certificate)
    def test_sign_message(self):
        signature = create_signature(test_message)
        self.assertTrue(signature)
        self.assertTrue(verify_signature(test_message, signature))

    @patch.object(MusePaymentAdaptorConfig, 'certificate', new=test_certificate)
    def test_verify_signature(self):
        self.assertTrue(verify_signature(test_message, test_signature))

    @patch.object(MusePaymentAdaptorConfig, 'certificate', new=test_certificate)
    def test_verify_signature_fail(self):
        self.assertFalse(verify_signature(test_message, test_wrong_signature))

