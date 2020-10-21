
#This is the logic to determine attributes on UTM coordinate system

#convert to UTM,
# datum preferred is WGS84, est'd in 1984
#ellipsoid is cylindrical if possible
#zone 10T for western Oregon
#LatA, LongA are assuming we've gotten the coordinates from another source, function call, etc.

#111000 factor is because 111 kilometers is the distance that 1 degree represents
# 111 kilometers times 1000 meters is the distance in meters that 1 degree represents
northing = (111,000.0 *LatA) #in meters
longitudeDecimal = longA + 123.0 #would give the offset from the meridian of the zone

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
