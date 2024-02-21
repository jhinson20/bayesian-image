from pgmpy.models import BayesianNetwork
import pandas as pd
from pgmpy.inference import VariableElimination


data = pd.read_csv('Problems/data/Problem_32.csv')

graph = BayesianNetwork()

graph.add_node('S')
graph.add_node('O')
graph.add_edge('S', 'O')

graph.fit(data)

states = graph.states

infer = VariableElimination(graph)

#This is for P(S|O)
query1 = infer.query(variables = ["S"], evidence= {'O':1})
print(query1)

#This is for P(S|O')
query2 = infer.query(variables = ["S"], evidence= {'O':0})
print(query2)