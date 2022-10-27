import logging
from typing import Any, List, Dict

import graphene
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from graphene_django.filter import DjangoFilterConnectionField

from core.schema import signal_mutation_module_after_mutating
from muse_payment_adaptor.apps import MusePaymentAdaptorConfig
from muse_payment_adaptor.gql_queries import HFBankInformationGQLType
from muse_payment_adaptor.models import HFBankInformation
from muse_payment_adaptor.services import HFBankInformationService
import graphene_django_optimizer as gql_optimizer

logger = logging.getLogger(__name__)


class Query(graphene.ObjectType):
    hf_bank_information = DjangoFilterConnectionField(HFBankInformationGQLType)

    def resolve_hf_bank_information(self, info, **kwargs):
        filters = []

        client_mutation_id = kwargs.get("client_mutation_id", None)
        if client_mutation_id:
            filters.append(Q(mutations__mutation__client_mutation_id=client_mutation_id))

        Query._check_permissions(info.context.user)
        return gql_optimizer.query(HFBankInformation.objects.filter(*filters).all(), info)

    @staticmethod
    def _check_permissions(user: Any) -> None:
        if type(user) is AnonymousUser or not user.id or not user.has_perms(
                MusePaymentAdaptorConfig.gql_hf_bank_info_search_perms):
            raise PermissionError("Unauthorized")


class MuseHFMutationExtension:
    _extensions = {
        "CreateHealthFacilityMutation": lambda x: MuseHFMutationExtension._after_create(**x),
        "UpdateHealthFacilityMutation": lambda x: MuseHFMutationExtension._after_update(**x),
        "DeleteHealthFacilityMutation": lambda x: MuseHFMutationExtension._after_delete(**x),
    }

    @classmethod
    def extend(cls, sender, **kwargs) -> List[Dict[str, str]]:
        return cls._extensions.get(sender._mutation_class, cls._empty_extension)(kwargs)

    @classmethod
    def _empty_extension(cls, **kwargs) -> List[Dict[str, str]]:
        return []

    @classmethod
    def _after_create(cls, **kwargs) -> List[Dict[str, str]]:
        if kwargs.get('error_messages', []):
            return cls._empty_extension()

        user = kwargs.get('user', None)
        hf_code = kwargs.get('data', {}).get('code', None)
        bank_info = kwargs.get('data', {}).get('mutation_extensions', {}).get('bank_account_info', {})

        if bank_info:
            result = HFBankInformationService(user).create_bank_info_for_hf(code=hf_code, bank_info=bank_info)
            return cls._parse_result(result)
        else:
            return cls._empty_extension()

    @classmethod
    def _after_update(cls, **kwargs) -> List[Dict[str, str]]:
        if kwargs.get('error_messages', []):
            return cls._empty_extension()

        user = kwargs.get('user', None)
        hf_uuid = kwargs.get('data', {}).get('uuid', None)
        bank_info = kwargs.get('data', {}).get('mutation_extensions', {}).get('bank_account_info', {})

        if bank_info:
            result = HFBankInformationService(user).update_bank_info_for_hf(uuid=hf_uuid, bank_info=bank_info)
        else:
            result = HFBankInformationService(user).delete_bank_info_for_hf(uuid=hf_uuid)

        return cls._parse_result(result)

    @classmethod
    def _after_delete(cls, **kwargs) -> List[Dict[str, str]]:
        if kwargs.get('error_messages', []):
            return cls._empty_extension()

        user = kwargs.get('user', None)
        hf_uuid = kwargs.get('data', {}).get('uuid', None)

        result = HFBankInformationService(user).delete_bank_info_for_hf(uuid=hf_uuid)
        return cls._parse_result(result)

    @classmethod
    def _parse_result(cls, result: dict) -> List[Dict[str, str]]:
        if result and not result.get('success', False):
            message = result.get("message", "Unknown")
            details = result.get("details", "No details")
            logger.warning(f'{message}, {details}')
            return [{'message': message, 'detail': details}]
        return []

    @staticmethod
    def _check_permissions(user, perms) -> None:
        if type(user) is AnonymousUser or not user.id or not user.has_perms(perms):
            raise PermissionError("Unauthorized")


def bind_signals():
    signal_mutation_module_after_mutating["location"].connect(MuseHFMutationExtension.extend)
