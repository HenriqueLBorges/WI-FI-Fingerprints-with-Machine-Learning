#Used to train machine learn models
import utils
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import time
import seaborn as sns 
import genAliasDict
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.tree import export_graphviz
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix
import pickle
import time
import csv
import json

start_time = time.time()

def batch_classify(X_train, Y_train, X_test, Y_test, no_classifiers = 5, verbose = True):
    """
    This method, takes as input the X, Y matrices of the Train and Test set.
    And fits them on all of the Classifiers specified in the dict_classifier.
    The trained models, and accuracies are saved in a dictionary. The reason to use a dictionary
    is because it is very easy to save the whole dictionary with the pickle module.
    
    Usually, the SVM, Random Forest and Gradient Boosting Classifier take quiet some time to train. 
    So it is best to train them on a smaller dataset first and 
    decide whether you want to comment them out or not based on the test accuracy score.
    """
    
    dict_models = {}
    for classifier_name, classifier in list(dict_classifiers.items())[:no_classifiers]:
        t_start = time.clock()
        classifier.fit(X_train, Y_train)
        t_end = time.clock()
        
        t_diff = t_end - t_start
        train_score = classifier.score(X_train, Y_train)
        test_score = classifier.score(X_test, Y_test)
        
        dict_models[classifier_name] = {'model': classifier, 'train_score': train_score, 'test_score': test_score, 'train_time': t_diff}
        if verbose:
            print("trained {c} in {f:.2f} s".format(c=classifier_name, f=t_diff))
        
        #Exports classifier
        with open('./'+ classifier_name + '.pkl', 'wb') as f:
            pickle.dump(classifier, f, pickle.HIGHEST_PROTOCOL)
        if classifier_name == 'Decision Tree':
            keys = []
            for key, value in macAddresses.iteritems():
                keys.append(key)
            keys.sort()

            export_graphviz(classifier, out_file='classifier.dot', class_names=classifier.classes_,
                feature_names=keys, impurity=False, filled=True)

        #Creates machine learning model's confusion matrix    
        consfusionMatrix = confusion_matrix(Y_test, classifier.predict(X_test))
        consfusionMatrix = pd.DataFrame(consfusionMatrix,columns=classifier.classes_)
            
        consfusionMatrix ['label'] = classifier.classes_

        cols = consfusionMatrix.columns.tolist()
        cols = cols[-1:] + cols[:-1]

        consfusionMatrix = consfusionMatrix[cols]
        consfusionMatrix.to_csv('./' + classifier_name + '.csv', sep=',', index=False)    
    return dict_models



def display_dict_models(dict_models, sort_by='test_score'):
    cls = [key for key in dict_models.keys()]
    test_s = [dict_models[key]['test_score'] for key in cls]
    training_s = [dict_models[key]['train_score'] for key in cls]
    training_t = [dict_models[key]['train_time'] for key in cls]
    
    df_ = pd.DataFrame(data=np.zeros(shape=(len(cls),4)), columns = ['classifier', 'train_score', 'test_score', 'train_time'])
    for ii in range(0,len(cls)):
        df_.loc[ii, 'classifier'] = cls[ii]
        df_.loc[ii, 'train_score'] = training_s[ii]
        df_.loc[ii, 'test_score'] = test_s[ii]
        df_.loc[ii, 'train_time'] = training_t[ii]
    
    print(df_.sort_values(by=sort_by, ascending=False))


#Reads CSV file
#data = pd.read_csv('/home/pi/wifi-fingerprints/data/dataSet.csv')
data = pd.read_csv('/Users/henriqueborges/Documents/Senac/TCC/TCC 2/code/wifi-fingerprints API_python/api/data/dataset.csv')

#Loads the mac addresses dict
macAddresses = utils.loadObj('macAddresses')

keys = []
for key, value in macAddresses.iteritems():
    keys.append(key)

keys.sort()

# Gets macAlias and RSSI columns
X = data[keys]
X.fillna(0, inplace=True)

#Gets only the room column
Y = ((data[['room']]).values.ravel())

#Splits data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)

#print('X_test = ' + str(X_test.iloc[0]))
#print('Y_train = ' + str(Y_train))


#Saves test data
documents = {}
for i in range(0, len(Y_test)):
    print(i)
    room = Y_test[i]
    fingerprints = []
    
    for j in range(0, len(keys)):
        fingerprint = {}
        if(X_test.iloc[i][j] != 0):
            fingerprint['macAddress'] = keys[j]
            fingerprint['RSSI'] = X_test.iloc[i][j]    
            fingerprints.append(fingerprint)

    if Y_test[i] in documents:
        documents[Y_test[i]].append(fingerprints)
    else:
        documents[Y_test[i]] = []
        documents[Y_test[i]].append(fingerprints)

for key, fingerprints in documents.iteritems():
    with open('/Users/henriqueborges/Documents/Senac/TCC/imports/testData/' + key + '.json', 'w') as outfile:
            json.dump(documents[key], outfile)



#Types of classifiers
dict_classifiers = {
    #"Logistic Regression": LogisticRegression(),
    "Nearest Neighbors": KNeighborsClassifier(n_neighbors=3),
    "Linear SVC": LinearSVC(penalty='l1', C=100.0, dual=False),
    #"Gradient Boosting Classifier": GradientBoostingClassifier(n_estimators=1000),
    "Decision Tree": tree.DecisionTreeClassifier(min_samples_split=50),
    #"SGDClassifier": SGDClassifier(n_jobs=-1, penalty='l1', l1_ratio=1),
    #"Random Forest": RandomForestClassifier(n_estimators=1000),
    #"Neural Net": MLPClassifier(alpha = 1),
    #"Naive Bayes": GaussianNB(),
    #"AdaBoost": AdaBoostClassifier(),
    #"QDA": QuadraticDiscriminantAnalysis(),
    #"Gaussian Process": GaussianProcessClassifier()
}

#SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
#    decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
#    max_iter=-1, probability=False, random_state=None, shrinking=True,
#    tol=0.001, verbose=False)

dict_models = batch_classify(X_train, Y_train, X_test, Y_test, no_classifiers = 8)
display_dict_models(dict_models)
elapsed_time = time.time() - start_time
print 'Time to train models = ' + str(elapsed_time) + ' seconds.'