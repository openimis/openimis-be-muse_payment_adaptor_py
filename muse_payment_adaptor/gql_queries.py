import graphene
from graphene_django import DjangoObjectType
from core import ExtendedConnection
from muse_payment_adaptor.models import HFBankInformation


class HFBankInformationGQLType(DjangoObjectType):
    class Meta:
        model = HFBankInformation
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "health_facility__uuid": ["exact"],
            "bank_account": ["exact"],
            "bank_name": ["exact"],
            "account_name": ["exact"],
            "bic": ["exact"]
        }
        connection_class = ExtendedConnection
