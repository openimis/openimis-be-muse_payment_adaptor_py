import json
import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import BaseModel

from core.datetimes.ad_datetime import datetime
from invoice.models import Bill, BillItem
from muse_payment_adaptor.api_interface.dataclasses import BulkyPaymentSubmissionRequest, \
    BulkyPaymentSubmissionRequestMessage, BulkyPaymentMessageHeader, BulkyPaymentSummary, BulkyPaymentPayListElement
from muse_payment_adaptor.api_interface.muse_http_client import MuseAdaptorHttpClient
from muse_payment_adaptor.api_interface.signature import create_signature_b64_string
from muse_payment_adaptor.apps import MusePaymentAdaptorConfig
from muse_payment_adaptor.models import PaymentRequest, PaymentRequestDetails

logger = logging.getLogger(__name__)


class MuseApiClient(ABC):
    def __init__(self, api_http_client: MuseAdaptorHttpClient = MuseAdaptorHttpClient.get_default()):
        self.api_http_client = api_http_client

    @property
    @abstractmethod
    def _api_endpoint(self) -> str:
        """
        This property specifies the exact endpoint to be used by the client. The endpoint will be joined with root path
        from the MuseAdaptorHttpClient.
        """

    def _submit(self, model: BaseModel) -> Optional[str]:
        response = self.api_http_client.send_post_request(self._api_endpoint, model.json())
        if response:
            if response.ok:
                return response.content.decode('utf-8')
            else:
                logger.error(f"Muse request failed, HTTP code %s", response.status_code)
                if response.content:
                    logger.error(f"Response content %s", response.content.decode('utf-8'))

    def _build_message_signature(self, message: BaseModel) -> str:
        # To JSON, To UTF-8 bytes
        encoded_msg = json.dumps({'message': message.dict()}).encode('utf-8')
        # Create signature bytes, To b64 bytes, To b64 string (ascii)
        signature_str = create_signature_b64_string(encoded_msg)
        return signature_str


class BulkPaymentSubmissionClient(MuseApiClient):
    _api_endpoint = MusePaymentAdaptorConfig.muse_post_bp_endpoint

    def submit_bulky_payment(self, bill: Bill, payment_desc: str = '') -> Optional[str]:
        """
        Submit Bill as bulky payment to MUSE Api. This method will send the submission and save the request in the
        database.

        :param bill: Bill to be submitted
        :param payment_desc: Payment description to be included with the submission
        :return: response content, if the request is successful
        """
        try:
            request = self._build_request(bill, payment_desc)
            self._store_request(request)
            # TODO update model after submit?
            return self._submit(request)
        except BaseException as e:
            logger.error("Error while sending MUSE request", exc_info=e)
            return None

    def _build_request(self, bill: Bill, description: str) -> BulkyPaymentSubmissionRequest:
        message = self._build_request_message(bill, description)
        signature = self._build_message_signature(message)
        return BulkyPaymentSubmissionRequest(
            message=message,
            digitalSignature=signature
        )

    def _build_request_message(self, bill: Bill, description: str) -> BulkyPaymentSubmissionRequestMessage:
        message_header = self._build_request_message_header(bill)
        message_content = self._build_request_message_summary(bill, description)
        pay_list = self._build_request_pay_list(bill)
        return BulkyPaymentSubmissionRequestMessage(
            messageHeader=message_header,
            paymentSummary=message_content,
            payList=pay_list,
        )

    def _build_request_message_header(self, bill: Bill) -> BulkyPaymentMessageHeader:
        return BulkyPaymentMessageHeader(
            sender=MusePaymentAdaptorConfig.muse_api_sender,
            receiver=MusePaymentAdaptorConfig.muse_api_receiver,
            msgId=str(bill.uuid),
            messageType=MusePaymentAdaptorConfig.muse_bp_header_message_type,
            paymentType=MusePaymentAdaptorConfig.muse_bp_header_payment_type,
        )

    def _build_request_message_summary(self, bill: Bill, description: str) -> BulkyPaymentSummary:
        return BulkyPaymentSummary(
            institutioncode=MusePaymentAdaptorConfig.muse_bp_message_institution_code,
            totalAmount=bill.amount_net,
            referenceNo=str(bill.uuid),
            paymentDesc=description,
            applyDate=datetime.now().isoformat(),
            noofTransaction=bill.line_items_bill.count(),
            isSTP=False,
        )

    def _build_request_pay_list(self, bill: Bill) -> List[BulkyPaymentPayListElement]:
        pay_list = []
        for bill_item in bill.line_items_bill.all():
            pay_list.append(self._build_request_pay_list_element(bill_item))
        return pay_list

    def _build_request_pay_list_element(self, line_item: BillItem) -> BulkyPaymentPayListElement:
        return BulkyPaymentPayListElement(
            paymentChannel='',
            payeeCode='',
            payeeName='',
            payeeAccountNumber='',
            payeeAccountName='',
            payeeBankName='',
            payeeBankBic='',
            amount=line_item.amount_net,
        )  # TODO API call to request this info ?

    def _store_request(self, request: BulkyPaymentSubmissionRequest) -> PaymentRequest:
        request_model = PaymentRequest.objects.create(**{
            'message_id': request.message.messageHeader.msgId,
            'payment_type': request.message.messageHeader.paymentType,
            'reference_no': request.message.paymentSummary.referenceNo,
            'payment_description': request.message.paymentSummary.paymentDesc,
            'total_amount': request.message.paymentSummary.totalAmount,
            'no_of_tnx': len(request.message.payList),
            'status': None,
            'record_date': datetime.now(),
        })

        for pay_list_item in request.message.payList:
            PaymentRequestDetails.objects.create(**{
                'payment_request': request_model,
                'payee_code': pay_list_item.payeeCode,
                'name': pay_list_item.payeeName,
                'acc_no': pay_list_item.payeeAccountNumber,
                'acc_name': pay_list_item.payeeAccountName,
                'bank': pay_list_item.payeeBankBic,
                'bank_bic': pay_list_item.payeeBankBic,
                'amount': pay_list_item.amount,
                'payment_channel': pay_list_item.paymentChannel,
            })

        return request_model
