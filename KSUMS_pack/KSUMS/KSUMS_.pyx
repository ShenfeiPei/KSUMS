# distutils: language = c++

cimport numpy as np
import numpy as np
np.import_array()

from .KSUMS_ cimport KSUMS

cdef class PyKSUMS:
    cdef KSUMS c_KSUMS

    def __cinit__(self, np.ndarray[int, ndim=2] NN, np.ndarray[double, ndim=2] NND, c_true):
        self.c_KSUMS = KSUMS(NN, NND, c_true)

    def clu(self):
        self.c_KSUMS.opt()

    def _construct_hi(self, sam_i):
        self.c_KSUMS.construct_hi(sam_i)


    @property
    def y_pre(self):
        return self.c_KSUMS.y

    @property
    def time(self):
        return self.c_KSUMS._time
