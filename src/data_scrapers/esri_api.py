import os
import click
import requests


@click.command()
@click.argument('name')
@click.argument('url')
def retrieve_arcgis_api_data(name, url):
    """Download datasets from ArcGIS API and write to GeoJSON file.
    """
    content = requests.get(url).text

    output_filepath = os.path.join('data', f'{name}.geojson')
    with open(output_filepath, 'wt') as file:
        file.write(content)


if __name__ == '__main__':
    retrieve_arcgis_api_data()
