from muse_payment_adaptor.models import PaymentRequest, PaymentRequestDetails
from rest_framework import serializers
from django.core import serializers as json_serializer


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

    def create(self, validated_data):
        header = validated_data["message"]["messageHeader"]
        summary = validated_data["message"]["paymentSummary"]
        pay_list = validated_data["message"]["payList"]

        request = PaymentRequest()
        request.message_id = header["message_id"]
        request.payment_type = header["payment_type"]
        request.reference_no = summary["reference_no"]
        request.total_amount = summary["total_amount"]
        request.no_of_tnx = summary["no_of_tnx"]
        request.payment_date = summary["payment_date"]
        request.payment_description = summary["payment_description"]

        # payment_data = json_serializer.serialize('json', [request])
        # payment = PaymentRequest.objects.create(**payment_data)

        request.save()

        for payee in pay_list:
            PaymentRequestDetails.objects.create(
                payment_request_id=request, **payee)

        return request
