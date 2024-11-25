import os
import requests


def retrieve_geojson(dataset_url, filename):
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
    pass


def retrieve_local_authority_polygons():
    link = 'https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/' \
    'LAU1_Dec_2015_GCB_in_England_and_Wales_2022/FeatureServer/0/query?outFields' \
    '=*&where=1%3D1&f=geojson'
    retrieve_geojson(link, 'local_authority_boundaries.geojson')


def retrieve_postcode_polygons():
    'https://www.arcgis.com/sharing/rest/content/items/a2f8c9c5778a452bbf640d98c166657c/data'

if __name__ == '__main__':
    retrieve_defra_crow_data()
    retrieve_national_trust_data()
