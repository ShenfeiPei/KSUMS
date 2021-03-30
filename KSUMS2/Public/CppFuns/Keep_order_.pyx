# distutils: language = c++

cimport numpy as np
import numpy as np
np.import_array()

from Keep_order_ cimport Keep_order

cdef class PyKeepOrder:
    cdef Keep_order KO

    def __cinit__(self, y, int N, int c):
        self.KO = Keep_order(y, N, c)

    def _sub(self, ind):
        self.KO.sub(ind)

    def _add(self, ind):
        self.KO.add(ind)

    @property
    def N(self):
        return self.KO.N

    @property
    def o2ni(self):
        cdef np.ndarray[int, ndim=1, mode='c'] ret
        ret = np.zeros((self.KO.c,), dtype=np.int32)
        for i in range(self.KO.c):
            ret[i] = self.KO.o2ni[i]
        return ret
