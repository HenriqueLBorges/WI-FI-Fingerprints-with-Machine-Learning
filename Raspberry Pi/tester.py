import json

def getSamples(room, forbidenMacAddresses):
    fingerprints = []
    try:
        with open('/Users/henriqueborges/Documents/Senac/TCC/imports/testData/' + room + '.json') as json_data_file:
            data = json.load(json_data_file)
            cont = 0
            #navigates through every fingerprint inside fingerprints array
            for fingerprint in data:
                #navigates through every access inside the fingerprint array
                array = []
                for accessPoint in fingerprint:                
                    if accessPoint['macAddress'] not in forbidenMacAddresses:
                        array.append(accessPoint)

                #updates counter
                cont += 1
                
                #Adds the fingerprint into the array
                
                fingerprints.append(array)
                #verifies if there are enough fingerprints
                if cont == 10:
                    break
        return fingerprints
    except IOError as e:
        print(e)
        print "Error, couldn't find JSON collected data."