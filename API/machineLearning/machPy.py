#Executes a machine learning model
import pandas as pd
import numpy as np
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
from wiFiFingeprints import mongo
import time
import utils
import pickle
import cPickle

#Loads the trained model
#model = joblib.load('teste.pkl')

#with open('SVM.pkl', 'rb') as file:  
#    model = pickle.load(file)

#print 'type(v) = ' + str(type(model))

totals = {'A-E': 0, 'E169': 0, 'E168': 0, 'E167': 0, 'E166': 0, 'E-C': 0, 'C135': 0, 'C134': 0, 'C133': 0, 'C132': 0, 'C131': 0, 'B130': 0, 'C-B': 0, 'B129': 0, 'B128': 0, 'B127': 0, 'B126': 0, 'B-A': 0, 'A125': 0, 'A123': 0, 'A122': 0, 'A121': 0, 'A120': 0, 'A119': 0, 'A118': 0, 'A-E': 0, 'E169': 0, 'E168': 0, 'E167': 0, 'E166': 0}

def loadObj(name):
    #with open('./' + name + '.pkl', 'rb') as f:
    with open('./machineLearning/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

model = loadObj('Decision Tree')
#model = loadObj('Linear SVC')
#model = loadObj('Nearest Neighbors')

def getCurrentPosition(fingerprints):
    start_time = time.time()

    macAddresses = utils.loadObj('macAddresses')
    keys = []
    for key, _ in macAddresses.iteritems():
        keys.append(key)

    #sorts list
    keys.sort()
    print(keys)
    elapsed_time = time.time() - start_time

    x = np.array(fingerprints)
    x = x.reshape(1, -1)
    result = model.predict(x)
    #print('Elapsed time: ' + str(elapsed_time))
    return utils.mostCommon(result)


def getCurrentPosition1(fingerprint):
    start_time = time.time()

    #Imports the macAdresses list
    macAddresses = loadObj('macAddresses')
    
    items = [0] * len(macAddresses)

    #print 'teste = ' + str(macAddresses)
    for item in fingerprint:
        address = ''
        rssi = 0
        for key, value in item.iteritems():
            if key == 'macAddress':
                address = value
            elif key == 'RSSI':
                rssi = value        

        items[macAddresses[address]] = rssi

    #Creates a numpy array    
    data = np.array(items)

    #Reshape data cause we only have one item.
    data = data.reshape(1, -1)
    result = model.predict(data)
    
    #Calculates the ammount of time between the start and the end time of the method.
    elapsed_time = time.time() - start_time
    #print('Elapsed time: ' + str(elapsed_time))
    return utils.mostCommon(result)

def getCurrentPositionMultiple(fingerprints):
    start_time = time.time()

    #Imports the macAdresses list
    macAddresses = loadObj('macAddresses')
    
    items = [0] * len(macAddresses)
    results = []
    #print 'teste = ' + str(macAddresses)
    for fingerprint in fingerprints:
        for item in fingerprint:
            address = ''
            rssi = 0
            for key, value in item.iteritems():
                if key == 'macAddress':
                    address = value
                elif key == 'RSSI':
                    rssi = value        
            try:
                items[macAddresses[address]] = rssi
            except KeyError:
                pass
        results.append(np.array(items))

    #Creates a numpy array    
    data = np.array(results)

    #Reshape data cause we only have one item.
    
    #data = data.reshape(1, -1)
    #result = model.predict(data)

    results = model.predict_proba(data)

    labels = []

    for result in results:
        result = list(result)
        print(result)
        #for i in range(result.size):
            #print('class ' + str(model.classes_[i]) + ' - probability = ' + str(result [i]))
        #value = max(result)
        #print(result.index(max(result)))
        labels.append(model.classes_[result.index(max(result))])
    
    #Calculates the ammount of time between the start and the end time of the method.
    elapsed_time = time.time() - start_time
    print('Elapsed time: ' + str(elapsed_time))

    label = utils.mostCommon(labels)

    probabilities = 0.0

    index = list(model.classes_).index(label)
    cont = 0
    
    for result in results:
        result = list(result)
        print('probability = ' + str(result[index]))
        probabilities += result[index]
        cont += 1
    print 'Number of classes = ' + str(len(model.classes_))
    print 'probabilities = ' + str(probabilities/cont)
    print 'label = ' + str(label)
    if (probabilities/cont) >= 0.7:
        return label
    else:
        return 'unknown'

def getCurrentPositionProbabilist(fingerprint):
    start_time = time.time()

    #Imports the macAdresses list
    macAddresses = loadObj('macAddresses')
    
    items = [0] * len(macAddresses)

    #print 'teste = ' + str(macAddresses)
    for item in fingerprint:
        address = ''
        rssi = 0
        for key, value in item.iteritems():
            if key == 'macAddress':
                address = value
            elif key == 'RSSI':
                rssi = value        

        try:
            items[macAddresses[address]] = rssi
        except KeyError:
            pass

    #Creates a numpy array    
    data = np.array(items)

    #Reshape data cause we only have one item.
    data = data.reshape(1, -1)
    results = model.predict_proba(data)

    labels = []

    for result in results:
        result = list(result)
        #for i in range(result.size):
            #print('class ' + str(model.classes_[i]) + ' - probability = ' + str(result [i]))
        value = max(result)
        index = result.index(value)

    #Calculates the ammount of time between the start and the end time of the method.
    elapsed_time = time.time() - start_time
    print('Elapsed time: ' + str(elapsed_time))
    return model.classes_[index]

def getCurrentPositionMultiple1(fingerprints, expected_class):
    #print(totals)
    start_time = time.time()

    #Imports the macAdresses list
    macAddresses = loadObj('macAddresses')
    
    items = [0] * len(macAddresses)
    results = []

    for fingerprint in fingerprints:
        for item in fingerprint:
            address = ''
            rssi = 0
            for key, value in item.iteritems():
                if key == 'macAddress':
                    address = value
                elif key == 'RSSI':
                    rssi = value        
            try:
                items[macAddresses[address]] = rssi
            except KeyError:
                pass
        results.append(np.array(items))

    #Creates a numpy array    
    data = np.array(results)

    #Predict the results for each fingerprint collected
    result = model.predict(data)
    print 'classes = ' + str(result)

    #Calculate the total time to predict
    elapsed_time = time.time() - start_time
    print('Elapsed time: ' + str(elapsed_time))
    
    result_class = utils.mostCommon(result)
    
    #Verfies if the most commom result matches it's the expected class
    if result_class == expected_class:
        totals[result_class] += 1

        #Verifies if there are more than a n entries
        if totals[result_class] > 1:
            totals[result_class] = 0

            for i in range(len(result)):
                if result[i] == result_class:
                    #Add the fingerprint to it's interest point
                    mongo.addNewFingerprints(result_class, fingerprints[i])
                    break

    return result_class

