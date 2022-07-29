
import numpy as np
import pandas as pd
from scipy import stats

from sklearn import metrics
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import confusion_matrix
from sklearn.metrics import adjusted_rand_score as ari_ori
from sklearn.metrics import adjusted_mutual_info_score as ami_ori
from sklearn.metrics import normalized_mutual_info_score as nmi_ori


def precision(y_true, y_pred):
    assert (len(y_pred) == len(y_true))
    N = len(y_pred)
    y_df = pd.DataFrame(data=y_pred, columns=["label"])
    ind_L = y_df.groupby("label").indices
    ni_L = [stats.mode(y_true[ind]).count[0] for yi, ind in ind_L.items()]
    return np.sum(ni_L) / N


def multi_precision(y_true, Y):
    ret = np.array([precision(y_true=y_true, y_pred=y_pred) for y_pred in Y])
    return ret


def recall(y_true, y_pred):
    re = precision(y_true=y_pred, y_pred=y_true)
    return re


def multi_recall(y_true, Y):
    ret = np.array([recall(y_true=y_true, y_pred=y_pred) for y_pred in Y])
    return ret


def accuracy(y_true, y_pred):
    """Get the best accuracy.

    Parameters
    ----------
    y_true: array-like
        The true row labels, given as external information
    y_pred: array-like
        The row labels predicted by the model

    Returns
    -------
    float
        Best value of accuracy
    """

    cm = confusion_matrix(y_true=y_true, y_pred=y_pred)
    cost_m = np.max(cm) - cm
    indices = linear_sum_assignment(cost_m)
    indices = np.asarray(indices)
    indexes = np.transpose(indices)
    total = 0
    for row, column in indexes:
        value = cm[row][column]
        total += value
    return total * 1. / np.sum(cm)


def multi_accuracy(y_true, Y):
    ret = np.array([accuracy(y_true=y_true, y_pred=y_pred) for y_pred in Y])
    return ret


def fmi(y_true, y_pred):
    ret = metrics.fowlkes_mallows_score(labels_true=y_true, labels_pred=y_pred)
    return ret


def multi_fmi(y_true, Y):
    ret = np.array([fmi(y_true=y_true, y_pred=y_pred) for y_pred in Y])
    return ret


def ari(y_true, y_pred):
    ret = ari_ori(labels_true=y_true, labels_pred=y_pred)
    return ret


def multi_ari(y_true, Y):
    ret = np.array([ari(y_true=y_true, y_pred=y_pred) for y_pred in Y])
    return ret


def ami(y_true, y_pred, average_method="max"):
    ret = ami_ori(labels_true=y_true, labels_pred=y_pred, average_method=average_method)
    return ret


def multi_ami(y_true, Y):
    ret = np.array([ami(y_true=y_true, y_pred=y_pred) for y_pred in Y])
    return ret


def nmi(y_true, y_pred, average_method="max"):
    ret = nmi_ori(labels_true=y_true, labels_pred=y_pred, average_method=average_method)
    return ret


def multi_nmi(y_true, Y):
    ret = np.array([nmi(y_true=y_true, y_pred=y_pred) for y_pred in Y])
    return ret
