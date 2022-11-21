from . import views
from django.urls import path

urlpatterns = [
    path('bulkpayment', views.make_bulk_payment, name='bulkpayment'),
    path('ack', views.bulk_payment_sub_req_ack, name='ack'),
    path('resp', views.bulk_payment_sub_resp, name="resp"),
    path('settlement', views.payment_settlement, name='settlement')
]
