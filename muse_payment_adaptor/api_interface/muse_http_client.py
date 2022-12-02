import logging
from typing import Any
from urllib.parse import urljoin, urlencode

import requests
from requests import Response

from muse_payment_adaptor.apps import MusePaymentAdaptorConfig

logger = logging.getLogger(__name__)


class MuseAdaptorHttpClient:
    """
    Http client to be used for muse http requests
    """

    def __init__(self, root_url: str):
        """
        :param root_url: Root url for all request from this client
        """
        self.root_url = root_url

    def send_post_request(self, endpoint_url: str, body: Any) -> Response:
        """
        Send POST request to the endpoint with a given data.

        :param endpoint_url: Endpoint to send the data to. Will be joined with url provided in constructor
        :param body: Body arguments for POST request
        """
        url = self._build_url(endpoint_url)
        try:
            return requests.post(url=url, data=body, headers=self._build_headers())
        except requests.exceptions.RequestException as e:
            logger.error("POST request to Muse API failed", exc_info=e)

    def _build_headers(self) -> dict:
        return MusePaymentAdaptorConfig.muse_request_headers

    def _build_url(self, endpoint_url, query_params=None) -> str:
        url = urljoin(self.root_url, endpoint_url)
        if query_params:
            url.query = urlencode(query_params)
        return url.geturl()

    @staticmethod
    def get_default():
        return MuseAdaptorHttpClient(MusePaymentAdaptorConfig.muse_base_uri)
