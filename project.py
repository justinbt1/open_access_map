import pathlib
import subprocess
import click
from src.download_datasets import download_all_data


@click.group()
def cli():
    pass


@cli.command()
def setup():
    pathlib.Path('data').mkdir(exist_ok=True)
    pathlib.Path('outputs').mkdir(exist_ok=True)

    subprocess.run('conda env create --file=environment.yaml')
    print('Run conda activate oa_maps to activate environment')


@cli.command()
def download_data():
    download_all_data()


if __name__ == '__main__':
    cli()
