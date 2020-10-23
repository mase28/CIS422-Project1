from gpx_read import get_coordinates_gpx
import requests
import json
from create_route import get_path

def get_directions(path: str) -> list:
	#Function that gets turn by turn directions from the path returned by get_path
	text = json.loads(path)
	directions = []
	for x in text["matchings"]:
		for y in x["legs"]:
			for z in y["steps"]:
				directions.append(z["maneuver"]["instruction"] + " in " + str(round(z["distance"] / 1000, 2)) + " KM")
	return directions

def remove_directions(directions: list) -> list:
	#Function that removes each "You have arrived" directions except the last one
	#and combines the distances from all the "Head (direction)..." instructions
	new_dir = []
	prev = ""
	i = 0
	while i < (len(directions)):
		direction = directions[i].split(" ")
		if direction[0] == "You"  and i != len(directions) - 1:
			i += 1
			continue
		elif direction[0] == "Head":
			distance = float(direction[len(direction) - 2])
			for j in range(i+1, len(directions)):
				if j >= len(directions) - 1:
					i = j+1
					break
				distance += float(direction[len(direction) - 2])
				direction = directions[j].split(" ")
				if direction[0] != "Head" and direction[0] != "You" and len(direction) > 5:
					direction[len(direction) - 2] = str(round(distance, 2))
					new_dir.append(" ".join(direction))
					i = j + 1
					break
		else:
			if i <= len(directions) - 1 and len(direction) > 5:
				curr_street = " ".join(direction[3:(len(direction)-3)])
				distance = float(direction[len(direction)-2])
				while True:
					i += 1 
					next_dir = directions[i].split(" ")
					next_street = " ".join(next_dir[3:(len(next_dir)-3)])
					if (curr_street == next_street):
						distance += float(next_dir[len(next_dir)-2])
					else:
						direction[len(direction)-2] = str(round(distance))
						new_dir.append(" ".join(direction))
						break
			elif len(direction) > 5:
				new_dir.append(directions[i])
			i += 1
	return new_dir

def main(file: str, api: str):
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
	for i in new_dir:
		print(i)

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

	f = open("./app/templates/output.html", "w")
	f.write(output_first)
	f.close()
