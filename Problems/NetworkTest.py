import pandas as pd
import os
from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete.CPD import TabularCPD
from pgmpy.estimators import BayesianEstimator
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold

#Set global variable values

numberNodes = 4
sampleSize = 1000
numberSplits = 5
seed = 84
uniformShape = False
_accuracy = []
_sensitivity = []
_specificity = []
# _confusion = [[0, 0], [0, 0]]

#Creates file object
fileName = 'data/dotLine.csv'

dataFile = pd.read_csv(fileName)

if not os.path.isfile(fileName):
    print('file dn exist')

#Randomly select data
data = dataFile.sample(n=sampleSize, random_state=seed, replace=True)

#Create the folds for the data
kf = KFold(n_splits=numberSplits, shuffle=False)

for foldNum, (train_index, test_index) in enumerate(kf.split(data), 1):

    #Select training and test data based on the indicies of the fold
    train = data.iloc[train_index]
    test = data.iloc[test_index]

    #Creates the bayesian network
    edges = [('shape', 'x0'), ('shape', 'x1'), ('shape', 'x2'), ('shape', 'x3')]

    graph = BayesianNetwork(edges)

    #Fit data to network
    graph.fit(train, state_names={'shape': [0, 1], 'x0': [0, 1], 'x1': [0, 1], 'x2': [0, 1], 'x3': [0, 1]}, 
            estimator=BayesianEstimator, prior_type='BDeu', complete_samples_only=False)

    #Makes the shape estimation uniform if uniformShape is true
    if(uniformShape):
        shape_cpd = TabularCPD('shape', 2, [[0.5],[0.5]])
        graph.add_cpds(shape_cpd)

    infer = VariableElimination(graph)

    #Arrays that will contain the actual and predicted values of each of the rows from the test set
    pred_test = []
    actu_test = []

    #Evaluating test data

    for index, row in test.iterrows():
        pred_shape = row['shape']

        #Creates a list of node names, ['x0', 'x1', ...]
        nodeNames = list("x" + str(i) for i in range(numberNodes))

        #Creating a dictionary with all of the node values, {'x0' = 1, 'x1' = 0}
        evidenceDict = {}

        for i in range(numberNodes):
            evidenceDict[nodeNames[i]] = row[nodeNames[i]]

        #Getting the prediction based on the given evidence dictionary
        pred_shape = infer.map_query(variables = ["shape"], evidence= evidenceDict, show_progress=False)['shape']


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
        actu_test.append(actual_row['shape'])

    matrix = confusion_matrix(actu_test, pred_test)

    # for i in range(len(matrix)):
    #     for j in range(len(matrix[i])):
    #         _confusion[i][j] += matrix[i][j] 

    tn = matrix[0][0]
    fp = matrix[0][1]
    fn = matrix[1][0]
    tp = matrix[1][1]

    _accuracy.append((tp+tn)/(tp+tn+fp+fn))
    _sensitivity.append(tp/(tp+fn))
    _specificity.append(tn/(tn+fp))

#Calculations are made with 0 being the value of a dot and 1 being the value of a line
#This means that a false negative is the network predicting a dot when the actual is a line, as dots are negative (0) and lines are positive (1)
print("-"*50)
#print("Confusion Matrix: " + str(_confusion))
print("Accuracy is {0:.2f}%.".format((sum(_accuracy)/len(_accuracy)) * 100))
print("Sensitivity is {0:.2f}%.".format((sum(_sensitivity)/len(_sensitivity)) * 100))
print("Specificity is {0:.2f}%.".format((sum(_specificity)/len(_specificity)) * 100))
print("-"*50)