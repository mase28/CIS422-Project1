# we will have our original input GPX
#Say points A & B  each have a latitude and longitude values
#we need a margin of error, let's say it's 0.000029. can modify that if needed
#the margin of error means that when we're comparing lonA in fileA to lonB in fileB,
#lonA can be > or < lonB by (.000029 or less) and we'd believe that lonA still on same route as lonB,
#assuming latitude similarly corresponds

marginOfError = 0.0005   #This can still change. We need to find accurate margin of Error

def compareLats(latA: float, latB: float) -> bool:
    maxLatB = latA + marginOfError
    minLatB = latA - marginOfError
    if ((latB <= maxLatB) and (latB >= minLatB)): 
        return True
    else: 
        return False

def compareLons(lonA: float, lonB: float) -> bool:
    maxLonB = lonA + marginOfError
    minLonB = lonA - marginOfError
    if((lonB <= maxLonB ) and (lonB >= minLonB)): 
        return True
    else: 
        return False

def comparingResult(coordA, coordB):
    if(compareLats(coordA[1], coordB[1]) and compareLons(coordA[0], coordB[0])): 
        return True
    else: 
        return False
