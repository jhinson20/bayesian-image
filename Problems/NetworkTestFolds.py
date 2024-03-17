#I will be testing properties of the dotline dataset using a network with the probability of shape being left at 60/40

import tkinter as tk
import pandas as pd
import os
from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete.CPD import TabularCPD
from pgmpy.estimators import BayesianEstimator
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
import numpy as np

#Set global variable values

numberNodes = 4
sampleSize = 1000
numberSplits = 5
seed = 84
_confusion = [[0, 0], [0, 0]]

#Creates file object
fileName = 'data/dotLine.csv'

dataFile = pd.read_csv(fileName)

if not os.path.isfile(fileName):
    print('file dn exist')

#Randomly select data
data = dataFile.sample(n=sampleSize, random_state=seed, replace=True)

#Create the folds for the data
kf = KFold(n_splits=numberSplits, shuffle=False)

#Creates the bayesian network
edges = [('shape', 'x0'), ('shape', 'x1'), ('shape', 'x2'), ('shape', 'x3')]

graph = BayesianNetwork(edges)

for foldNum, (train_index, test_index) in enumerate(kf.split(data), 1):

    #Select training and test data based on the indicies of the fold
    train = data.iloc[train_index]
    test = data.iloc[test_index]

    #Fit data to network
    graph.fit(train, state_names={'shape': [0, 1], 'x0': [0, 1], 'x1': [0, 1], 'x2': [0, 1], 'x3': [0, 1]}, 
            estimator=BayesianEstimator, prior_type='BDeu', complete_samples_only=False)

    #Makes the shape estimation uniform
    #shape_cpd = TabularCPD('shape', 2, [[0.5],[0.5]])
    #graph.add_cpds(shape_cpd)

    infer = VariableElimination(graph)

    #Arrays that will contain the actual and predicted values of each of the rows from the test set
    pred_test = []
    actu_test = []

    #Evaluating test data

    for index, row in test.iterrows():
        pred_shape = row['shape']

        nodeNames = list("x" + str(i) for i in range(numberNodes))

        #Creating a dictionary with all of the node values
        evidenceDict = {}

        for i in range(numberNodes):
            evidenceDict[nodeNames[i]] = row[nodeNames[i]]

        #Getting the prediction based on the given evidence dictionary
        pred_shape = str(infer.map_query(variables = ["shape"], evidence= evidenceDict))
        pred_shape = int(pred_shape[pred_shape.find(':') + 1 : pred_shape.rfind('}')].strip())

        #Appending the prediction to the list
        pred_test.append(pred_shape)

        #Build query string for the actual value of the shape
        query_string = ""

        for key, value in evidenceDict.items():
            query_string += key + " == " + str(value) + " and "

        query_string = query_string[:query_string.rfind("and")-1]

        #Getting the actual value of the shape given the same activated nodes from the original data set
        actual_row = dataFile.query(query_string).iloc[0]

        #Appending the actual value to the list
        actu_test.append(int(actual_row['shape']))

    matrix = confusion_matrix(actu_test, pred_test)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            _confusion[i][j] += matrix[i][j] 

tn = _confusion[0][0]
fp = _confusion[0][1]
fn = _confusion[1][0]
tp = _confusion[1][1]

accuracy = (tp+tn)/(tp+tn+fp+fn)
sensitivity = tp/(tp+fn)
specificity = tn/(tn+fn)

#Calculations are made with 0 being the value of a dot and 1 being the value of a line
#This means that a false negative is the network predicting a dot when the actual is a line, as dots are negative (0) and lines are positive (1)
print("-"*30)
print("Confusion Matrix: " + str(_confusion))
print("Accuracy is {0:.2f}%.".format(accuracy * 100))
print("Sensitivity is {0:.2f}%.".format(sensitivity * 100))
print("Specificity is {0:.2f}%.".format(specificity * 100))
print("-"*30)
