import random
from datetime import datetime
from string import ascii_letters
from typing import Union, List

from django.test import TestCase
from django.urls import reverse
from requests import get, post
from rest_framework import status

from .clients import Visit


# Typings
# --------------------------------------------------------------------------------------------------
METHOD = Union[get, post]


class VisitTestMixin(TestCase):
    """Visit test cases."""

    method = None
    reverse_path = None

    def setUp(self):
        """Setup test case method."""

        self.visit_client = Visit()

    def tearDown(self):
        """Flushes Redis after every cache."""

        self.flush_redis()

    def flush_redis(self):
        """Flush Redis records."""

        self.visit_client._Visit__flush()  # NOQA

    @staticmethod
    def generate_domain_name(count: int, length: int = 10) -> List[str]:
        """
        Function that generates list of domain names.
        :param count: count of domain names
        :param length: length of domain name wo: protocol, sub-domain and top-level domain.
        :return: List[str]
        """

        return (
            [
                f'https://'
                f'{"".join(random.choice(ascii_letters) for _ in range(length))}'
                f'.com'
                for _ in range(count)

            ]
        )

    def make_request(self, client=None, data: dict = None):
        """
        Function that sends request to client.

        :param client: a class that can act as a client for testing purposes
        :param data: query parameters
        :return: requst object
        """

        if client is None:
            client = self.client

        return getattr(client, self.method.__name__)(
            path=reverse(self.reverse_path), content_type='application/json',
            HTTP_ACCEPT=f'application/json', data=data,
        )


class VisitShowTest(VisitTestMixin):

    method = get
    reverse_path = 'api:visit-visited-domains'

    def make_records(self, count: int):
        """
        Function that making records in Redis.
        :param count: count of Redis records
        """

        links = self.generate_domain_name(count)
        self.visit_client.register(links)

    def test_show_visit(self):
        """Test on retrieving count of registered objects."""

        start = datetime.now().timestamp()

        # make records
        # ------------
        records_count = 5
        self.make_records(records_count)

        # request params
        # --------------
        end = datetime.now().timestamp()

        query_params = {'from': start, 'to': end}
        response = self.make_request(client=self.client, data=query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('domains', list())), records_count)


class VisitRegisterTest(VisitTestMixin):

    method = post
    reverse_path = 'api:visit-visited-links'

    def test_register_resource(self):
        """Test on registering resources."""

        records_count = 5
        data = {'links': self.generate_domain_name(records_count)}

        start = datetime.now().timestamp()
        response = self.make_request(client=self.client, data=data)
        end = datetime.now().timestamp()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('status'), "ok")
        self.assertEqual(len(self.visit_client.find(start=start, end=end)), records_count)
