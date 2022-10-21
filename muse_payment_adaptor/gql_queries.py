import graphene
from graphene_django import DjangoObjectType
from core import ExtendedConnection
from muse_payment_adaptor.models import HFBankInformation


class HFBankInformationGQLType(DjangoObjectType):
    uuid = graphene.String(source='uuid')

    class Meta:
        model = HFBankInformation
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "health_facility__uuid": ["exact"],
            "health_facility__code": ["exact"],
            "id": ["exact"],
            "bank_account": ["exact"],
            "bank_name": ["exact"],
            "account_name": ["exact"],
            "bic": ["exact"],

            "date_created": ["exact", "lt", "lte", "gt", "gte"],
            "date_updated": ["exact", "lt", "lte", "gt", "gte"],
            "is_deleted": ["exact"],
            "version": ["exact"],
        }
        connection_class = ExtendedConnection
