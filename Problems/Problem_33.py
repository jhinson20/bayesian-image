from pgmpy.models import BayesianNetwork
import pandas as pd
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD

graph = BayesianNetwork()

graph.add_node('B')
graph.add_node('A')
graph.add_node('J')
graph.add_edge('B', 'A')
graph.add_edge('A', 'J')

cpd_B = TabularCPD(variable='B', variable_card=2, values=[[0.999], [0.001]])
cpd_A = TabularCPD(variable='A', variable_card=2, values=[[0.9984, 0.06], [0.0016, 0.94]],
                   evidence=['B'], evidence_card=[2])
cpd_J = TabularCPD(variable='J', variable_card=2, values=[[0.95, 0.1], [0.05, 0.9]],
                   evidence=['A'], evidence_card=[2])

graph.add_cpds(cpd_A,cpd_B, cpd_J)

states = graph.states

assert graph.check_model()

infer = VariableElimination(graph)

#This is for P(J|B)
query1 = infer.query(variables = ["J"], evidence= {'B':1})
print(query1)

#This is for P(S|B')
query2 = infer.query(variables = ["J"], evidence= {'B':0})
print(query2)