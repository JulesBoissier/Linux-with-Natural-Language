import unittest
from unittest.mock import patch, Mock

from __main__ import translate_command

class TestTranslateCommand(unittest.TestCase):

    @patch(
        "linux_with_natural_language.__main__.client.chat.completions.create"
    )
    def test_sudo(self, mock_create):
        mock_completion = Mock()
        mock_completion.choices = [Mock()]
        mock_completion.choices[0].message = Mock()
        mock_completion.choices[0].message.content = 'Hello'
        mock_create.return_value = mock_completion

        command = translate_command(query='Hey', sudo=True)

        self.assertEqual('sudo Hello', command)