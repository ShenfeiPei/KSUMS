#ifndef _KSUMS_H
#define _KSUMS_H

#include <iostream>
#include <algorithm>
#include <fstream>
#include <stdlib.h>
#include <vector>
#include <ctime>
#include "CppFuns.h"
#include "Keep_order.h"

class KSUMS{
public:
    int N = 0;
    int knn = 0;
    int c_true = 0;

    std::vector<std::vector<int>> NN;
    std::vector<std::vector<double>> NND;
    std::vector<int> y;

    double *hi = nullptr;
    int *hi_TF = nullptr;
    int *hi_count = nullptr;

    int *knn_c = nullptr;
    int num_iter = 0;

    double max_d = 0;
    double _time = 0;

    Keep_order KO;

    KSUMS();
    KSUMS(std::vector<std::vector<int>> &NN, std::vector<std::vector<double>> &NND, double max_d, int c_true);
    ~KSUMS();

    void opt();

    void construct_hi(int sam_i);

};
#endif
