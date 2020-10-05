import requests
import json

def get_address(lat: float, lon: float) -> str:
	url = "https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP/default.aspx"
	ret = ""

	param = {
		"apiKey": "f2eca2195518451a925e621b57e7981a",
		"version": 4.10,
		"lat": lat,
		"lon": lon
	}

	resp = requests.get(url, params=param)
	content = resp.text.split(sep=',')

	for i in range(5, 9, 1):
		ret += content[i]
		if (i != 8):
			ret += ", "

	return ret
