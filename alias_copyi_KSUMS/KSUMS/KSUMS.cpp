#include "KSUMS.h"

KSUMS::KSUMS(){}

KSUMS::KSUMS(std::vector<std::vector<int>> &NN, std::vector<std::vector<double>> &NND, double max_d, int c_true){
    this->N = NN.size();
    this->c_true = c_true;

    this->NN = NN;
    this->NND = NND;
    this->max_d = max_d;

    //check NN
    for (int i = 0; i < N; i++){
        if (NN[i][0] != i){
            std::cout << "Error opening file" << std::endl;
            exit(EXIT_FAILURE);
        }
    }

    hi = new double[c_true];
    hi_count = new int[c_true];

    // initialize
    srand((unsigned)time(NULL));
    y.assign(N, 0);
    std::generate(y.begin(), y.end(), [c_true]() {return rand() % c_true;});

    KO = Keep_order(y, N, c_true);
}

KSUMS::~KSUMS() {}

void KSUMS::opt(){

    clock_t t_start = clock();

    int end_count = 0;
    int iter = 0, c_old = 0, c_new = 0;

    double h_min_val = 0;
    int h_min_ind = 0;

    int tmp_c = 0, tmp_nb = 0;

    for (iter = 0; iter < 100; iter++){
        end_count = 0;
        for (int sam_i = 0; sam_i < N; sam_i++){
            c_old = y[sam_i];

            // knn_c
            knn_c.clear();
            for (auto nb: NN[sam_i]){
                knn_c.insert(y[nb]);
            }

            construct_hi(sam_i);

            // find minimun in knn
            h_min_ind = *knn_c.begin();
            h_min_val = hi[h_min_ind];
            for (auto tmp_c: knn_c) if (hi[tmp_c] < h_min_val){
                h_min_ind = tmp_c;
                h_min_val = hi[h_min_ind];
            }

            if (KO.o2ni[0] * max_d < h_min_val){
                c_new = KO.o2c[0];
            }else{
                c_new = h_min_ind;
            }

            if (c_new == c_old){
                end_count +=1;
            }else{
                y[sam_i] = c_new;
                KO.sub(KO.c2o[c_old]);
                KO.add(KO.c2o[c_new]);
            }
        }
        if (end_count >= N){
            break;
        }
    }
    clock_t t_end = clock();
    _time = (t_end-t_start)/CLOCKS_PER_SEC;
    num_iter = iter;
}


void KSUMS::construct_hi(int sam_i){


    for (auto tmp_c: knn_c){
        hi[tmp_c] = 0;
        hi_count[tmp_c] = 0;
    }

    int nb, tmp_c;
    for (int k = 0; k < NN[sam_i].size(); k++){
        nb = NN[sam_i][k];
        tmp_c = y[nb];
        hi[tmp_c] += NND[sam_i][k];
        hi_count[tmp_c] += 1;
    }

    int tmp_ni;
    for (auto tmp_c: knn_c){
        tmp_ni = KO.o2ni[KO.c2o[tmp_c]];
        hi[tmp_c] += (tmp_ni - hi_count[tmp_c]) * max_d;
    }

}
