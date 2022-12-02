from muse_payment_adaptor.models import PaymentResponseDetails
from muse_payment_adaptor.serializer import BulkPaymentResponseSerializer, PaymentRequestSerializer, PaymentSettlementSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def make_bulk_payment(request):
    serializer = PaymentRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def bulk_payment_sub_req_ack(request):
    return Response({"data": request.data})


@api_view(['POST'])
def bulk_payment_sub_resp(request):
    serializer = BulkPaymentResponseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def payment_settlement(request):
    payee_code = request.data["message"]["settlementDetail"]["orgReferenceNo"]
    end_to_end = request.data["message"]["settlementDetail"]["voucherNo"]

    instance = PaymentResponseDetails.objects.filter(
        payee_code=payee_code, end_to_end=end_to_end).first()

    if instance is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PaymentSettlementSerializer(instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.validated_data)
    else:
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
