import os
import zipfile
import requests
import pandas as pd
import geopandas as gp


def retrieve_geojson(dataset_url, filename):
    """Download and write to GeoJSON file to disk.

    Args:
        dataset_url(str): URL to get GeoJSON file from.
        filename(str): Filename to save GeoJSON to in data dir.

    """
    content = requests.get(dataset_url).text

    output_filepath = os.path.join('data', filename)
    with open(output_filepath, 'wt') as file:
        file.write(content)


def retrieve_defra_crow_data():
    """Downloads DEFRA CRoW open access land data.
    """
    link = 'https://services.arcgis.com/JJzESW51TqeY9uat/arcgis/rest/services/CRoW_' \
    'Act_2000_Access_Layer/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'

    retrieve_geojson(link, 'defra_crow_oa.geojson')


def retrieve_national_trust_data():
    """Downloads National Trust always open land data

    This includes land open due to CRoW or permission from the NT (2023).

    """
    link = 'https://services-eu1.arcgis.com/NPIbx47lsIiu2pqz/arcgis/rest/services/' \
    'National_Trust_Open_Data_Land_Always_Open/FeatureServer/0/query?outFields=*&' \
    'where=1%3D1&f=geojson'

    retrieve_geojson(link, 'national_trust_oa.geojson')


def retrieve_right_of_way_data():
    # ToDo: Add public right of way data from all local authorities.
    pass


def retrieve_local_authority_polygons():
    """Download local authority polygons from ONS Open Geography Portal.
    """
    link = 'https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/' \
    'LAU1_Dec_2015_GCB_in_England_and_Wales_2022/FeatureServer/0/query?outFields' \
    '=*&where=1%3D1&f=geojson'

    retrieve_geojson(link, 'local_authority_boundaries.geojson')


def _prepare_postcode_data():
    """Loads all postcode CSV and extracts and saves postcodes and coordinates.
    """
    df = pd.read_csv(
        'data/ons_postcode_data/Data/ONSPD_FEB_2023_UK.csv',
        low_memory=False
    )

    # Filter to England postcodes only.
    df = df.loc[df['ctry'] == 'E92000001']
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
    retrieve_defra_crow_data()
    retrieve_national_trust_data()
    retrieve_right_of_way_data()
    retrieve_local_authority_polygons()
    retrieve_postcode_data()
