# we will have our original input GPX
#Say points A & B  each have a latitude and longitude values
#we need a margin of error, let's say it's 0.000029. can modify that if needed
#the margin of error means that when we're comparing lonA in fileA to lonB in fileB,
#lonA can be > or < lonB by (.000029 or less) and we'd believe that lonA still on same route as lonB,
#assuming latitude similarly corresponds


#This is a rough draft to start with and may be missing some info on:
#how we're getting our corresponding route per track-segment from the route-service
#how we're storing that corresponing route per track-segment from the route-service
#how to get pointB, latB, and lonB

#this might have:
#syntactic errors
#wrong "margin of error" number... we might have to look that number up. I guessed. I could be totally off


import re
from gpx_read import get_coordinates
from create_route import get_path

marginOfError = 0.000029
curreNTH = 0
#evens are latitude
#odds are longitude
#maybe there's a better way or  labeling system to distinguish which elements in list are latitude or longitude

def parseList():
    ls = get_coordinates("GPXinput.gpx")
    ret = get_path([ls[0], ls[len(ls - 1)]])
# print(ret)
    ret_ls = re.findall('[<](.*?)[>]', ret)

    new_ls = []
    #can we make the new list still have the latitudes and longitudes labeled
    #so that we can easily distinguish and extract the part that is latitude and part that is longitude
    for i in range(len(ret_ls)):
        if ret_ls[i][0:5] == "rtept":
            new_ls.append(ret_ls[i])
    print(new_ls)
    return new_ls
    #what data type are the elements of the list? Are they still tuples? strings?

#need a function for coordinate-output from RouteService,
# turn that output into a list of the same structure
# as the list of latitude and longitude of the input file
# or store results of coordinate-output in data structure.

#def get_route_service_coordinates():
    #enter trackpoint A and Trackpoint Z into a route service
    #
    #import the type of file that the Route Service creates?
    #fileB =
    #return fileB



#Presumably we entered starting trackpoint (Point J) and an ending trackpoint (Point K) into a route service
#the route service gave us a route
# we converted that route back to latitude and longitude in file B
#we're comparing latitude and longitude in trackpoint from GPX file at pointJ to file B pointJ



def get_point_B():
    #route_service_generated_list
    #file_b_point_list = get_coordinates("FileB") #there's really no such FileB, it's just s placeholder until we have a FileB
    #name that list "route_service_generated_list"
    #navigate to the curreNTH point in that structure
    #return Point B as a string with "lat:" latB, "lon:" lonB
    return


def getLatA(curreNTH):
    latA = parseList()[curreNTH]
    return latA



def getLonA(curreNTH):
    lonA = parseList()[curreNTH+1]
    return lonA
    #increment curreNTH in new_ls

def getLatB():
    #Parse the string returned by get_point_B
    #to cut away the part that says "lat"
# syntax for cut away unwanted part may be something like: ret_ls = re.findall('[<](.*?)[>]', ret)
    #store that remaining part after you cut away "lat"
    return 1

def getLonB():
    #same logic as getLatB, just for the longitude
    return 2
#A coordinates are from the GPX file,
#B coordinates are from the Route Service result
maxLatB = (getLatA(curreNTH) + marginOfError)
minLatB = (getLatA(curreNTH) - marginOfError)
maxLonB = getLonA(curreNTH) + marginOfError
minLonB = getLonA(curreNTH) - marginOfError
latA = (getLatA(curreNTH))
lonA = (getLonA(curreNTH))

def compareLats(curreNTH):
    if ((latA <= maxLatB) & (latA >= minLatB)): return True
    else: return False

def compareLons(curreNTH):
    if((lonA <= maxLonB )& (lonA >= minLonB)): return True
    else: return False

def comparingResult(curreNTH):
    if(compareLats(curreNTH) & compareLons(curreNTH)): return True
    else: return False

def determineWhichIsOff(curreNTH):
    if (comparingResult(curreNTH)) == False:
        if (compareLats(curreNTH)) == False:
            return " *LATITUDE is OFF!* "
        if (compareLons (curreNTH) == False):
            return " *LONGITUDE is OFF!* "
    else: return "*The Route Service coordinates match the input coordinates*"

if __name__ == "main":
    while(comparingResult(curreNTH) == True):
        curreNTH +1 # next latitude coordinate in list from GPX file