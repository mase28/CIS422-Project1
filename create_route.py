import requests
import json

def get_path(coords: list, api: str) -> str:
	#Function that uses the mapbox matchings api to plan the route
	coord = ""
	radiuses = "5;" * (len(coords) - 1) + "5"
	for i in range(len(coords)):
		coord += str(coords[i][0]) + "," + str(coords[i][1])
		if i != len(coords) - 1:
			coord += ";"
	url = f"https://api.mapbox.com/matching/v5/mapbox/cycling?access_token={api}"
	call = requests.post(url, data = {"coordinates": coord, "steps": "true", "tidy": "true", "radiuses": radiuses})
	return call.text

	