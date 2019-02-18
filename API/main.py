import json
import pathSolver.pathSolver as solver
import wiFiFingeprints.wipy as wipy
import machineLearning.machPy as machPy
import utils

def main(data):
    test = data['debug']
    exit = False
    path = []
    detination = ''
    currentPosition = ''
    nextPositions = ''
    macAddresses = utils.loadObj('./machineLearning/macAddress.pkl')

    if test: print 'Debug mode activated.'

    while not exit:
        #Destination loop.
        while True:
            while True:
                if test: print 'Input your destination'
                
                #Calls audio message that warns the user to input a destination.
                if test and data['keyboard']:
                    destination = raw_input('Room = ')
                #else:
                    #I need to implement a way to read the input from rapberry.
                if destination != '': break
        
            #Current location loop
            while True:
                #Gets current position.
                if test and data['disableIntialSearch']:
                    currentPosition = raw_input('Current Location = ')

                #I need to implement a way to get current location    
                if currentPosition != '': break

            path = solver.solve(currentPosition, destination)

            #Verifies if there is a path between current position and destination.
            if path: break
            else: print 'Error - it was no possible to find a path. Please verify your current position and destination.'
        
        currentPosition = path.pop()
        #Travel loop
        while len(path) > 0:
            nextPosition = path.pop()

            edge = solver.getInstruction(currentPosition, nextPosition)
            if not edge: print('Error - It was not possible to get the instruction.')
            else:
                if test: print 'Next step is head ' + edge['metadata']['type'] + ' to room ' + nextPosition + '.'
                
                #Stores the last positions to identify a new currentPosition
                lastPositions = []

                #Waits for the current position be equal to next positions
                for i in range(15):
                    fingerprints = []
                    fingerprints += wipy.getFingerprint()
                    items = [0] * (len(macAddresses) - len(fingerprints))
                    #print(fingerprints)
                    #for key, value in fingerprints.iteritems():
                    #    items.insert(macAddresses[key], value)
                    
                    #Executes the model passing the fingerprints.
                    result = machPy.getCurrentPosition1(fingerprints)
                    
                    #Stores the result
                    if i > 11:
                        lastPositions.append(result)

                    if test:
                        print 'current position = ' + str(result)
                    
                    #if the result matches the next position
                    if result is nextPosition:
                        break
                    if i == 14:
                        if test: print 'Real position did not match the position expected.'
                        
                        print(lastPositions)
                        currentPosition = utils.mostCommon(lastPositions)
                        print 'currentPosition = ' + str(currentPosition)
                    
                    
                #Verifies if we have already reached our destination.
                if currentPosition is destination:
                    if test: print 'Destination reached.'
                    break
                #If we're haven't reached the expected position, we get a new current position based on the last 3 results
                else:
                    path = solver.solve(currentPosition, destination)
                    if path:
                        currentPosition = path.pop()
                    else:
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
        print "Error, couldn't find configuration file."