from muse_payment_adaptor.models import PaymentRequest
from rest_framework import serializers


class MessageHeader(serializers.Serializer):
    msgId = serializers.CharField(max_length=50, source="message_id")
    paymentType = serializers.CharField(max_length=50, source="payment_type")


class PaymentSummary(serializers.Serializer):
    referenceNo = serializers.CharField(max_length=50, source="reference_no")
    paymentDesc = serializers.CharField(
        max_length=300, source="payment_description")
    totalAmount = serializers.DecimalField(
        max_digits=18, decimal_places=4, source="total_amount")
    noofTransaction = serializers.IntegerField(source="no_of_tnx")
    applyDate = serializers.DateTimeField(source="payment_date")


class PaymentRequestDetailsSerializer(serializers.Serializer):
    payeeCode = serializers.CharField(max_length=10, source="payee_code")
    payeeName = serializers.CharField(max_length=50, source="name")
    payeeAccountNumber = serializers.CharField(max_length=20, source="acc_no")
    payeeAccountName = serializers.CharField(max_length=100, source="acc_name")
    payeeBankName = serializers.CharField(max_length=50, source="bank")
    payeeBankBic = serializers.CharField(max_length=50, source="bank_bic")
    amount = serializers.DecimalField(
        max_digits=18, decimal_places=4)
    paymentChannel = serializers.CharField(
        max_length=50, source="payment_channel")


class BulkPaymentMessage(serializers.Serializer):
    messageHeader = MessageHeader()
    paymentSummary = PaymentSummary()
    payList = serializers.ListField(child=PaymentRequestDetailsSerializer())


class PaymentRequestSerializer(serializers.Serializer):
    message = BulkPaymentMessage()
