import pytest
from typing import Dict
from line import Line


class TestLine:
    @pytest.fixture()
    def line(self):
        line = Line()
        return line

    @pytest.mark.parametrize(
        "message", [({"type": "text", "text": "Hello World!!!!!!!!!!!!!!"}), ({})]
    )
    def test_push_message_ex(self, line: Line, message: Dict) -> None:
        line.push_message_ex(message)
