import logging

import allure
import curlify
from allure import step
from requests import Session


class BaseSession(Session):
    def __init__(self, **kwargs):
        self.base_url = kwargs.pop('base_url')
        super().__init__()

    def request(self, method, url, **kwargs):
        with step(f'{method} {url}'):
            response = super().request(method=method, url=f'{self.base_url}{url}', **kwargs)
            logging.info(f"Status code: {response.status_code} {curlify.to_curl(response.request)}")
            logging.info(response.text)
            allure.attach(f"Status code: {response.status_code} {curlify.to_curl(response.request)}", name="Text",
                          attachment_type=allure.attachment_type.TEXT)
            allure.attach(response.text, name="HTTP Response",
                          attachment_type=allure.attachment_type.TEXT)
        return response