from typing import Collection
from urllib.parse import urljoin, urlencode

import requests

from invoice.models import Bill
from muse_payment_adaptor.api_interface.dataclasses.bulkyPayment import PayListElement, PaymentSummary, \
    BulkyPaymentSubmissionMessage, BulkyPaymentSubmissionRequest
from muse_payment_adaptor.api_interface.dataclasses.generic import MessageHeader


class MuseAdaptorClient:

    def __init__(self, url, digital_signature):
        self.url = url
        self.signature = digital_signature

    def build_headers(self):
        return {
            'content-type': 'application/JSON',
            'MUSE-Com': 'default.sp.in',
            'Institution Code': 'IMIS',
            'service-code': 'SRVC044'  # TODO: Remove, for test instance only
        }

    def send_get_request(self, uri: str, query_params: dict):
        url = self._build_url(uri, query_params)
        with requests.Session() as s:
            s.get(url, headers=self.build_headers())

    def send_post_request(self, uri: str, body: dict, query_params: dict):
        url = self._build_url(uri, query_params)
        return requests.post(url=url, data=body)

    def _build_url(self, uri, query_params):
        url = urljoin(self.url, uri)
        url.query = urlencode(query_params)
        return url.geturl()


class BulkyPaymentClient:
    def __init__(self, api_client: MuseAdaptorClient):
        self.api_client = api_client

    def submit(self, bills: Collection[Bill]):
        message_header = self._build_message_header()
        pay_list = []
        for bill in bills:
            pay_list.append(self._build_bill_pay_element(bill))
        payment_batch = self._build_payment_batch(pay_list)
        payment_submission_message = self._build_payment_submission_message(
            message_header, payment_batch, pay_list
        )
        payment_submission_request = self._build_payment_submission_request(
            payment_submission_message
        )

    def _build_message_header(self) -> MessageHeader:
        ...

    def _build_bill_pay_element(self, bill: Bill) -> PayListElement:
        ...

    def _build_payment_batch(self, pay_list: Collection[PayListElement]) -> PaymentSummary:
        ...

    def _build_payment_submission_message(self, header, payment_batch, pay_list) -> BulkyPaymentSubmissionMessage:
        ...

    def _build_payment_submission_request(self, submission_message) -> BulkyPaymentSubmissionRequest:
        ...
