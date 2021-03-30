from libcpp.vector cimport vector

cdef extern from "Graph.cpp":
    pass

cdef extern from "Graph.h":
    cdef cppclass Graph:

        int V
        int num_clu
        vector[int] y
        vector[vector[int]] adj
        vector[vector[int]] adj_R

        Graph() except +
        Graph(int V) except +

        void addEdge(int v, int w)

        void connectedComponents()

        void RList_f()
