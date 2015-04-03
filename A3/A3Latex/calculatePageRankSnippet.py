#calculate PageRank
import networkx as nx
dg=nx.DiGraph()
dg.add_node(11)

dg.add_edges_from([(0,3), (3,0), (2,1), (2,0), (5,0), (4,0), (4,2), (10,4), (9,4), (8,4), (7,4), (6,4), (5,4), (4,5), (10,0), (9,0), (8,4)])
pr = nx.pagerank(dg, alpha=0.85, max_iter=100)
print pr