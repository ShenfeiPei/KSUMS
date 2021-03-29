#include "my.h"

template<typename T>
void read_M_vec2(std::string name, unsigned int K, std::vector<std::vector<T>> &M){
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
template void read_M_vec2<int>   (std::string name, unsigned int K, std::vector<std::vector<int>> &M);
template void read_M_vec2<double>(std::string name, unsigned int K, std::vector<std::vector<double>> &M);


void argsort_f(int *v, int n, int *ind){
	for (int i = 0; i < n; i++) ind[i] = i;
	std::sort(ind, ind + n, [&v](int i1, int i2){ return v[i1] < v[i2]; });
}

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
void write_vec(std::string name, std::vector<T> &y){
    std::fstream in_f;
	in_f.open(name.c_str(), std::ios::out | std::ios::binary);
//	in_f.write((char*)y, sizeof(T)*N);
	for(T &ele: y) in_f.write((char *)&ele, sizeof(T)) ;
	in_f.close();
}
template void write_vec<int>(std::string name, std::vector<int> &y);
template void write_vec<double>(std::string name, std::vector<double> &y);

void mode_f(int *v, int n, int *mode_ind, int *mode_count){
	*mode_count = 0;
	*mode_ind = -1;

	std::map<int, int> his;
	int ele;
	for (int i = 0; i < n; i++){
		ele = v[i];
		his[ele]++;
		if (his[ele] > *mode_count){
			*mode_ind = i;
			*mode_count = his[ele];
		}
	}
}

float clu_acc(int *y, int *y2, int N){

	int c2, S = 0, *tmp_y;

//	std::set<int> tmp(y, y+N);
//	c1 = tmp.size();

	std::set<int> tmp2(y2, y2+N);
	c2 = tmp2.size();

	//std::cout << "c1 = " << c1 << ", c2 = " << c2 << std::endl;

	int tmp_c;
	std::list<int> *ind = new std::list<int>[c2];
	for (int i = 0; i < N; i++){
		tmp_c = y2[i];
		if (tmp_c > c2){
			std::cout << "tmp_c = " << tmp_c << std::endl;
		}
		ind[tmp_c].push_back(i);
	}


	int ci, j, ci_ind, ci_count;
	for (int i = 0; i < c2; i++){

		ci = ind[i].size();

		tmp_y = new int[ci];
		j = 0;
		for (int ele : ind[i]){
			tmp_y[j] = y[ele];
			j++;
		}

		mode_f(tmp_y, ci, &ci_ind, &ci_count);

		S += ci_count;

		delete []tmp_y;
	}

	return S/(float)N;
}

void symmetry(std::vector<std::vector<int>> &NN, std::vector<std::vector<double>> &NND, double fill_ele){
    int N = NN.size();
    int K = NN[0].size();

    int id = 0;
    std::vector<int>::iterator it;
    for (int i = 0; i < N; i++){
        for (int j = 0; j < K; j++){
            id = NN[i][j];
            it = std::find(NN[id].begin(), NN[id].end(), i);
            if (it == NN[id].end()){
                NND[i][j] = fill_ele;
                NN[i][j] = -1;
            }
        }
    }
}

int exist_f(std::vector<int> &v, int x){
    int flag = -1;

    auto it = std::find(v.begin(), v.end(), x);
    if (it != v.end()) {
        flag = std::distance(v.begin(), it);
    }
    return flag;
}

