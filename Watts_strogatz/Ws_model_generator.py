import numpy as np
import networkx as nx

class Ws_generator:
    def __init__(self, n, k):
       self.num_vertices = n
       self.G = nx.Graph()
       if k % 2 != 0:
           raise ValueError
       self.halfk = int(k/2)
       for intial_vertex in range(self.num_vertices):
           edge_of_i = [(intial_vertex, (intial_vertex+end_vertex+1) % self.num_vertices ) 
                        for end_vertex in range(self.halfk)]
           self.G.add_edges_from(edge_of_i)
       pass
