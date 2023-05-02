import json
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
            content_type = response.headers.get('Content-Type')
            logging.info(f"Status code: {response.status_code} {curlify.to_curl(response.request)}")
            logging.info(response.text)
            logging.info(content_type)
            #
            allure.attach(f"Status code: {response.status_code} {curlify.to_curl(response.request)}", name="Text", attachment_type=allure.attachment_type.TEXT)
            # allure.attach(response.text, name="HTTP Response",
            #               attachment_type=allure.attachment_type.TEXT)
            attachments_dict = {
                'text/plain': (response.text, 'Text response', allure.attachment_type.TEXT),
                'text/html': (response.text, 'Text response', allure.attachment_type.TEXT),
                'application/json': (response.text, 'JSON response', allure.attachment_type.JSON),
                'application/xml': (response.text, 'XML response', allure.attachment_type.XML),
                'application/pdf': (response.content, 'PDF response', allure.attachment_type.PDF),
                'image/jpeg': (response.content, 'Image response', allure.attachment_type.PNG),
                'image/png': (response.content, 'Image response', allure.attachment_type.PNG),
                'image/gif': (response.content, 'Image response', allure.attachment_type.PNG),
            }
            if content_type in attachments_dict.keys():
                attachment_args = attachments_dict[content_type]
                allure.attach(*attachment_args)
            else:
                allure.attach(response.content, 'Unknown response',
                          allure.attachment_type.TEXT)
        return response