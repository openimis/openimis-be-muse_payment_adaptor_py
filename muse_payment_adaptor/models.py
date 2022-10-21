from django.db import models

from core.models import HistoryBusinessModel
from location.models import HealthFacility


class HFBankInformation(HistoryBusinessModel):
    health_facility = models.ForeignKey(HealthFacility, models.DO_NOTHING, db_column='HFId', blank=True, null=True)
    account_name = models.CharField(db_column='AccountName', max_length=50, blank=True, null=True)
    bank_account = models.CharField(db_column='BankAccount', max_length=50, blank=True, null=True)
    bank_name = models.CharField(db_column='BankName', max_length=50, blank=True, null=True)
    bic = models.CharField(db_column='BIC', max_length=11, blank=False, null=True)

    class Meta:
        managed = True
        db_table = "tblHFBankInformation"
