from unittest import TestCase
from unittest.mock import MagicMock

from core.ring_bell_usecase import RingBellUsecase


class TestRingBell(TestCase):
    def setUp(self):
        self.door_gateway = MagicMock()
        self.usecase = RingBellUsecase(self.door_gateway)

    def test_ring_bell(self):
        self.usecase.execute()

        self.door_gateway.ring_bell.assert_called()
