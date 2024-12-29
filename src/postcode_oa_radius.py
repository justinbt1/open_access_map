import geopandas as gp

def calculate_postcode_oa():
    print('Loading crow')
    crow_gdf = gp.read_file('data/defra_crow_oa.geojson')
    crow_gdf.crs = 'EPSG:4326'
    crow_gdf = crow_gdf.to_crs(epsg=6933)

    print('loading postcode')
    postcode_gdf = gp.read_file('data/ons_postcode_data.geojson')
    postcode_gdf = postcode_gdf.to_crs(epsg=6933)

    mile_radius = [1, 2.5, 5, 7.5]
    for meter_radius in [mile * 1609.344 for mile in mile_radius]:
        postcode_gdf = postcode_gdf['geometry'].buffer(meter_radius)

        print('Calculating intersections')
        intersection_gdf = gp.sjoin(
            postcode_gdf,
            crow_gdf,
            how='left',
            predicate='intersects'
        )

        print(intersection_gdf.area.to_list())


if __name__ == '__main__':
    calculate_postcode_oa()
