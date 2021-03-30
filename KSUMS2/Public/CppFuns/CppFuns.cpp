#include "CppFuns.h"

namespace cf{
    void EuDist2(vector<vector<double>> &A, vector<vector<double>> &B, vector<vector<double>> &C){

        int n = A.size();
        int m = B.size();

        vector<double> anorm(n, 0);
        square_sum_by_row(A, anorm);

        vector<double> bnorm(m, 0);
        square_sum_by_row(B, bnorm);

        #pragma omp parallel for
        for (int k = 0; k < n * m; k++){
            int i, j;
            i = k/m;
            j = k%m;
            C[i][j] = anorm[i] + bnorm[j] - 2 * inner_product(A[i].begin(), A[i].end(), B[j].begin(), (double) 0);
        }
    }

    void EuDist2_byCol(vector<vector<double>> &A, vector<vector<double>> &B, vector<vector<double>> &C){

        int n = A[0].size();
        int m = B[0].size();

        vector<double> anorm(n, 0);
        square_sum_by_col(A, anorm);

        vector<double> bnorm(m, 0);
        square_sum_by_col(B, bnorm);

        #pragma omp parallel for
        for (int k = 0; k < n * m; k++){
            int i, j;
            i = k/m;
            j = k%m;
            double tmp_d = 0;
            for (int l = 0; l < B.size(); l++){
                tmp_d += A[l][i] * B[l][j];
            }
            C[i][j] = anorm[i] + bnorm[j] - 2 * tmp_d;
        }
    }

    void EuDist2(vector<vector<double>> &A, vector<double> &anorm, vector<vector<double>> &B, vector<double> &bnorm, vector<vector<double>> &C){

        int n = A.size();
        int m = B.size();

        #pragma omp parallel for
        for (int k = 0; k < n * m; k++){
            int i, j;
            i = k/m;
            j = k%m;
            C[i][j] = anorm[i] + bnorm[j] - 2 * inner_product(A[i].begin(), A[i].end(), B[j].begin(), (double) 0);
        }
    }

    void EuDist2(valarray<valarray<double>> &A, valarray<double> &anorm, valarray<valarray<double>> &B, valarray<double> &bnorm, valarray<valarray<double>> &C){

        int n = A.size();
        int m = B.size();

        #pragma omp parallel for
        for (int k = 0; k < n * m; k++){
            int i, j;
            i = k/m;
            j = k%m;
            C[i][j] = anorm[i] + bnorm[j] - 2 * (A[i]*B[j]).sum();
        }
    }

    void EuDist2_byCol(vector<vector<double>> &A, vector<double> &anorm, vector<vector<double>> &B, vector<double> &bnorm, vector<vector<double>> &C){

        int n = A[0].size();
        int m = B[0].size();

        #pragma omp parallel for
        for (int k = 0; k < n * m; k++){
            int i, j;
            i = k/m;
            j = k%m;
            double tmp_d = 0;
            for (int l = 0; l < B.size(); l++){
                tmp_d += A[l][i] * B[l][j];
            }
            C[i][j] = anorm[i] + bnorm[j] - 2 * tmp_d;
        }
    }

    void square_sum_by_row(vector<vector<double>> &X, vector<double> &norm){

        #pragma omp parallel for
        for (int i = 0; i < X.size(); i++){
            norm[i] = inner_product(X[i].begin(), X[i].end(), X[i].begin(), (double) 0);
        }
    }

    void square_sum_by_row(valarray<valarray<double>> &X, valarray<double> &norm){

        #pragma omp parallel for
        for (int i = 0; i < X.size(); i++){
            norm[i] = (X[i] * X[i]).sum();
        }
    }

    void square_sum_by_col(vector<vector<double>> &X, vector<double> &norm){

        #pragma omp parallel for
        for (int j = 0; j < X[0].size(); j++){
            norm[j] = 0;
            for (int i = 0; i < X.size(); i++){
                norm[j] += X[i][j] * X[i][j];
            }
        }
    }

    template <typename T, typename U>
    void argsort_TwoArr(vector<T> &v1, vector<U> &v2, vector<int> &ind){
        iota(ind.begin(), ind.end(), 0);
        std::sort(ind.begin(), ind.end(), [&v1, &v2](int i1, int i2){ return v1[i1] < v1[i2] || (v1[i1] < v1[i2] + 1e-8 && v2[i1] > v2[i2]); });
    }
    template void argsort_TwoArr<int, int>(vector<int> &v1, vector<int> &v2, vector<int> &ind);
    template void argsort_TwoArr<double, double>(vector<double> &v1, vector<double> &v2, vector<int> &ind);
    template void argsort_TwoArr<int, double>(vector<int> &v1, vector<double> &v2, vector<int> &ind);
    template void argsort_TwoArr<double, int>(vector<double> &v1, vector<int> &v2, vector<int> &ind);

    template <typename T>
    double median_vec2d(vector<vector<T>> &v){
        double ret;

        vector<T> v2;
        for (int i = 0; i < v.size(); i++){
            for (int j = 0; j < v[i].size(); j++){
                v2.push_back(v[i][j]);
            }
        }
        std::sort(v2.begin(), v2.end());
        ret = v2[v2.size()/2];

        return ret;

    }
    template double median_vec2d<int>(vector<vector<int>> &v);
    template double median_vec2d<double>(vector<vector<double>> &v);

    template <typename T>
    double median_v(vector<T> &v, int copy){
        double ret;
        if (copy==1){
            vector<T> v_sorted = v;
            std::sort(v_sorted.begin(), v_sorted.end());
           // if (n % 2 == 1){
           //     ret = v_sorted[n/2];
           // }else{
           //     ret = (v_sorted[n/2 - 1] + v_sorted[n/2])/2;
           // }
            ret = v_sorted[v.size()/2];
        }else{
            std::sort(v.begin(), v.end());
            ret = v[v.size()/2];
    //        if (n % 2 == 1){
    //            ret = v[n/2];
    //        }else{
    //            ret = (v[n/2 - 1] + v[n/2])/2;
    //        }
        }
        return ret;

    }
    template double median_v<int>(vector<int> &v, int copy);
    template double median_v<double>(vector<double> &v, int copy);

    template <typename T>
    void symmetry(vector<vector<int>> &NN, vector<vector<T>> &NND, int argument, T fill_ele){
        int N = NN.size();
        int knn = NN[0].size();

        if (argument == 1){
            vector<vector<int>> RNN;
            vector<vector<T>> RNND;
            RNN.resize(N);
            RNND.resize(N);

            int tmp_j = 0;
            double tmp_d = 0;
            for (int i = 0; i < N; i++){
                for (int k = 0; k < knn; k++){
                    tmp_j = NN[i][k];
                    tmp_d = NND[i][k];
                    RNN[tmp_j].push_back(i);
                    RNND[tmp_j].push_back(tmp_d);
                }
            }

            vector<bool> flag(N, false);
            for (int i = 0; i < N; i++){
                for (auto j : NN[i]){
                    flag[j] = true;
                }

                for (int k = 0; k < RNN[i].size(); k++){
                    tmp_j = RNN[i][k];
                    if (flag[tmp_j] == false){

                        NN[i].push_back(tmp_j);

                        tmp_d = RNND[i][k];
                        NND[i].push_back(tmp_d);
                    }
                }

                for (int k = 0; k < knn; k++){
                    tmp_j = NN[i][k];
                    flag[tmp_j] = false;
                }
            }
        }else{
            int id = 0;
            std::vector<int>::iterator it;
            for (int i = 0; i < N; i++){
                for (int j = 0; j < NN[i].size(); j++){
                    id = NN[i][j];
                    it = std::find(NN[id].begin(), NN[id].end(), i);
                    if (it == NN[id].end()){
                        NND[i][j] = fill_ele;
                    }
                }
            }
        }
    }
    template void symmetry<int>(vector<vector<int>> &NN, vector<vector<int>> &NND, int argument, int fill_ele);
    template void symmetry<double>(vector<vector<int>> &NN, vector<vector<double>> &NND, int argument, double fill_ele);

    template<typename T>
    void read_2Dvec(std::string name, unsigned int K, std::vector<std::vector<T>> &M){
        unsigned int N = M.size();
        unsigned int k = M[0].size();

        std::fstream in_f;
        T *tmp_K = new T[K];
        in_f.open(name.c_str(), std::ios::in | std::ios::binary);
        if(!in_f.is_open()){std::cout<<"open file error"<<std::endl;exit(-1);}

        for (unsigned int i = 0; i < N; i++){
            in_f.read((char*)tmp_K, sizeof(T)*K);
            M[i].assign(tmp_K, tmp_K + k);
        }
        in_f.close();
    }
    template void read_2Dvec<int>   (std::string name, unsigned int K, std::vector<std::vector<int>> &M);
    template void read_2Dvec<double>(std::string name, unsigned int K, std::vector<std::vector<double>> &M);

    template<typename T>
    void show_2Dvec(std::vector<std::vector<T>> &Vec, unsigned int n, unsigned int m){
        unsigned int N = Vec.size();
        unsigned int M = Vec[0].size();
        if (n > N || m > M) std::cout << "n (m) must be less or equal than N (M)." << std::endl;

        for (unsigned int i = 0; i < n; i++){
            for (unsigned int j = 0; j < m; j++){
                std::cout << Vec[i][j] << ", ";
            }
            std::cout << std::endl;
        }
    }
    template void show_2Dvec<int>(std::vector<std::vector<int>> &Vec, unsigned int n, unsigned int m);
    template void show_2Dvec<double>(std::vector<std::vector<double>> &Vec, unsigned int n, unsigned int m);


    template<typename T>
    void argsort_f(vector<T> &v, vector<int> &ind){
        for (int i = 0; i < v.size(); i++) ind[i] = i;
        std::sort(ind.begin(), ind.end(), [&v](int i1, int i2){ return v[i1] < v[i2]; });
    }
    template void argsort_f<int>(vector<int> &v, vector<int> &ind);
    template void argsort_f<double>(vector<double> &v, vector<int> &ind);

    double maximum_2Dvec(std::vector<std::vector<double>> &Vec){
        int N = Vec.size();
        std::vector<double> tmp(N, 0);

        for(int i = 0; i < N; i++){
            tmp[i] = *std::max_element(Vec[i].begin(), Vec[i].end());
        }

        double ret = *std::max_element(tmp.begin(), tmp.end());
        return ret;
    }


    template<typename T>
    void write_vec(std::string name, std::vector<T> &y){
        std::fstream in_f;
        in_f.open(name.c_str(), std::ios::out | std::ios::binary);
    //	in_f.write((char*)y, sizeof(T)*N);
        for(T &ele: y) in_f.write((char *)&ele, sizeof(T)) ;
        in_f.close();
    }
    template void write_vec<int>(std::string name, std::vector<int> &y);
    template void write_vec<double>(std::string name, std::vector<double> &y);

};
