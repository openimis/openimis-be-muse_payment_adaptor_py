import logging
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from muse_payment_adaptor.gql_queries import HFBankInformationGQLType

logger = logging.getLogger(__name__)


class Query(graphene.ObjectType):
    hf_bank_information = DjangoFilterConnectionField(HFBankInformationGQLType)
