import os
import yaml
import zipfile
import requests
import pandas as pd
import geopandas as gp


def retrieve_arcgis_api_data(name, url):
    """Download datasets from ArcGIS API and write to GeoJSON file.

    Args:
        name(str): Filename of file to save dataset to. 
        url(str): ArcGIS API URL.

    """
    content = requests.get(url).text

    output_filepath = os.path.join('data', f'{name}.geojson')
    with open(output_filepath, 'wt') as file:
        file.write(content)


def _prepare_postcode_data():
    """Loads all postcode CSV and extracts and saves postcodes and coordinates.
    """
    df = pd.read_csv(
        'data/ons_postcode_data/Data/ONSPD_FEB_2023_UK.csv',
        low_memory=False
    )

    england_ctry_code = 'E92000001'
    df = df.loc[df['ctry'] == england_ctry_code]
    df = df[['pcd', 'pcd2', 'pcds', 'lat', 'long']]
    df = df.reindex()

    gdf = gp.GeoDataFrame(
        df,
        geometry=gp.points_from_xy(df.long, df.lat),
        crs='EPSG:4326'
    )

    filepath = os.path.join('data', 'ons_postcode_data.geojson')
    gdf.to_file(filepath, driver="GeoJSON")


def retrieve_postcode_data(url):
    """Downloads ONS postcode data from ONS Open Geography Portal.

    Args:
        url(str): ONS OGP postcode directory URL.

    """
    response = requests.get(url)
    filepath = os.path.join('data', 'ons_postcode_data.zip')

    with open(filepath, mode="wb") as file:
        file.write(response.content)

    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        extraction_path = os.path.join('data', 'ons_postcode_data')
        zip_ref.extractall(extraction_path)

    _prepare_postcode_data()
    os.remove(filepath)


def download_all_data():
    with open(os.path.join('src', 'api_config.yaml')) as file:
        config = yaml.safe_load(file)

    for url, name in zip(config['arcgis_api']['urls'], config['arcgis_api']['names']):
        print(f'Downloading data from {url}')
        retrieve_arcgis_api_data(name, url)

    print('Downloading ONS postcode data.')
    retrieve_postcode_data(config['ons_postcodes']['url'])


if __name__ == '__main__':
    download_all_data()
