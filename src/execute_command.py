import subprocess

def execute_command(translated_command: str, timeout: int):
    # Run command with timeout
    try:
        result = subprocess.run(
            translated_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        print("Command output:")
        print(result.stdout)
        if result.stderr:
            print("Command error output:")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout} seconds")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        print(f"stderr: {e.stderr}")
    except Exception as e:
        print(f"An error occurred while running the command: {e}")
