#I will be testing properties of the dotline dataset using a network with the probability of shape being left at 60/40

import tkinter as tk
import pandas as pd
import os
from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete.CPD import TabularCPD
from pgmpy.estimators import BayesianEstimator
from sklearn.model_selection import train_test_split

#Creates file object
fileName = 'data/dotLine.csv'

dataFile = pd.read_csv(fileName)

if os.path.isfile(fileName):
    print('exists')
else:
    print('dn exist')

numberNodes = 4
sampleSize = 1000
seed = 84

data = dataFile.sample(n=sampleSize, random_state=seed, replace=True)

train, test = train_test_split(data, test_size=.2, random_state=seed)

print(train)

print("\n\n\n")

print(test)

'''
#Add random rows from file to the data object, simulating user input
#Changes randomly every time program is ran
for i in range(100):
    row = data.sample(n=1)
    realShape = row['shape'].values[0]

    dot = {
        'shape': [realShape]
    }

    dataFrame = pd.DataFrame(dot)

    nodeNames = list("x" + str(i) for i in range(numberNodes))

    for i in range(len(nodeNames)):
        dataFrame[nodeNames[i]] = row[nodeNames[i]].values[0]

    newData = pd.concat([newData, dataFrame], ignore_index=True)


#Creates the bayesian network
edges = [('shape', 'x0'), ('shape', 'x1'), ('shape', 'x2'), ('shape', 'x3')]

graph = BayesianNetwork(edges)
graph.fit(newData, state_names={'shape': [0, 1], 'x0': [0, 1], 'x1': [0, 1], 'x2': [0, 1], 'x3': [0, 1]}, 
          estimator=BayesianEstimator, prior_type='BDeu', complete_samples_only=False)
#shape_cpd = TabularCPD('shape', 2, [[0.5],[0.5]])
#graph.add_cpds(shape_cpd)

infer = VariableElimination(graph)

#Testing row values for accuracy and other features
sumCorrect = 0

for index, row in data.iterrows():
    print(row['shape'])

    evidenceDict = {}

    nodeNames = list("x" + str(i) for i in range(numberNodes))

    for i in range(numberNodes):
        evidenceDict[nodeNames[i]] = row[nodeNames[i]]

    shape = str(infer.map_query(variables = ["shape"], evidence= evidenceDict))
    shape = int(shape[shape.find(':') + 1 : shape.rfind('}')].strip())

    if shape == row['shape']:
        print('Shapes match')
        sumCorrect += 1
    else:
        print('Shapes dont match')

numberRows = data.shape[0]

print("Accuracy is {0:.2f}%.".format((sumCorrect/numberRows)*100))

'''