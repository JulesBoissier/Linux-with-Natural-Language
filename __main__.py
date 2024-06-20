from dotenv import load_dotenv
import os
import subprocess
import click
from openai import OpenAI

SYSTEM_PROMPT = """
    Please provide a Linux command that accomplishes the following task: "Write a Linux command to achieve the following Natural Language command. 
    You must reply with only the linux command. Nothing else!" Ensure your response consists solely of the Linux command required to fulfill the task.
    """

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


def explain_command(command: str, model: str):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Give a clear step-by-step explanation of what this command does, labelling logical steps as 1, 2, etc",
            },
            {"role": "user", "content": command},
        ],
    )

    explanation = response.choices[0].message.content.strip()

    return explanation


@click.command()
@click.argument("query", type=str)
@click.option(
    "--model", default="gpt-3.5-turbo", help="Specify the model to use for translation."
)
@click.option(
    "--explain/--no-explain", default=False, help="Enable explanation of translation."
)
@click.option(
    "--trust/--no-trust", default=False, help="Enable trusted mode for translation."
)
@click.option(
    "--sudo/--no-sudo", default=False, help="Enable sudo mode for translation."
)
@click.option(
    "--timeout", default=30, help="Specify a timeout for the command execution."
)
def translate_command(
    query, model=None, explain=False, trust=False, sudo=False, timeout=30
):

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    # Extract the content from the response
    translated_command = response.choices[0].message.content.strip()

    # Clean up the command: remove unnecessary formatting
    translated_command = (
        translated_command.replace("```bash", "").replace("```", "").strip()
    )

    if sudo:
        translated_command = "sudo " + translated_command

    print("Translated command: ", translated_command)

    if explain:
        explanation = explain_command(translated_command, model=model)
        print("Explanation: ", explanation)

    if trust or input("Run command? (Y/N): ").strip().lower() == "y":
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


if __name__ == "__main__":
    translate_command()
