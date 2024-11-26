import os
import yaml
import zipfile
import requests
import pandas as pd
import geopandas as gp

with open('src/data_urls.yaml', 'rt') as config_file:
    config = yaml.safe_load(config_file)


def retrieve_arcgis_api_data():
    """Download datasets from ArcGIS API and write to GeoJSON file.
    """
    for dataset in config:
        url = config[dataset]['url']
        filename = config[dataset]['filename']
        content = requests.get(url).text

        output_filepath = os.path.join('data', filename)
        with open(output_filepath, 'wt') as file:
            file.write(content)


def retrieve_right_of_way_data():
    # ToDo: Add public right of way data from all local authorities.
    pass


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


def retrieve_postcode_data():
    """Downloads ONS postcode data from ONS Open Geography Portal.
    """
    url = 'https://www.arcgis.com/sharing/rest/content/items/a2f8c9c5778a452bbf6' \
    '40d98c166657c/data'

    response = requests.get(url)
    filepath = os.path.join('data', 'ons_postcode_data.zip')

    with open(filepath, mode="wb") as file:
        file.write(response.content)

    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        extraction_path = os.path.join('data', 'ons_postcode_data')
        zip_ref.extractall(extraction_path)

    _prepare_postcode_data()
    os.remove(filepath)


if __name__ == '__main__':
    retrieve_arcgis_api_data()
    retrieve_postcode_data()
