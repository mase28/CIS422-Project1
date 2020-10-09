import re
import json
from gpx_read import get_coordinates
from create_route import get_path

if __name__ == "__main__":
	ls = get_coordinates("gpx_file.gpx")

	ret = get_path([ls[0], ls[len(ls)-1]])

	js = json.loads(ret)
	for keys in js:
		if keys == "features":
			temp = js["features"][0]
			for key in temp:
				if key == "geometry":
					print(temp[key]["coordinates"])
	