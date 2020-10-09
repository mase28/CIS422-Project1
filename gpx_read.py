import gpxpy
import gpxpy.gpx

#Opens gpx file and stores coordinates in a list of tuples
def get_coordinates(file: str) -> list:
	gpx_file = open(file, 'r')
	gpx = gpxpy.parse(gpx_file)
	result = []

	for track in gpx.tracks:
		for segment in track.segments:
			for point in segment.points:
				result.append([point.longitude, point.latitude])

	gpx_file.close()

	return result
