from gpx_read import get_coordinates_gpx
from create_route import get_path, get_coordinates_json
from compare_coord_files import comparingResult

if __name__ == "__main__":
	ls = get_coordinates_gpx("gpx_file.gpx")

	ret = get_path([ls[0], ls[len(ls)-1]])

	coords = get_coordinates_json(ret)

	for i in range(len(coords)):
		if comparingResult(ls[i], coords[i]):
			print(f"Coordinate in gpx: {ls[i]} Coordinate in json: {coords[i]}. These line up.")
		else:
			print(f"Coordinate in gpx: {ls[i]} Coordinate in json: {coords[i]}. These do not line up.")

	