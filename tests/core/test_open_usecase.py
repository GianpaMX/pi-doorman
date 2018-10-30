from unittest import TestCase
from unittest.mock import Mock

from core.open_usecase import OpenUsecase


class TestOpenUsecase(TestCase):
    def setUp(self):
        self.door_gateway = Mock()

        self.usecase = OpenUsecase(self.door_gateway)

    def test_open(self):
        self.usecase.execute()

        self.door_gateway.open.assert_called()
