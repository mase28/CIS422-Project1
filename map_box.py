from gpx_read import get_coordinates_gpx
import requests
from shapely.geometry import LineString, MultiLineString, Polygon
import json
import polyline
import matplotlib.pyplot as plt
import utm
import geopy.distance

def get_path(coords: list):
	coord = ""
	for i in range(len(coords)):
		coord += str(coords[i][1]) + "," + str(coords[i][0])
		if i != len(coords) - 1:
			coord += ";"
	coord += "?"
	url = "https://api.mapbox.com/directions/v5/mapbox/driving/" + coord + "geometries=geojson&steps=true&access_token=pk.eyJ1IjoibWFzZTI4IiwiYSI6ImNrZ2U1NjdraDA4OGUycXBpZHlsOWxyZnYifQ.sYRLp9MeUZeUNbTMzCM5AA"
	call = requests.get(url)
	return call.text

def get_coords(js):
	text = json.loads(js)
	line = text["routes"][0]["geometry"]["coordinates"]
	return line

def track_to_utm(track):
    """convert [[lat, lon], [lat, lon], ... ]
    to [(easting, northing, cumdist), (easting, northing, cumdist), ...]
    with a zone --- we choose one UTM zone and make sure all eastings and 
    northings are in that zone, so that distance between points can be 
    computed directly from UTM values.
    """
    if len(track) == 0:
        return track, 10 

    # Determine UTM zone from center of path
    mid_lat, mid_lon = track_centerpoint(track)
    _, _, utm_zone, _ = utm.from_latlon(mid_lat, mid_lon)

    utm_path = [ ]

    for pt in track:
        lat, lon = pt
        easting, northing, _, _ = utm.from_latlon(lat, lon, force_zone_number=utm_zone)
        # Compact rep in text: Round meters for easting and northing,
        # two digits for kilometer distance
        utm_pt = (round(easting), round(northing))
        utm_path.append(utm_pt)

    return utm_path, utm_zone

def track_centerpoint(track):
    """Given track == [[lat, lon], [lat, lon], ... ], 
    return (midlat, midlon) as central values, i.e., 
    midlat is halfway between min and max of lat, and midlon is 
    halfway between min and max of lon.
    """
    if len(track) == 0:
        return (0, 0)
    elif len(track) == 1:
        return track[0]
    min_lat, min_lon = track[0]
    max_lat, max_lon = track[0]
    for pt in track:
        lat, lon = pt
        if lat < min_lat:
            min_lat = lat
        if lat > max_lat:
            max_lat = lat
        if lon < min_lon:
            min_lon = lon
        if lon > max_lon:
            max_lon = lon
    return (min_lat + max_lat)/2.0, (min_lon + max_lon)/2.0

def switch_latlon(ls):
	for i in range(len(ls)):
		temp = ls[i][0]
		ls[i][0] = ls[i][1]
		ls[i][1] = temp

def plot_shapely(ob, color):
	if isinstance(ob, LineString):
		x, y = ob.xy
		plt.plot(x, y, color)
	elif isinstance(ob, MultiLineString):
		for line in multiline:
			x, y = line.xy
			plt.plot(x, y, color)
	elif isinstance(ob, Polygon):
		x, y = ob.exterior.xy
		plt.plot(x, y, color)

def get_directions(path):
	text = json.loads(path)
	directions = []
	for steps in text["routes"][0]["legs"][0]["steps"]:
		for instr in steps["maneuver"]:
			if instr == "instruction":
				directions.append(steps["maneuver"][instr])
	return directions

if __name__ == "__main__":
	ls = get_coordinates_gpx("gpx_file.gpx")
	
	
	gpx_utm_path, gpx_zone = track_to_utm(ls[:10])
	gpx_polyline = LineString(gpx_utm_path)
	
	start = 0
	end = len(ls[:10]) - 1
	end_path = end // 2
	directions = []
	flag = True
	while (start < end):
		path = get_path([ls[start], ls[end_path]])
		map_coords = get_coords(path)
		switch_latlon(map_coords)
		map_utm_path, _ = track_to_utm(map_coords)
		map_polyline = LineString(map_utm_path)

		buff = LineString(map_utm_path).buffer(.5)
		diff = gpx_polyline.difference(buff)

		if (diff.is_empty):
			directions.append(get_directions(path))
			start = end_path
			end_path = end
		else:
			diff_ls = list(diff.coords)
			# print(diff_ls)
			mid = diff_ls[len(diff_ls) // 2]
			# print(f"mid: ({int(mid[0])}, {int(mid[1])})")
			# print(f"utm_gpx: {gpx_utm_path}")
			for i in range(start, end):
				print(f"gpx: ({gpx_utm_path[i][0]}, {gpx_utm_path[i][1]})  mid: ({mid[0]}, {mid[1]}")
				if int(gpx_utm_path[i][0]) == int(mid[0]) and int(gpx_utm_path[i][1]) == int(mid[1]):
					end_path = i
					break

		print(f"Start: {start}, end_path: {end_path}")
		print(directions)
		print()
	
	# path = get_path([ls[0], ls[10]])
	# map_coords = get_coords(path)
	# switch_latlon(map_coords)
	# map_utm_path, map_zone = track_to_utm(map_coords)
	# map_polyline = LineString(map_utm_path)

	# buff = LineString(map_utm_path).buffer(.5)
	# diff = gpx_polyline.difference(buff)
	# inter = gpx_polyline.intersection(buff)

	# plot_shapely(gpx_polyline, "r")
	# plot_shapely(map_polyline, "g")
	# plot_shapely(buff, "y")
	# plot_shapely(diff, "b")

	# print(list(gpx_polyline.coords))
	# print()
	# print(list(map_polyline.coords))
	# print()
	# print(list(diff.coords))
	# print()
	# print(list(inter.coords))

	# plt.show()


