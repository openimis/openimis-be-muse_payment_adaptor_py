from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def bulk_payment_sub_req_ack(request):
    return Response({"data": request.data})


@api_view(['POST'])
def bulk_payment_sub_resp(request):
    return Response({"data": request.data})
