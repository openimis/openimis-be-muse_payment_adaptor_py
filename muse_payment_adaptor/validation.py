from core.validation import BaseModelValidation
from muse_payment_adaptor.models import HFBankInformation


class HFBankInformationValidation(BaseModelValidation):
    OBJECT_TYPE = HFBankInformation

    @classmethod
    def validate_create(cls, user, **data):
        super().validate_create(user, **data)

    @classmethod
    def validate_update(cls, user, **data):
        super().validate_update(user, **data)

    @classmethod
    def validate_delete(cls, user, **data):
        super().validate_delete(user, **data)
