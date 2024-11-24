import os
import requests


def retrieve_geojson(dataset_url, filename):
    content = requests.get(dataset_url).text

    output_filepath = os.path.join('data', filename)
    with open(output_filepath, 'wt') as file:
        file.write(content)


def retrieve_national_trust_data():
    """Downloads National Trust always open land data

    This includes land open due to CRoW or permission from the NT (2023).

    """
    link = 'https://services-eu1.arcgis.com/NPIbx47lsIiu2pqz/arcgis/rest/services/' \
            'National_Trust_Open_Data_Land_Always_Open/FeatureServer/0/' \
            'query?outFields=*&where=1%3D1&f=geojson'
    
    retrieve_geojson(link, 'national_trust_oa.geojson')
