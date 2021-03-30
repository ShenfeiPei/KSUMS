#ifndef CPPFUNS_H_
#define CPPFUNS_H_

#include <iostream>
#include <fstream>
#include <vector>
#include <valarray>
#include <algorithm>
#include <functional>
#include <numeric>

using namespace std;

namespace cf{
    void EuDist2(vector<vector<double>> &A, vector<vector<double>> &B, vector<vector<double>> &C);

    void EuDist2(vector<vector<double>> &A, vector<double> &anorm, vector<vector<double>> &B, vector<double> &bnorm, vector<vector<double>> &C);

    void EuDist2(valarray<valarray<double>> &A, valarray<double> &anorm, valarray<valarray<double>> &B, valarray<double> &bnorm, valarray<valarray<double>> &C);

    void EuDist2_byCol(vector<vector<double>> &A, vector<vector<double>> &B, vector<vector<double>> &C);

    void EuDist2_byCol(vector<vector<double>> &A, vector<double> &anorm, vector<vector<double>> &B, vector<double> &bnorm, vector<vector<double>> &C);

    void square_sum_by_row(vector<vector<double>> &X, vector<double> &norm);
    void square_sum_by_row(valarray<valarray<double>> &X, valarray<double> &norm);
    void square_sum_by_col(vector<vector<double>> &X, vector<double> &norm);

    template <typename T, typename U>
    void argsort_TwoArr(vector<T> &v1, vector<U> &v2, vector<int> &ind);

    template <typename T>
    double median_vec2d(vector<vector<T>> &v);

    template <typename T>
    double median_v(vector<T> &v, int copy);

    template <typename T>
    void symmetry(vector<vector<int>> &NN, vector<vector<T>> &NND, int argument, T fill_ele);

    template<typename T>
    void read_2Dvec(std::string name, unsigned int K, std::vector<std::vector<T>> &M);

    template<typename T>
    void show_2Dvec(std::vector<std::vector<T>> &Vec, unsigned int n, unsigned int m);

    template<typename T>
    void argsort_f(vector<T> &v, vector<int> &ind);

    double maximum_2Dvec(std::vector<std::vector<double>> &Vec);

    template<typename T>
    void write_vec(std::string name, std::vector<T> &y);
}

#endif
