import click
from src.translate_command import translate_command

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
def main(query, model=None, explain=False, trust=False, sudo=False, timeout=30):

    command = translate_command(
        query=query,
        model=model,
        explain=explain,
        trust=trust,
        sudo=sudo,
        timeout=timeout,
    )
    return command
