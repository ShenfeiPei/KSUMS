import os
import numpy as np
from alias_copyi_KSUMS.KSUMS import KSUMS
from alias_copyi_KSUMS.Public import Ifuns, Gfuns, Mfuns

knn = 20

# load date
file_path = os.path.dirname(__file__)
X, y_true, N, dim, c_true = Ifuns.load_mat(os.path.join(file_path, "data/Mpeg7_20200916.mat"))
print(N, dim, c_true)

NN, NND = Gfuns.knn_f(X, knn)

obj = KSUMS(NN.astype(np.int32), NND, c_true)
obj.clu()
y_pred = obj.y_pre


acc = Mfuns.accuracy(y_true=y_true, y_pred=y_pred)
print(acc)

#  paper: Mpeg7, acc = 0.554
#  run:   Mpeg7, acc = 0.555
