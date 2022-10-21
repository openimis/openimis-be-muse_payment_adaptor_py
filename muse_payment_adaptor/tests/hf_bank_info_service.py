from django.test import TestCase

from core import TimeUtils
from core.models import User
from muse_payment_adaptor.helpers.data import test_hf_data, test_hf_bank_info_data
from muse_payment_adaptor.models import HFBankInformation
from muse_payment_adaptor.services import HFBankInformationService

from location.services import HealthFacilityService


class HFBankInformationServiceTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(HFBankInformationServiceTests, cls).setUpClass()

        if not User.objects.filter(username='admin_muse').exists():
            User.objects.create_superuser(username='admin_muse', password='S\/pe®Pąßw0rd™')

        cls.user = User.objects.filter(username='admin_muse').first()
        cls.service = HFBankInformationService(cls.user)
        cls.hf = HealthFacilityService(cls.user).update_or_create(test_hf_data)

    def test_add_bank_info_to_hf(self):
        result = self.service.create_bank_info_for_hf(**{'bank_info': test_hf_bank_info_data, 'hf': self.hf})
        self.assertTrue(result['success'])

    def test_add_bank_info_to_hf_uuid(self):
        result = self.service.create_bank_info_for_hf(**{'bank_info': test_hf_bank_info_data, 'uuid': self.hf.uuid})
        self.assertTrue(result['success'])

    def test_add_bank_info_to_hf_code(self):
        result = self.service.create_bank_info_for_hf(**{'bank_info': test_hf_bank_info_data, 'code': self.hf.code})
        self.assertTrue(result['success'])

    def test_update_bank_info_to_hf(self):
        updated_bank_name = 'updated bank name'
        result_create = self.service.create_bank_info_for_hf(**{'bank_info': test_hf_bank_info_data, 'hf': self.hf})
        self.assertTrue(result_create['success'])
        result_update = self.service.update_bank_info_for_hf(
            **{'bank_info': test_hf_bank_info_data | {'bank_name': updated_bank_name}, 'hf': self.hf})
        self.assertTrue(result_update['success'])
        model = HFBankInformation.objects.get(uuid=result_update['data']['uuid'])
        self.assertEqual(updated_bank_name, model.bank_name)

    def test_delete_bank_info_to_hf(self):
        result_create = self.service.create_bank_info_for_hf(**{'bank_info': test_hf_bank_info_data, 'hf': self.hf})
        self.assertTrue(result_create['success'])
        result_delete = self.service.delete_bank_info_for_hf(**{'hf': self.hf})
        self.assertTrue(result_delete['success'])
        model = HFBankInformation.objects.get(uuid=result_create['data']['uuid'])
        self.assertTrue(model.is_deleted)

    def test_create_bank_info_no_hf(self):
        result = self.service.create_bank_info_for_hf(**{'bank_info': test_hf_bank_info_data,})
        self.assertFalse(result['success'])

    def test_create_bank_info_no_bank_info(self):
        result = self.service.create_bank_info_for_hf(**{'hf': self.hf})
        self.assertFalse(result['success'])
