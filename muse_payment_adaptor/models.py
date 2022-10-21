from core.models import HistoryBusinessModel
from location.models import HealthFacility
from pyexpat import model
import uuid
from django.db import models


class PaymentRequest(models.Model):
    id = models.UUIDField(db_column="Id", primary_key=True, default=uuid.uuid4)
    message_id = models.CharField(
        db_column="MessageId", blank=False, null=False, max_length=50)
    payment_type = models.CharField(
        db_column="PaymentId", blank=True, null=True, max_length=50)
    reference_no = models.CharField(
        db_column="ReferenceNo", blank=True, null=True, max_length=50)
    total_amount = models.DecimalField(
        db_column="TotalAmount", blank=True, null=True, max_digits=18, decimal_places=4)
    no_of_tnx = models.IntegerField(
        db_column="NoOfTnx", blank=True, null=True)
    payment_date = models.DateField(
        db_column="PaymentDate", blank=True, null=True)
    status = models.CharField(
        db_column="Status", blank=True, null=True, max_length=10)
    record_date = models.DateTimeField(
        db_column="RecordDate", null=False, blank=False, auto_now=True)

    class Meta:
        db_table = "PaymentRequest"


class PaymentRequestDetails(models.Model):
    id = models.UUIDField(db_column="Id", primary_key=True, default=uuid.uuid4)
    payment_request_id = models.ForeignKey(
        PaymentRequest, models.DO_NOTHING, db_column="PaymentRequestId", blank=True, null=True)
    payee_code = models.CharField(
        db_column="PayeeCode", blank=True, null=True, max_length=10)
    name = models.CharField(
        db_column="Name", blank=True, null=True, max_length=50)
    acc_no = models.CharField(
        db_column="AccNo", blank=True, null=True, max_length=20)
    acc_name = models.CharField(
        db_column="AccName", blank=True, null=True, max_length=100)
    bank = models.CharField(
        db_column="Bank", blank=True, null=True, max_length=50)
    bank_bic = models.CharField(
        db_column="BankBIC", blank=True, null=True, max_length=50)
    amount = models.DecimalField(
        db_column="Amount", blank=True, null=True, max_digits=18, decimal_places=4)
    payment_channel = models.CharField(
        db_column="PaymentChannel", blank=True, null=True, max_length=50)

    class Meta:
        db_table = "PaymentRequestDetails"


class PaymentResponse(models.Model):
    id = models.UUIDField(db_column="Id", primary_key=True, default=uuid.uuid4)
    payment_request_id = models.ForeignKey(
        PaymentRequest, models.DO_NOTHING, db_column="PaymentRequestId", blank=True, null=True)
    gateway_msg_id = models.CharField(
        db_column="GatewayMsgId", blank=True, null=True, max_length=50)
    message_type = models.CharField(
        db_column="MessageType", blank=True, null=True, max_length=20)
    payment_type = models.CharField(
        db_column="PaymentType", blank=True, null=True, max_length=20)
    response_date = models.DateTimeField(
        db_column="ResponseDate", blank=True, null=True)
    status = models.CharField(
        db_column="Status", blank=True, null=True, max_length=20)
    status_description = models.CharField(
        db_column="StatusDescription", blank=True, null=True, max_length=200)
    record_date = models.DateTimeField(
        db_column="RecordDate", blank=False, null=False, auto_now=True)

    class Meta:
        db_table = "PaymentResponse"


class PaymentResponseDetails(models.Model):
    id = models.UUIDField(db_column="Id", primary_key=True, default=uuid.uuid4)
    response_id = models.ForeignKey(
        PaymentResponse, models.DO_NOTHING, db_column="ResponseId", blank=True, null=True)
    gateway_msg_id = models.CharField(
        db_column="GatewayMsgId", blank=True, null=True, max_length=50)
    payee_code = models.CharField(
        db_column="PayeeCode", blank=True, null=True, max_length=10)
    end_to_end = models.CharField(
        db_column="EndToEnd", blank=True, null=True, max_length=50)
    status = models.CharField(
        db_column="Status", blank=True, null=True, max_length=20)
    status_description = models.CharField(
        db_column="StatusDescription", blank=True, null=True, max_length=200)
    record_date = models.DateTimeField(
        db_column="RecordDate", blank=False, null=False, auto_now=True)

    class Meta:
        db_table = "PaymentResponseDetails"


class HFBankInformation(HistoryBusinessModel):
    health_facility = models.ForeignKey(
        HealthFacility, models.DO_NOTHING, db_column='HFId', blank=True, null=True)
    account_name = models.CharField(
        db_column='AccountName', max_length=50, blank=True, null=True)
    bank_account = models.CharField(
        db_column='BankAccount', max_length=50, blank=True, null=True)
    bank_name = models.CharField(
        db_column='BankName', max_length=50, blank=True, null=True)
    bic = models.CharField(
        db_column='BIC', max_length=11, blank=False, null=True)

    class Meta:
        managed = True
        db_table = "tblHFBankInformation"
