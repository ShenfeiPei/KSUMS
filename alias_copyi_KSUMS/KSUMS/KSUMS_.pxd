from libcpp.vector cimport vector

from alias_copyi_KSUMS.Public.CppFuns.Keep_order_ cimport Keep_order

cdef extern from "CppFuns.cpp":
    pass

cdef extern from "KSUMS.cpp":
    pass

cdef extern from "KSUMS.h":
    cdef cppclass KSUMS:
        int N
        int knn
        int c_true
        vector[vector[int]] NN
        vector[vector[double]] NND
        vector[int] y

        int *hi
        int *hi_TF
        int *hi_count

        int *knn_c
        int num_iter
        double max_d
        double _time

        Keep_order KO

        KSUMS() except +
        KSUMS(vector[vector[int]]& NN, vector[vector[double]]& NND, int c_true) except +
        void opt()
        void construct_hi(int sam_i)
