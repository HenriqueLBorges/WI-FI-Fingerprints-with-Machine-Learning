from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['teste']
users = db['users']
points = db['interest_points']

def test():
    for u in users.find():
        print(u)

def addInterestPoint(interestPoint):
    points.insert(interestPoint)

def getAccessPoints(accessPoints, floor):
    cursor = points.find({})
    fingerprints = []
    for fingerprint in cursor:
        fingerprints.append(fingerprint)
    return fingerprints

def getInterestPoint(room):
    cursor = points.find({'room': room})
    for fingerprint in cursor:
        return fingerprint

def addNewFingerprints(room, fingerprints):
    interestPoint = None
    interestPoint = getInterestPoint(room)

    if interestPoint is not None:
        newAdreesses = []
        #Get new fingerprints addresses list
        for fingerprint in fingerprints:
            newAdreesses = list(set(newAdreesses) - set(fingerprint['fingerprints_order']))

        #Sums the diferrence between old fingerprint_order and newAdresses into fingerprint_order
        newAdreesses = list(set(newAdreesses) - set(interestPoint['fingerprints_order']))
        points.update({'room': room}, {'$push': {'fingerprints': fingerprints, 'fingerprint_order': newAdreesses}}, upsert=False)