
#This is the logic to determine attributes on UTM coordinate system

#convert to UTM,
# datum preferred is WGS84, est'd in 1984
#ellipsoid is cylindrical if possible
#zone 10T for western Oregon

# point LatA, LongA get from the file
northing = 111,000.0 *abs(LatA) #in meters
longitudeDecimal = longA + 123.0
#if any point is greater than 126 W longitude or less than 120 W longitude,
#then we can't make accurate measurements with UTM because a zone only spans 6 degrees
#upon transcending zones, you'd lose accuracy
# we're lucky we're at 123 west longitude because that's exactly the middle of zone 10
#and zones are based on the exact middle of the 6 degrees longitude being 500,000
# but we never go as far as 3 whole degrees in either direction.
#Confirm? Please?!
def determineEasting():
    if (longitudeDecimal >0):
        addTo500000 =(longitudeDecimal * 111000.0)
        easting =  500000.0 + addTo500000
        return easting
    if(longitudeDecimal <0):
        subtractFrom500000 = (longitudeDecimal * 111000.0)
        easting = 500000.0 - subtractFrom500000
        return easting
    if (longitudeDecimal == 0.0):
        easting = 500000
        return easting
#easting is in approximate meters;
# approximate
# because 111,000 meters (or 111 km) is the distance of 1 degree longitude at the equator.
#Not sure about difference in factor for 44 North latitude















