import requests
import json

def get_path(coords) -> str:
	body = {"coordinates":coords}

	headers = {
    	'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    	'Authorization': '5b3ce3597851110001cf62483d18334e69f5463f93b256caef070b0b',
    	'Content-Type': 'application/json; charset=utf-8'
	}
	
	call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/geojson', json=body, headers=headers)
	
	return call.text

def get_coordinates_json(json_input):
	js = json.loads(json_input)
	coords = {}
	for keys in js:
		if keys == "features":
			temp = js["features"][0]
			for key in temp:
				if key == "geometry":
					coords = temp[key]["coordinates"]
	return coords
	