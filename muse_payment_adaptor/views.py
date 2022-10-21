from muse_payment_adaptor.serializer import PaymentRequestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def make_bulk_payment(request):
    serializer = PaymentRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def bulk_payment_sub_req_ack(request):
    return Response({"data": request.data})


@api_view(['POST'])
def bulk_payment_sub_resp(request):
    return Response({"data": request.data})
