import logging

from core.services import BaseService
from core.services.utils import build_delete_instance_payload, output_exception, check_authentication
from core.services.utils.serviceUtils import check_permissions
from location.models import HealthFacility
from muse_payment_adaptor.apps import MusePaymentAdaptorConfig
from muse_payment_adaptor.models import HFBankInformation
from muse_payment_adaptor.validation import HFBankInformationValidation

logger = logging.getLogger(__name__)


class HFBankInformationService(BaseService):
    OBJECT_TYPE = HFBankInformation

    def __init__(self, user, validation_class=HFBankInformationValidation):
        super().__init__(user, validation_class)

    @check_permissions(permissions=MusePaymentAdaptorConfig.gql_hf_bank_info_create_perms)
    def create(self, obj_data: dict) -> dict:
        return super(HFBankInformationService, self).create(obj_data)

    @check_permissions(permissions=MusePaymentAdaptorConfig.gql_hf_bank_info_update_perms)
    def update(self, obj_data: dict) -> dict:
        return super(HFBankInformationService, self).update(obj_data)

    @check_permissions(permissions=MusePaymentAdaptorConfig.gql_hf_bank_info_delete_perms)
    def delete(self, obj_data: dict) -> dict:
        return super(HFBankInformationService, self).delete(obj_data)

    def create_bank_info_for_hf(self, **kwargs) -> dict:
        try:
            bank_info = self._get_bank_info(**kwargs)
            hf = self._get_hf(**{'validity_to': None, **kwargs})
            bank_info['health_facility'] = hf
            return self.create(bank_info)
        except BaseException as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="create_bank_info_for_hf",
                                    exception=exc)

    def update_bank_info_for_hf(self, **kwargs) -> dict:
        try:
            bank_info = self._get_bank_info(**kwargs)
            hf = self._get_hf(**{'validity_to': None, **kwargs})
            queryset = HFBankInformation.objects.filter(health_facility=hf, is_deleted=False)
            if queryset:
                bank_info_ = queryset.first()
                data = bank_info.copy()
                data['id'] = bank_info_.uuid
                return self.update(data)
            else:
                return self.create_bank_info_for_hf(**{'hf': hf, "bank_info": bank_info, **kwargs})
        except BaseException as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="update_bank_info_for_hf",
                                    exception=exc)

    def delete_bank_info_for_hf(self, **kwargs) -> dict:
        try:
            hf = self._get_hf(**kwargs)
            queryset = HFBankInformation.objects.filter(health_facility=hf, is_deleted=False)
            if queryset.count() == 1:
                return self.delete({'id': queryset.first().uuid})
            elif queryset.count() > 1:
                logger.warning(f'Multiple bank accounts for deleted HF {hf.uuid}')
                [self.delete({'id': hf_bank_info.uuid}) for hf_bank_info in queryset]
            return build_delete_instance_payload()
        except BaseException as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="delete_bank_account_for_hf",
                                    exception=exc)

    @staticmethod
    def _get_bank_info(**kwargs):
        bank_info = kwargs.get('bank_info', None)
        if bank_info:
            return bank_info
        else:
            raise AttributeError('Bank information not provided')

    @staticmethod
    def _get_hf(**kwargs):
        hf = None

        if 'hf' in kwargs:
            hf = kwargs.get('hf', None)
        elif 'code' in kwargs:
            hf = HealthFacility.objects.get(code=kwargs['code'])
        elif 'uuid' in kwargs:
            hf = HealthFacility.objects.get(uuid=kwargs['uuid'])

        if hf:
            return hf
        else:
            raise AttributeError(f'HF information not provided. HF bank info updated')
