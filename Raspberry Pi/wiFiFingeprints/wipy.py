import commands
import re
import uuid
import math
import utils

def setInterestPoint():

    interestPoint = {
        '_id': str(uuid.uuid1()),
        'room': '',
        'floor': 0, 
        'position': {
            'x': 0,
            'y': 0,
            'z': 0
        },
        'fingerprints': [],
        'fingerprints_order': [],
        'observations': 'Primeiro fingerprint'
    }

    fingerprints = []
    orders = []

    for i in range(3): 
        fingerprints.append(getFingerprint())
        orders.append(getFingerprintOrder(fingerprints[i]))
    
    #Mounts a fingerprint analyzer order containing all access points
    order = unionFingerprintOrders(orders)

    interestPoint['fingerprints'].append(normalizeFingerprints(fingerprints, order))
    interestPoint['fingerprints_order'] = order
    return interestPoint

#Union an list of fingerprints insert order in one order containing only the common macAddress'.
def unionFingerprintOrders(orders):
    size = len(orders)
    buckets = {}
    order = []

    for i in range(size):
        for j in range(len(orders[i])):
            if orders[i][j] in buckets:
                buckets[orders[i][j]] += 1
            else: buckets[orders[i][j]] = 1

    for i in range(len(buckets)):
        item = buckets.popitem()
        if item[1] == size:
            order.append(str(item[0]))

    return order

#Mounts a list containing the access' points' order inside an Wi-Fi Fingerprint.
def getFingerprintOrder(fingerprint):
    order = []
    for item in fingerprint:
        order.append(item['macAddress'])
    return order

#Order the Wi-Fi Fingerprint access points and return it.
def orderFingerprint(fingerprint, order):
    changes = True

    while changes:
        orderIndex = 0
        changes = False
        size = len(fingerprint)
        for i in range(size):
            if fingerprint[i]['macAddress'] != order[orderIndex] and i < size - 1:
                aux = fingerprint[i]
                fingerprint[i] = fingerprint[i + 1]
                fingerprint[i + 1] = aux
                changes = True
            else: orderIndex += 1
    return fingerprint

#Union a Wi-Fi Fingeprint list into one Wi-Fi Fingerprint tha contains only the common access points between all list itens and their average RSSI value.
def normalizeFingerprints(fingerprints, order):
    fingerprintNormalized = []
    
    for i in range(len(order)):
        result = 0.0
        for fingerprint in fingerprints:
            for item in fingerprint:
                if item['macAddress'] == order[i]:
                    result += item['RSSI']
                    break

        fingerprintNormalized.append({
            'macAddress': order[i],
            'RSSI':result / len(fingerprints)}) 

    return fingerprintNormalized

def getFingerprint():
    #Executes the command
    
    #For Macs OSX
    #output=commands.getstatusoutput('airport -s')
    
    #For Raspbian
    output=commands.getstatusoutput('sudo iwlist scan')
    
    outputText = output[1]
    outputText = outputText.replace("\n", " ")
    outputText = outputText.replace("level=", "level= ")
    lines = outputText.split('Cell ')

    fingerprint = []

    for line in lines:
        #Filters the mac address and it's RSSI value from line.
        macAddress = re.findall(r'((?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})', line)
        dBm = re.findall(r'(level= -?\d{0,2}\.{0,1}\d{0,2})', line)
    
        if dBm and macAddress:
            macAddress = str(macAddress[0])
            dBm = int(str(dBm[0]).replace("level= ", ""))

            #Adds the access point to the list
            fingerprint.append({
                'macAddress': macAddress,
                'RSSI': dBm
            })

    return fingerprint

def eucDist(fingerprint1, fingerprint2, order):
    result = 0.0
    for macAddress in order:
        indexFingeprint1 = utils.findInDict(fingerprint1, 'macAddress', macAddress)
        indexFingeprint2 = utils.findInDict(fingerprint2, 'macAddress', macAddress)
        
        if indexFingeprint1 is not None and indexFingeprint2 is not None:
            result += math.pow((fingerprint1[indexFingeprint1]['RSSI'] - fingerprint2[indexFingeprint2]['RSSI']), 2)

    return math.sqrt(result)

#Converts the fingerprint into a 2-D array.
def convertFingeprintTo2dArray(fingerprint):
    result = []

    for item in fingerprint:
        item = item.values()
        for i in range(0, len(item), 2):
            result.append([item[i], item[i + 1]])

    return result