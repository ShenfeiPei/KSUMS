#ifndef _MY_H
#define _MY_H
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <list>
#include <set>
#include <map>
#include <ctime>
#include <math.h>
#include <limits.h>
#include <omp.h>

#define NUM_THREADS_PEI 12

template <typename T>
void readM(std::string name, unsigned int N, unsigned int K, unsigned int k, T *M);

template <typename T>
T median_v(T *v, int n, int copy);

template <typename T>
T sum_v(T *v, int n);

int exist_f(int *v, int n, int x);

template <typename T>
void argsort_f(T *v, int n, int *ind);

template <typename T>
void show_M(T *Matrix, int N, int M, int n, int m);

template <typename T>
void readM(std::string name, unsigned int N, unsigned int K, unsigned int k, T *M){

    std::fstream in_f;
    T *tmp_K = new T[K];
    in_f.open(name.c_str(), std::ios::in | std::ios::binary);

    if (!in_f) std::cout << "fail to open the file" <<std::endl;
    else{
        for (unsigned i = 0; i < N; i++){
            in_f.read((char*)tmp_K, sizeof(T)*K);
            for (unsigned j = 0; j < k; j++){
                M[i*k + j] = tmp_K[j];
            }
        }
        in_f.close();
    }
}
// ctypes can not handle fstream
template <typename T>
void readM_C(std::string name, unsigned int N, unsigned int K, unsigned int k, T *M){
    T *tmp_K = new T[K];
    FILE *in_f=fopen(name.c_str(), "rb");

    for (int i = 0; i < N; i++){
        fread(tmp_K, sizeof (int), K, in_f);
        for (int j = 0; j < k; j++){
            M[i*k + j] = tmp_K[j];
        }
    }
    fclose(in_f);
}

template <typename T>
T median_v(T *v, int n, int copy){
    T ret;
    if (copy==1){
        T *v_sorted = new T[n];
        for (int i = 0; i < n; i++) v_sorted[i] = v[i];
        std::sort(v_sorted, v_sorted + n);
//        if (n % 2 == 1){
//            ret = v_sorted[n/2];
//        }else{
//            ret = (v_sorted[n/2 - 1] + v_sorted[n/2])/2;
//        }
        ret = v_sorted[n/2];
    }else{
        std::sort(v, v + n);
        ret = v[n/2];
//        if (n % 2 == 1){
//            ret = v[n/2];
//        }else{
//            ret = (v[n/2 - 1] + v[n/2])/2;
//        }
    }
    return ret;
}

template <typename T>
T sum_v(T *v, int n){
	T ret = 0;
	for (int i = 0; i < n; i++){
		ret += v[i];
	}
	return ret;
}

int exist_f(int *v, int n, int x){
	int flag = -1;

	for (int i = 0; i < n; i++){
		if (v[i] == x){
			flag = i;
			break;
		}
	}

	return flag;
}

template <typename T>
void show_M(T *Matrix, int N, int M, int n, int m){
	for (int i = 0; i < std::min(n, N); i++){
		for (int j = 0; j < std::min(m, M); j++){
			std::cout << Matrix[i*M + j] << ", ";
		}
		std::cout << std::endl;
	}
}

template <typename T>
void argsort_f(T *v, int n, int *ind){
	for (int i = 0; i < n; i++) ind[i] = i;
	std::sort(ind, ind + n, [&v](int i1, int i2){ return v[i1] < v[i2]; });
}

template <typename T, typename U>
void argsort_TwoArr(T *v1, U *v2, int n, int *ind){
	for (int i = 0; i < n; i++) ind[i] = i;
	std::sort(ind, ind + n, [&v1, &v2](int i1, int i2){ return v1[i1] < v1[i2] || (v1[i1] < v1[i2] + 1e-8 && v2[i1] > v2[i2]); });
}

#endif
