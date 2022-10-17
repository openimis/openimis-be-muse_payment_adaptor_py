import logging

from core.services import BaseService
from core.services.utils import build_delete_instance_payload, output_exception
from location.models import HealthFacility
from muse_payment_adaptor.models import HFBankInformation
from muse_payment_adaptor.validation import HFBankInformationValidation

logger = logging.getLogger(__name__)


class HFBankInformationService(BaseService):
    OBJECT_TYPE = HFBankInformation

    def __init__(self, user, validation_class=HFBankInformationValidation):
        super().__init__(user, validation_class)

    def create_bank_info_for_hf(self, **kwargs):
        try:
            bank_info = kwargs.pop('bank_info', None)
            hf = self._get_hf(**kwargs | {'validity_to': None})
            if hf:
                bank_info['health_facility'] = hf
                return self.create(bank_info)
            else:
                return output_exception(model_name=self.OBJECT_TYPE.__name__, method="create_bank_info_for_hf",
                                        exception="HF not found")
        except BaseException as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="create_bank_info_for_hf",
                                    exception=exc)

    def update_bank_info_for_hf(self, **kwargs):
        try:
            bank_info = kwargs.pop('bank_info', None)
            hf = self._get_hf(**kwargs | {'validity_to': None})
            queryset = HFBankInformation.objects.filter(health_facility=hf, is_deleted=False)
            if queryset:
                bank_info_ = queryset.first()
                data = bank_info.copy()
                data['id'] = bank_info_.uuid
                return self.update(data)
            else:
                return self.create_bank_info_for_hf(**(kwargs | {'hf': hf, "bank_info": bank_info}))
        except BaseException as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="update_bank_info_for_hf",
                                    exception=exc)

    def delete_bank_info_for_hf(self, **kwargs):
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
    def _get_hf(**kwargs):
        if 'hf' in kwargs:
            return kwargs.get('hf', None)
        elif 'code' in kwargs or 'uuid' in kwargs:
            return HealthFacility.objects.get(**kwargs)
        else:
            raise AttributeError(f'HF information not provided. HF bank info updated')
