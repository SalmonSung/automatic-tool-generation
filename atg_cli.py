import os
import click
import config
from core.utils import get_latest_file
from atg import AgentBuilder  # Assuming this is where AgentBuilder lives
from dotenv import load_dotenv

load_dotenv()

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])





@click.command(help="""\b
Generate tools for an LLM agent to analyze the provided data.

Example:
    python atg.py generate -p data.csv -b 3
""")
@click.option(
    "-p", "--path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    required=True,
    help="Path to your original data file."
)
@click.option(
    "-b", "--breadth",
    default=2,
    show_default=True,
    type=int,
    help="How many methods should the agent create?"
)
def generate(path, breadth):
    print("Generating tools for {} breadth={}".format(path, breadth))
    # click.echo(f" Input File: {path}")
    # click.echo(f" Breadth: {breadth}")

    import asyncio
    agent = AgentBuilder(breadth=breadth)
    results = asyncio.run(agent.run(path))
    print(f'\n\nGenerated Tools saved in {results}\n\n')


@click.command(help="""\b
Replay the most recent result or a specific one.
""")
@click.option(
    "-m", "--mode",
    default="path",
    type=click.Choice(["path", "content"], case_sensitive=False),
    show_default=True,
    help="What to replay: 'path' shows the latest file path, 'content' prints its contents."
)
def replay(mode):

    latest_file_path = get_latest_file(config.APP_PATH_RESULT)
    if mode == "path":
        print("\n\n\nLatest tool.py is saved at:")
        print(str(latest_file_path) + "\n\n\n")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="v0.3", prog_name="Automatic Tool Generation für LLM Agent")
def cli():
    """
    Automatic Tool Generation for LLM Agent

    A CLI to generate and replay tools based on input data files.
    """
    # Ensure required directories exist
    os.makedirs(config.APP_PATH_RESULT, exist_ok=True)
    os.makedirs(config.APP_PATH_DATASET, exist_ok=True)

cli.add_command(generate)
cli.add_command(replay)

if __name__ == "__main__":
    cli()

