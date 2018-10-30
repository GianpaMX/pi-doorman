from unittest import TestCase
from unittest.mock import MagicMock

from core.open_usecase import OpenUsecase


class TestOpenUsecase(TestCase):
    def setUp(self):
        self.door_gateway = MagicMock()

        self.usecase = OpenUsecase((123, 456), self.door_gateway)

    def test_valid_pin_open(self):
        self.usecase.execute(123)

        self.door_gateway.open.assert_called()

    def test_invalid_pin_open(self):
        self.usecase.execute(789)

        self.door_gateway.open.assert_not_called()
