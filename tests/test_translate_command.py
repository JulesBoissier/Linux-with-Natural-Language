import unittest
from unittest.mock import _Call, patch, Mock, call

from src.translate_command import (
    translate_command,
    explain_command,
    add_sudo_prefix,
    strip_bash_artefacts,
    TRANSLATION_SYSTEM_PROMPT,
    EXPLANATION_SYSTEM_PROMPT,
)

def test_add_sudo_prefix():
    command = 'ls -la'

    sudo_command = add_sudo_prefix(translated_command = command)

    assert f'sudo {command}' == sudo_command

def test_strip_bash_artefacts():
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
        assert result == expected_output

@patch(
    "src.translate_command.client.chat.completions.create"
)
def test_explain_command(mock_create):

    explanation = 'This is an explanation of the provided command.'

    mock_completion = Mock()
    mock_completion.choices = [Mock()]
    mock_completion.choices[0].message = Mock()
    mock_completion.choices[0].message.content = explanation
    mock_create.return_value = mock_completion

    result = explain_command(command = '', model = '')

    assert result ==  "Explanation: \n" + explanation


class TestTranslateCommand(unittest.TestCase):

    def _mock_create_call(self, response : str):
        mock_completion = Mock()
        mock_completion.choices = [Mock()]
        mock_completion.choices[0].message = Mock()
        mock_completion.choices[0].message.content = response

        return mock_completion

    @patch("src.translate_command.client.chat.completions.create")
    @patch("builtins.input", return_value="y")
    @patch("builtins.print")
    @patch("src.translate_command.explain_command", side_effect=explain_command)
    @patch("src.translate_command.execute_command")
    def test_command_explanation(
        self,
        mock_execute_command,
        mock_explain_command,
        mock_print,
        mock_input,
        mock_create,
    ):

        mock_create.side_effect = [
            self._mock_create_call(response="```bash\nls -la\n```"),
            self._mock_create_call(response="Explanation of sudo ls -la"),
        ]

        query = "List all files"
        model = "test-model"
        explain = True
        trust = False
        sudo = False
        timeout = 30

        translated_command = translate_command(
            query, model=model, explain=explain, trust=trust, sudo=sudo, timeout=timeout
        )

        # Check if the API call was made with the correct parameters
        # Define expected calls
        expected_translation_call = call(
            model=model,
            messages=[
                {"role": "system", "content": TRANSLATION_SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
        )

        expected_explanation_call = call(
            model=model,
            messages=[
                {"role": "system", "content": EXPLANATION_SYSTEM_PROMPT},
                {"role": "user", "content": "ls -la"},
            ],
        )

        mock_create.assert_has_calls([expected_translation_call, expected_explanation_call], any_order=False)

        # Check if the print statements were called with the correct output
        mock_print.assert_any_call("Translated command: ", "ls -la")
        mock_print.assert_any_call("Explanation: \nExplanation of sudo ls -la")

        # Check if the translated command was processed correctly
        self.assertEqual(translated_command, "ls -la")

    @patch("src.translate_command.client.chat.completions.create")
    @patch("builtins.input", return_value="y")
    @patch("builtins.print")
    @patch("src.translate_command.explain_command")
    @patch("src.translate_command.execute_command")
    def test_command_exec_if_trust(
        self,
        mock_execute_command,
        mock_explain_command,
        mock_print,
        mock_input,
        mock_create,
    ):

        query = "List all files"
        model = "test-model"
        explain = False
        trust = True
        sudo = False
        timeout = 30

        mock_create.return_value = self._mock_create_call(
            response="```bash\nls -la\n```"
        )

        translated_command = translate_command(
            query, model=model, explain=explain, trust=trust, sudo=sudo, timeout=timeout
        )

        # Check if the execute_command was called with the correct parameters
        mock_execute_command.assert_called_once_with(
            translated_command="ls -la", timeout=timeout
        )

    @patch("src.translate_command.client.chat.completions.create")
    @patch("builtins.input", return_value="y")
    @patch("builtins.print")
    @patch("src.translate_command.explain_command")
    @patch("src.translate_command.execute_command")
    def test_command_exec_if_input_yes(
        self,
        mock_execute_command,
        mock_explain_command,
        mock_print,
        mock_input,
        mock_create,
    ):

        query = "List all files"
        model = "test-model"
        explain = False
        trust = False
        sudo = False
        timeout = 30

        mock_create.return_value = self._mock_create_call(
            response="```bash\nls -la\n```"
        )

        translated_command = translate_command(
            query, model=model, explain=explain, trust=trust, sudo=sudo, timeout=timeout
        )

        # Check if the execute_command was called with the correct parameters
        mock_execute_command.assert_called_once_with(
            translated_command="ls -la", timeout=timeout
        )

    @patch("src.translate_command.client.chat.completions.create")
    @patch("builtins.input", return_value="n")
    @patch("builtins.print")
    @patch("src.translate_command.explain_command")
    @patch("src.translate_command.execute_command")
    def test_no_command_exec(
        self,
        mock_execute_command,
        mock_explain_command,
        mock_print,
        mock_input,
        mock_create,
    ):

        query = "List all files"
        model = "test-model"
        explain = False
        trust = False
        sudo = False
        timeout = 30

        mock_create.return_value = self._mock_create_call(
            response="```bash\nls -la\n```"
        )

        translated_command = translate_command(
            query, model=model, explain=explain, trust=trust, sudo=sudo, timeout=timeout
        )

        # Check if the execute_command was called with the correct parameters
        mock_execute_command.assert_not_called()
