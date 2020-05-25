import logging
import click

from src.data.cleaner import clean as clean_data

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
def clean():
    clean_data()
    

if __name__ == '__main__':
    cli()
