from importlib.metadata import requires
from muse_payment_adaptor.models import PaymentRequest, PaymentRequestDetails, PaymentResponse, PaymentResponseDetails
from rest_framework import serializers


class MessageHeader(serializers.Serializer):
    msgId = serializers.CharField(max_length=50, source="message_id")
    messageType = serializers.CharField(max_length=50)
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

        request.save()

        for payee in pay_list:
            PaymentRequestDetails.objects.create(
                payment_request=request, **payee)

        return request


class MessageSummary(serializers.Serializer):
    orgMsgId = serializers.CharField(max_length=50)
    status = serializers.CharField(max_length=50)
    statusDesc = serializers.CharField(max_length=200)


class BPPayList(serializers.Serializer):
    payeeCode = serializers.CharField(max_length=10, source="payee_code")
    endtoEndid = serializers.CharField(max_length=30, source="end_to_end")


class BulkPaymentSubmissionResponseMessage(serializers.Serializer):
    messageHeader = MessageHeader()
    messageSummary = MessageSummary()
    bPPaylist = serializers.ListField(child=BPPayList(), required=False)


class BulkPaymentResponseSerializer(serializers.Serializer):
    message = BulkPaymentSubmissionResponseMessage()

    def create(self, validated_data):
        header = validated_data["message"]["messageHeader"]
        summary = validated_data["message"]["messageSummary"]
        pay_list = {}
        if "bPPaylist" in validated_data["message"]:
            pay_list = validated_data["message"]["bPPaylist"]

        paymentRequest = PaymentRequest.objects.get(
            message_id=summary["orgMsgId"])

        response = PaymentResponse()
        response.payment_request = paymentRequest
        response.gateway_msg_id = header["message_id"]
        response.message_type = header["messageType"]
        response.payment_type = header["payment_type"]
        response.status = summary["status"]
        response.status_description = summary["statusDesc"]

        response.save()

        for payeeList in pay_list:
            PaymentResponseDetails.objects.create(
                response=response, **payeeList)

        return response


class PaymentSettlementMessageSummary(serializers.Serializer):
    createdAt = serializers.DateTimeField(source="settlement_date")


class PaymentSettlmentDetails(serializers.Serializer):
    orgReferenceNo = serializers.CharField(max_length=10, source="payee_code")
    overallStatus = serializers.CharField(max_length=20, source="status")
    overallStatusDesc = serializers.CharField(
        max_length=200, source="status_description")
    voucherNo = serializers.CharField(max_length=50, source="end_to_end")


class PaymentSettlementMessage(serializers.Serializer):
    messageHeader = MessageHeader()
    messageSummary = PaymentSettlementMessageSummary()
    settlementDetail = PaymentSettlmentDetails()


class PaymentSettlementSerializer(serializers.Serializer):
    message = PaymentSettlementMessage()

    def update(self, instance, validated_data):
        header = validated_data["message"]["messageHeader"]
        summary = validated_data["message"]["messageSummary"]
        settlement = validated_data["message"]["settlementDetail"]

        instance.settlement_msg_id = header.get(
            "message_id", instance.settlement_msg_id)
        instance.settlement_date = summary.get(
            "settlement_date", instance.settlement_date)
        instance.status = settlement.get("status", instance.status)
        instance.status_description = settlement.get(
            "status_description", instance.status_description)
        instance.save()
        return instance
