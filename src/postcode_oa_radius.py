import geopandas as gp

def calculate_postcode_oa():
    print('Loading crow')
    crow_gdf = gp.read_file('data/defra_crow_oa.geojson')
    crow_gdf.crs = 'EPSG:4326'
    crow_gdf = crow_gdf.to_crs(epsg=6933)

    print('loading postcode')
    postcode_gdf = gp.read_file('data/ons_postcode_data.geojson')
    postcode_gdf = postcode_gdf.to_crs(epsg=6933)

    crow_gdf['crow_geometry'] = crow_gdf['geometry']

    intersection_gdf = postcode_gdf[['pcd', 'geometry']].sjoin(
        crow_gdf[['OBJECTID', 'geometry', 'crow_geometry']],
        how='left',
        predicate='intersects'
    )

    intersection_gdf = intersection_gdf['geometry'].intersection(
        intersection_gdf['crow_geometry']
    )


if __name__ == '__main__':
    calculate_postcode_oa()
