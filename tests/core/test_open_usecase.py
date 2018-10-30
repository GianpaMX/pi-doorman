from unittest import TestCase
from unittest.mock import MagicMock

from core.open_usecase import OpenUsecase


class TestOpenUsecase(TestCase):
    def setUp(self):
        self.door_gateway = MagicMock()

        self.usecase = OpenUsecase(self.door_gateway)

    def test_open(self):
        self.usecase.execute()

        self.door_gateway.open.assert_called()
