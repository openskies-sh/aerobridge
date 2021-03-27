from django.test import TransactionTestCase
from faker import Faker


class TestModels(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.faker = Faker()

    @classmethod
    def tearDownClass(cls):
        pass
