from gpx_read import get_coordinates_gpx
import json
from create_route import get_path

def get_directions(path: str) -> list:
	#Function that gets turn by turn directions from the path returned by get_path
	text = json.loads(path)
	directions = []
	for x in text["matchings"]:
		for y in x["legs"]:
			for z in y["steps"]:
				directions.append(z["maneuver"]["instruction"] + " in " + str(z["distance"]) + " KM")
	return directions

def remove_directions(directions: list) -> list:
	#Function that removes unhelpful directions
	new_dir = []
	prev = []
	for i in range(len(directions)):
		direction = directions[i].split(" ")
		direction_str = " ".join(direction[:len(direction) - 3])
		if direction[0] == "You"  and i != len(directions) - 1:
			continue
		elif direction_str in prev or direction[0] == "Head" or len(direction) == 5:
			continue
		else:
			prev.append(direction_str)
			new_dir.append(directions[i])
	return new_dir

def main(file: str, api: str):
	print("In Main")
	ls = get_coordinates_gpx(file)

	start = 0
	end = len(ls) - 1
	end_path = 100
	directions = []
	while(start < end):
		path = get_path(ls[start:end_path], api)
		direction = get_directions(path)
		directions += direction
		start += 100
		end_path += 100

	new_dir = remove_directions(directions)

	output_first = (
    "<html lang=\"en\">\n"
    "<head>\n"
    "<meta charset=\"utf-8\">\n"
    "</head>\n"
    "<body>\n"
    "\t<ul>\n")

	output_sec = (
    "\t</ul>\n"
    "</body>\n"
    "</html>")


	for i in new_dir:
		output_first += "\t\t<li>" + i + "</li>\n"

	output_first += output_sec

	f = open("./templates/output.html", "w")
	f.write(output_first)
	f.close()
