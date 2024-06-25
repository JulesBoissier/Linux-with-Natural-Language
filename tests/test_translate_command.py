import unittest
from unittest.mock import patch, Mock

from src.translate_command import translate_command, add_sudo_prefix, strip_bash_artefacts

class TestTranslateCommand(unittest.TestCase):

    def test_add_sudo_prefix(self):
        command = 'ls -la'

        sudo_command = add_sudo_prefix(translated_command = command)

        self.assertEqual(f'sudo {command}', sudo_command)

    def test_strip_bash_artefacts(self):
        test_cases = [
            ("```bash\nls -la\n```", "ls -la"),  # Simple case with bash tags
            ("```bash\necho 'Hello, World!'\n```", "echo 'Hello, World!'"),  # Bash tags with an echo command
            ("```bash\napt-get update && apt-get upgrade\n```", "apt-get update && apt-get upgrade"),  # Bash tags with multiple commands
            ("```bash\n   python3 script.py\n```", "python3 script.py"),  # Bash tags with leading spaces
            ("ls -la", "ls -la"),  # No bash tags
            ("```bash\nls -la", "ls -la"),  # Missing closing tag
            ("```bash```", "")  # Empty bash block
        ]

        for input_str, expected_output in test_cases:
            result: str = strip_bash_artefacts(input_str)
            self.assertEqual(result, expected_output)

    @patch(
        "src.translate_command.client.chat.completions.create"
    )
    def test_explain_command(self, mock_create):
        pass

    # @patch(
    #     "src.translate_command.client.chat.completions.create"
    # )
    # def test_add_sudo_prefix(self, mock_create):
    #     mock_completion = Mock()
    #     mock_completion.choices = [Mock()]
    #     mock_completion.choices[0].message = Mock()
    #     mock_completion.choices[0].message.content = 'Hello'
    #     mock_create.return_value = mock_completion

    #     command = translate_command(query='Hey', sudo=True)

    #     self.assertEqual('sudo Hello', command)