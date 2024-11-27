# Arcane incantation to print all the other targets, from https://stackoverflow.com/a/26339924
help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

.PHONY: download_data
download_data:
	python src/data_scrapers/esri_api.py "defra_crow_oa" "https://services.arcgis.com/JJzESW51TqeY9uat/arcgis/rest/services/CRoW_Act_2000_Access_Layer/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
	python src/data_scrapers/esri_api.py "national_trust_oa" "https://services-eu1.arcgis.com/NPIbx47lsIiu2pqz/arcgis/rest/services/National_Trust_Open_Data_Land_Always_Open/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
	python src/data_scrapers/esri_api.py "local_authority_boundaries" "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAU1_Dec_2015_GCB_in_England_and_Wales_2022/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
	python src/data_scrapers/ons_postcode_data.py "https://www.arcgis.com/sharing/rest/content/items/a2f8c9c5778a452bbf640d98c166657c/data"
