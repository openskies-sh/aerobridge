import os

from django.test import TransactionTestCase
from faker import Faker

from ..aerobridge_tests_base import AerobridgeTestsBase


class TestModels(TransactionTestCase, AerobridgeTestsBase):
    data_path = os.getcwd() + '/tests/fixtures/'

    @classmethod
    def setUpClass(cls):
        cls.faker = Faker()

    @classmethod
    def tearDownClass(cls):
        pass
