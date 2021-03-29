import numpy as np
from KSUMS_pack.KSUMS import KSUMS
from KSUMS_pack.Public import Ifuns, Gfuns, Mfuns

knn = 20

# load date
X, y_true, N, dim, c_true = Ifuns.load_mat("/home/pei/DATA/Mpeg7_20200916.mat")
print(N, dim, c_true)

NN, NND = Gfuns.knn_f(X, knn)

obj = KSUMS(NN.astype(np.int32), NND, c_true)
obj.clu()
y_pred = obj.y_pre


acc = Mfuns.accuracy(y_true=y_true, y_pred=y_pred)
print(acc)

paper: Mpeg7, acc = 0.554
run:   Mpeg7, acc = 0.555
