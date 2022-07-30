from libcpp.vector cimport vector

from alias_copyi_KSUMS.FeiPub.CppFuns.Keep_order_ cimport Keep_order

cdef extern from "CppFuns.cpp":
    pass

cdef extern from "KSUMS.cpp":
    pass

cdef extern from "KSUMS.h":
    cdef cppclass KSUMS:

        vector[int] y
        double _time

        int *hi
        int *hi_TF
        int *hi_count

        int *knn_c
        int num_iter

        Keep_order KO

        KSUMS() except +
        KSUMS(vector[vector[int]]& NN, vector[vector[double]]& NND, double max_d, int c_true) except +
        void opt()
