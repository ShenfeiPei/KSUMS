cimport numpy as np
import numpy as np
np.import_array()

from IDEAL_NPU import funs as Ifuns


from .Graph_ cimport Graph

cdef class PyGraph:
    cdef Graph c_Graph

    def __cinit__(self, int V):
        self.c_Graph = Graph(V)

    def addEdge(self, int v, int w):
        self.c_Graph.addEdge(v, w)


