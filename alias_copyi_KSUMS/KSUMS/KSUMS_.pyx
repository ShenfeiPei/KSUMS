# distutils: language = c++

cimport numpy as np
import numpy as np
np.import_array()

from .KSUMS_ cimport KSUMS

cdef class PyKSUMS:
    cdef KSUMS c_KSUMS

    def __cinit__(self, NN, NND, max_d, c_true):
        self.c_KSUMS = KSUMS(NN, NND, max_d, c_true)

    def opt(self):
        self.c_KSUMS.opt()

    @property
    def y_pre(self):
        return np.array(self.c_KSUMS.y)

    @property
    def time(self):
        return self.c_KSUMS._time
