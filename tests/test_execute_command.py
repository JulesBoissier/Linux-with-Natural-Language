import subprocess
from unittest import TestCase
from unittest.mock import patch, Mock
from src.translate_command import execute_command  # Adjust the import path as needed


class TestExecuteCommand(TestCase):

    @patch("subprocess.run")
    def test_execute_command_success(self, mock_run):
        # Set up the mock to simulate a successful command execution
        mock_result = Mock()
        mock_result.stdout = "Success output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        execute_command("ls -la", timeout=30)

        mock_run.assert_called_once_with(
            "ls -la", shell=True, capture_output=True, text=True, timeout=30
        )

    @patch("subprocess.run")
    def test_execute_command_timeout(self, mock_run):
        # Set up the mock to simulate a command timeout
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="ls -la", timeout=30)

        execute_command("ls -la", timeout=30)

        mock_run.assert_called_once_with(
            "ls -la", shell=True, capture_output=True, text=True, timeout=30
        )

    @patch("subprocess.run")
    def test_execute_command_failure(self, mock_run):
        # Set up the mock to simulate a command failure
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="ls -la", stderr="Error output"
        )

        execute_command("ls -la", timeout=30)

        mock_run.assert_called_once_with(
            "ls -la", shell=True, capture_output=True, text=True, timeout=30
        )

    @patch("subprocess.run")
    def test_execute_command_generic_exception(self, mock_run):
        # Set up the mock to simulate a generic exception
        mock_run.side_effect = Exception("Generic error")

        execute_command("ls -la", timeout=30)

        mock_run.assert_called_once_with(
            "ls -la", shell=True, capture_output=True, text=True, timeout=30
        )
