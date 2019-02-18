import json
import machPy
import utils
import sys

json_data=open('/Users/henriqueborges/Documents/Senac/TCC/imports/A118.json').read()
data = json.loads(json_data)
fingerprints = []
forbidenMacAddresses = [u'B8:27:EB:A6:7B:C5', u'B8:27:EB:24:1B:E1']

#navigates through every fingerprint inside document fingerprints' array
for fingerprint in data['fingerprints']:
    #navigates through every access inside the fingerprint array
    items = []
    for accessPoint in fingerprint:
        if accessPoint['macAddress'] not in forbidenMacAddresses and accessPoint['macAddress'] not in items:
            items.append(accessPoint)
    fingerprints.append(items)

macAddresses = utils.loadObj('./macAddresses')

results = []
for fingerprint in fingerprints:
    #print(fingerprint)
    #machPy.getCurrentPositionProbabilist(fingerprint)
    #print(machPy.getCurrentPosition1(fingerprint))
    result = machPy.getCurrentPosition1(fingerprint)
    #print('result = ' + result)
    results.append(result)
    #break
print('final = ' + str(utils.mostCommon(results))) 

#result = machPy.getCurrentPosition2(fingerprints)
#print('result = ' + result)