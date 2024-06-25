import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

from src.execute_command import execute_command

SYSTEM_PROMPT = """
    Please provide a Linux command that accomplishes the following task: "Write a Linux command to achieve the following Natural Language command. 
    You must reply with only the linux command. Nothing else!" Ensure your response consists solely of the Linux command required to fulfill the task.
    """

# Load environment variables from .env file and the environment
load_dotenv(find_dotenv())

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found. Please set it in the environment or in a .env file."
    )


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

    print("Explanation: \n", explanation)


def strip_bash_artefacts(translated_command: str):
    return translated_command.replace("```bash", "").replace("```", "").strip()


def add_sudo_prefix(translated_command: str):
    return "sudo " + translated_command


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
    translated_command = strip_bash_artefacts(translated_command)

    if sudo:
        translated_command = add_sudo_prefix(translated_command)

    print("Translated command: ", translated_command)

    if explain:
        explain_command(translated_command, model=model)

    if trust or input("Run command? (Y/N): ").strip().lower() == "y":
        execute_command(translated_command=translated_command, timeout=timeout)

    return translated_command
