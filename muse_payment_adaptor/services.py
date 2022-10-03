import logging

from core.services import BaseService
from muse_payment_adaptor.models import HFBankInformation
from muse_payment_adaptor.validation import HFBankInformationValidation

logger = logging.getLogger(__name__)


class HFBankInformationService(BaseService):
    OBJECT_TYPE = HFBankInformation

    def __init__(self, user, validation_class=HFBankInformationValidation):
        super().__init__(user, validation_class)
