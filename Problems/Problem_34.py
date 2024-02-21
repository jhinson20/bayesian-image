from pgmpy.models import BayesianNetwork
import pandas as pd
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD

graph = BayesianNetwork()

graph.add_node('S')
graph.add_node('O')
graph.add_node('F')
graph.add_edge('S', 'O')
graph.add_edge('S', 'F')

cpd_B = TabularCPD(variable='S', variable_card=2, values=[[0.29], [0.71]])
cpd_A = TabularCPD(variable='O', variable_card=2, values=[[0.95, 0.825], [0.05, 0.175]],
                   evidence=['S'], evidence_card=[2])
cpd_J = TabularCPD(variable='F', variable_card=2, values=[[0.945, 0.7], [0.055, 0.3]],
                   evidence=['S'], evidence_card=[2])

graph.add_cpds(cpd_A, cpd_B, cpd_J)

states = graph.states

assert graph.check_model()

print(states)

infer = VariableElimination(graph)

#This is for P(J|B)
query1 = infer.query(variables = ["S"], evidence= {'O':1, 'F':1})
print(query1)

#This is for P(S|B')
query2 = infer.query(variables = ["S"], evidence= {'O':0, 'F':0})
print(query2)