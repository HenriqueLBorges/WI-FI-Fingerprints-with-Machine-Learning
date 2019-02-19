#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Load python modules
import utils
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import time
import seaborn as sns
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


# In[2]:


#Saves the start time of the operation
start_time = time.time()


# In[3]:


def batch_classify(X_train, Y_train, X_test, Y_test, no_classifiers = 5, verbose = True):
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
    return dict_models


# In[4]:


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


# In[ ]:


#Reads dataset CSV file
#data = pd.read_csv('./interest_points.csv', low_memory=False)


# In[19]:


#Loads the mac addresses dictionaire
macAddresses = utils.loadObj('macAddresses')

#print mac addresses dictionaire
print(macAddresses)


# In[20]:
data = pd.DataFrame()
teste = {}
teste['room'] = np.dtype(np.unicode_)
keys = [0] * len(macAddresses)
for key, value in macAddresses.iteritems():
    keys[value] = key
    teste[key] = np.dtype(np.int8)

print(teste)
chunks = pd.read_csv('./interest_points.csv', dtype=teste, low_memory=False, chunksize=100000)

for chunk in chunks:
      data = pd.concat([ data, chunk ] )

#print mac addresses keys that will be used as columns
print(keys)


# In[21]:


#Loads data from all mac addresses columns 
X = data[keys]

#Fills the gaps with zeros
X.fillna(0, inplace=True)

#Prints X data
print(X)


# In[22]:


#Loads the room column as our label
Y = ((data[['room']]).values.ravel())

#Prints labels
print(Y)


# In[23]:


#Splits data - 70% to train the model and the 30% to test the model after training
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)


# In[30]:


#Defines a dict containing all Machine Learning techniques that will be used
dict_classifiers = {
    #"Logistic Regression": LogisticRegression(),
    "Nearest Neighbors": KNeighborsClassifier(n_neighbors=3),
    #"Linear SVC": LinearSVC(penalty='l1', C=100.0, dual=False, max_iter=10000),
    #"Gradient Boosting Classifier": GradientBoostingClassifier(n_estimators=1000),
    "Decision Tree": tree.DecisionTreeClassifier(min_samples_split=50),
    #"SGDClassifier": SGDClassifier(n_jobs=-1, penalty='l1', l1_ratio=1,tol=None, max_iter=10000),
    #"Random Forest": RandomForestClassifier(n_estimators=1000),
    #"Neural Net": MLPClassifier(alpha = 1),
    #"Naive Bayes": GaussianNB(),
    #"AdaBoost": AdaBoostClassifier(),
    #"QDA": QuadraticDiscriminantAnalysis(),
    #"Gaussian Process": GaussianProcessClassifier()
}


# In[31]:


dict_models = batch_classify(X_train, Y_train, X_test, Y_test, no_classifiers = 8)
display_dict_models(dict_models)
elapsed_time = time.time() - start_time
print 'Time to train models = ' + str(elapsed_time) + ' seconds.'


# In[ ]:




