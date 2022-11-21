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

    def __init__(self, url: str):
        """
        :param url: Root url for all request from this client
        """
        self.url = url

    def send_post_request(self, path: str, body: Any) -> Response:
        """
        Send POST request to the endpoint with a given data.

        :param path: Endpoint to send the data to. Will be joined with url provided in constructor
        :param body: Body arguments for POST request
        """
        url = self._build_url(path)
        try:
            return requests.post(url=url, data=body, headers=self._build_headers())
        except requests.exceptions.RequestException as e:
            logger.error("POST request to Muse API failed", exc_info=e)

    def _build_headers(self) -> dict:
        return MusePaymentAdaptorConfig.muse_request_headers

    def _build_url(self, uri, query_params=None) -> str:
        url = urljoin(self.url, uri)
        if query_params:
            url.query = urlencode(query_params)
        return url.geturl()
