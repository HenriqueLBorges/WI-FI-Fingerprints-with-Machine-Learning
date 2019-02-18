import json
with open('config.json') as json_data_file:
        data = json.load(json_data_file)
#Gets compass bearing
def getCompassBearing():
    destination = raw_input('destination = ')
    return destination

#Returns the offset in between two cardinal points
def getDifference (cardinal1, cardinal2):
    difference = raw_input('difference = ')
    return int(difference)

#Receives an angle and returns the cardinal point
def compassBearing(angle):
    for key, value in data['compass_rose'].iteritems():
        if angle >= value['min'] and angle <= value['max']:
            return key