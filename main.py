import re
from gpx_read import get_coordinates
from create_route import get_path

if __name__ == "__main__":
	ls = get_coordinates("gpx_file.gpx")

	ret = get_path([ls[0], ls[len(ls)-1]])

	# print(ret)
	ret_ls = re.findall('[<](.*?)[>]', ret)

	new_ls = []
	for i in range(len(ret_ls)):
		if ret_ls[i][0:5] == "rtept":
			new_ls.append(ret_ls[i])
	print(new_ls)