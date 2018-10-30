from unittest import TestCase

from core.check_pin_usecase import CheckPinUsecase


class TestCheckPinUsecase(TestCase):
    def setUp(self):
        self.usecase = CheckPinUsecase((123, 456))

    def test_valid(self):
        result = self.usecase.execute(123)

        assert result is True

    def test_invalid(self):
        result = self.usecase.execute(789)

        assert result is False
