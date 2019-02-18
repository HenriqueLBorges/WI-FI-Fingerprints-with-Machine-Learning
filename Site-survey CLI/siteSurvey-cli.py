import commands
import sys
import os
import uuid
import mongo

comamnds = ('addf', 'rmf', 'help')

def newInterestPoint():
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
        'observations': ''
    }

    while(interestPoint['room'] != ''):
        interestPoint['room'] = raw_input('Room = ')

    while(not interestPoint['floor'].isdigit()):
        try:
            interestPoint['floor'] = int(raw_input('Floor = '))
        except ValueError:
            print 'Invalid number'

    while(interestPoint['observations'] != ''):
        interestPoint['observations'] = raw_input('Observations = ')
    
    addInterestPoint(interestPoint)

    return getInterestPoint(interestPoint['room'])

def interestPoints():
    interestPoint = None
    while True:
        answer = raw_input('Create a new interest point? Y or N\n')
        if answer == 'Y':
            interestPoint = newInterestPoint()
            break
        elif answer == 'N':
            while True:
                interestPoint = getInterestPoint(raw_input('Interest point room: '))
                if interestPoint is not None:
                    break
                else: print 'Not a valid interest point'
            break  
    return interestPoint      

def execute(tokens):
    #print tokens
    for token in tokens:
        if token == 'addf':
            seriesCommand = False #flag to add a certain number of fingerprints one after another
            numSeries = 0
            
            for i in range(1, len(tokens)):
                if  tokens[i] == '-s':
                    seriesCommand = True
                elif tokens[i].isdigit() and seriesCommand:
                    numSeries = tokens[i]
                    break

            if not seriesCommand:
                numSeries = 1

            interestPoint = interestPoints()
            newFingerprints = []
            
            #Iterates over the number of fingerprint the usar wants to add
            for i in range(0, numSeries):
                newFingerprints[i] = getFingerprint()
                
            #Adds the new fingerprints into the interest point
            addNewFingerprints(interestPoint['room'], newFingerprints)

            print 'Added ' + str(numSeries) + ' fingerprint into interest point of room ' + interestPoint['room']
            break
        elif token == "rmf":
            allCommand = False #flag to erase all fingerprints
            locationCommand = False #flag to remove the location from the dabase too
            for i in range(1, len(tokens)):
                if  tokens[i] == '-a':
                    allCommand = True
                elif  allCommand and tokens[i] == '-l':
                    locationCommand = True
            if allCommand and locationCommand:
                print 'rmf -a -l'
            elif allCommand:
                print 'rmf -a'
            else: print 'rmf'
            break
        elif token == 'help':
            print '1. addf - adds a fingerprint to the current location (-s <integer> option to add a certain number of fingerprints to the same location)\n'
            print '2. rmf - removes a fingerprint from the dabase (-a option to remove all fingerprints form the location)\n'
            print '3. exit - exits site-survey cli)'
            break
        elif token == "exit":
            sys.exit(0)
        else: print 'unknown command\ntype help to get a list of the commands'

print 'site-survey cli'
while (True):
    execute(raw_input('> ').split(' '))