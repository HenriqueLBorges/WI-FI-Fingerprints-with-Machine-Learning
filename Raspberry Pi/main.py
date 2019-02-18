import json
import pathSolver.pathSolver as solver
import wiFiFingeprints.wipy as wipy
import requests
import input
import utils
import tester
import audio.audio as audio
#import compass as compass
import compassTest as compass
from time import sleep

#Default timer constant
defaultTimer = 4

def getPosition(host, fingerprints, expected):
    params = {'class': expected}
    headers = {'Authorization': 'Bearer 123'}
    response = requests.post(host + '/addFingerprints', params=params, headers=headers, data=None, json=fingerprints)
    #print 'response = ' + str(response.text)
    
    if response.status_code != requests.codes.ok:
        print 'Error on API request'
        print(response.text)
    else:
        return response.text

def main(data):
    test = data['debug']
    exit = False
    path = []
    destination = ''
    currentPosition = ''
    nextPosition = ''

    if test: print 'Debug mode activated.'

    while not exit:
        #Plays a greetings audio
        audio.greetings()

        #Destination loop.
        while True:
            while True:
                if test: print 'Input your destination'
                
                #Plays a audio message that warns the user to input a destination.
                audio.inputDestination()

                if test and data['keyboard']:
                    destination = raw_input('Room = ')
                else:
                    destination = input.inputRoom()
                if destination != '': break

            #Current location loop
            while True:
                #Gets current position.
                if test and data['disableGetFingerprints']:
                    currentPosition = raw_input('Current Location = ')
                else:
                    fingerprints = []
                    for i in range(10):
                        fingerprints.append(wipy.getFingerprint())
                    currentPosition = getPosition(data['api_host'], fingerprints, '')
                #I need to implement a way to get current location    
                if currentPosition != '': break

            path = solver.solve(currentPosition, destination)

            #Verifies if there is a path between current position and destination.
            if path: break
            else: 
                print 'Error - it was no possible to find a path. Please verify your current position and destination.'
                #Plays a feedback audio
                audio.routeError()

        if test:
            print 'path = ' + str(path)

        currentPosition = path.pop()

        #Plays the current position feedback.
        audio.currentLocation()
        audio.room(currentPosition)

        #Plays the destination audio
        audio.destination()
        audio.room(destination)

        #Travel loop
        while len(path) > 0:
            nextPosition = path.pop()

            edge = solver.getInstruction(currentPosition, nextPosition)
            if not edge: 
                if test: print('Error - It was not possible to get the instruction.')
                #Plays a feedback audio
                audio.routeError()
                break
            else:
                if test: 
                    print 'Next step is head ' + compass.compassBearing(edge['metadata']['type']) + ' to room ' + edge['target'] + '.'
                    print 'Waiting ' + str(defaultTimer * edge['metadata']['weight']) + ' secods...'

                #Plays an audio to warn about direction
                audio.frontOf()
                audio.direction(compass.compassBearing(edge['metadata']['type']))

                #Waits for the user to be in the correct position
                while True:
                    try:
                        currenDirection = compass.getCompassBearing()

                        #if test:
                            #print 'current Direction = ' + str(currenDirection) + ' and angle = ' + str(compass.getSensorBearing())
                            #print 'oriented Direction = ' + str(compass.compassBearing(edge['metadata']['type']))
                        
                        if currenDirection == compass.compassBearing(edge['metadata']['type']):
                            break 
                        else:
                            difference = compass.getDifference(currenDirection, compass.compassBearing(edge['metadata']['type']))

                            if test:
                                print 'Difference between cardinal1 and cardinal2 = ' + str(difference)
                            
                            if difference > 0:
                                if test: 
                                    print 'Turn right a little to stay in the correct position...'
                                audio.turnRight()
                            else: 
                                if test:
                                    print 'Turn left a little to stay in the correct position...'
                                audio.turnLeft()

                    except Exception as e:
                        if test:
                            print 'Compass exception = ' + str(e)
                        audio.compassError()
                        break

                #Plays the instruction
                audio.instruction(edge['target'])
                
                #Waits for the use to follow the instruction
                sleep(defaultTimer * edge['metadata']['weight'])
                
                #Stores the last positions to identify a new currentPosition
                lastPositions = []

                #Waits for the current position be equal to next positions
                for i in range(5):
                    fingerprints = []

                    if data['disableGetFingerprints']:
                        fingerprints = tester.getSamples(nextPosition, data['forbidenMacAddresses'])
                    else:
                        for i in range(10):
                            fingerprints.append(wipy.getFingerprint())
                        
                    #Executes the model passing the fingerprints.
                    result = getPosition(data['api_host'], fingerprints, nextPosition)
                    
                    #Stores the result
                    if i > 11:
                        lastPositions.append(result)

                    #if test:
                    #    print 'current position = ' + str(result) + ' and next position = ' + str(nextPosition)
                    
                    #if the result matches the next position
                    if result == nextPosition:
                        currentPosition = nextPosition
                        break

                    if i == 14:
                        if test: 
                            print 'Real position did not match the position expected.'
                            print 'last positions = ' + str(lastPositions)
                        currentPosition = utils.mostCommon(lastPositions)
                    
                #Verifies if we have already reached our destination.
                if currentPosition == destination:
                    if test: print 'Destination ' + destination + ' reached.'
                    
                    #Plays an audio to warn about direction
                    room = solver.getNode(destination)

                    audio.frontOf()
                    audio.direction(compass.compassBearing(room['metadata']['direction']))
                    
                    try:
                        #Waits for the user to be in the correct position
                        while True:
                            currenDirection = compass.getCompassBearing()
                            
                            if currenDirection == compass.compassBearing(room['metadata']['direction']):
                                break
                            else:
                                difference = compass.getDifference(currenDirection, room['metadata']['direction'])

                                if test:
                                    print 'Difference between cardinal1 and cardinal2 = ' + str(difference)
                                
                                if difference > 0:
                                    if test: 
                                        print 'Turn right a little to stay in the correct position...'
                                    audio.turnRight()
                                else: 
                                    if test:
                                        print 'Turn left a little to stay in the correct position...'
                                    audio.turnLeft()

                    except Exception as e:
                        audio.compassError()
                        break
                        
                    #Plays a finish audio
                    audio.finish()
                    break
                
                if currentPosition == nextPosition:
                    if test:
                        print 'Current position did match the next position.'
                    
                #If we're haven't reached the expected position, we get a new current position based on the last 3 results
                else:
                    #Plays a feedback audio
                    audio.wrongPosition()
                    audio.recalculating()

                    if test: print 'Current position did not match the position expected. Recalculating route...'
                    
                    path = solver.solve(currentPosition, destination)
                    
                    if path:
                        if test: print 'new path = ' + str(path)
                        currentPosition = path.pop()
                    else:
                        #Plays a feedback audio
                        audio.routeError()
                        if test: print 'Error - it was no possible to find a path. Please verify your current position and destination.'
                        break
        
        #Need to read the input to see if the user wants to travel more.
         
if __name__ == '__main__':
    #Opens and loads the condiguration file.
    try:
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
            main(data)
    except IOError as e:
        print(e)
        print "Error, couldn't find configuration file."
        audio.configError()