import geopandas as gp

def calculate_postcode_oa():
    print('Loading crow')
    crow_gdf = gp.read_file('data/defra_crow_oa.geojson')
    print('loading postcode')
    postcode_gdf = gp.read_file('data/ons_postcode_data.geojson')
    postcode_gdf['geometry'] = postcode_gdf['geometry'].buffer(1000)

    intersection_gdf = gp.overlay(
        postcode_gdf,
        crow_gdf,
        how="intersection"
    )

    print(intersection_gdf)

if __name__ == '__main__':
    calculate_postcode_oa()
