from libcpp.vector cimport vector

cdef extern from "CppFuns.cpp":
    pass

cdef extern from "Keep_order.cpp":
    pass

cdef extern from "Keep_order.h":
    cdef cppclass Keep_order:
        int N
        int c
        int* o2ni
        int* o2c
        int* c2o

        ctypedef struct lr_ind:
            int l
            int r

        lr_ind *ni2o

        Keep_order() except+
        Keep_order(vector[int] y, int N, int c) except +

        void sub(int ind)
        void add(int ind)


