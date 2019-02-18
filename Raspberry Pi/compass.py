import py_qmc5883l
import time
import json
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

sensor = py_qmc5883l.QMC5883L()
declination = 0

#Loads declination config
try:
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
        delta = datetime.now() - datetime.strptime(data['updated'], '%d/%m/%Y')
        
        params = {
            'lat1': data['lat'],
            'lon1': data['lon'],
            'resultFormat': 'xml' 
        }

        #If the last update was more than 1 year ago. Update again
        if delta.days > 365:
            print 'Updating...'

            #Calls the API to receive the current declination for the coordinates
            response = requests.get('https://www.ngdc.noaa.gov/geomag-web/calculators/calculateDeclination', params=params)
            try:
                #Navigates through XML response and casts it to a float
                result = float(ET.fromstring(response.text).findall('result')[0].findall('declination')[0].text)
                
                #Sets declination
                declination = result

                #Updates json file
                data['declination'] = result
                data['updated'] = datetime.now().strftime('%d/%m/%Y')
                
                #Saves the config json file again.
                with open('config.json', 'w') as outfile:
                    json.dump(data, outfile)
            except Exception as e:
                if data ['debug']:
                    print(e)
        else: declination = data['declination']

except IOError as e:
    declination = 0

#If declination is not zero, calibrates sensor declination
if declination != 0:
    sensor.declination = declination
    print 'declination = ' + str(sensor.declination)

#Receives an angle and returns the cardinal point
def compassBearing(angle):
    for key, value in data['compass_rose'].iteritems():
        if angle >= value['min'] and angle <= value['max']:
            return key

#Gets compass bearing
def getCompassBearing():
    return compassBearing(sensor.get_bearing())

#Gets sensor bearing
def getSensorBearing():
    return sensor.get_bearing()
    
#Returns the offset in between two cardinal points
def getDifference (cardinal1, cardinal2):
    cardinal1 = data['compass_rose'][cardinal1]
    cardinal2 = data['compass_rose'][cardinal2]

    if cardinal2['max'] > cardinal1['max']:
        return 1
    else: return -1

