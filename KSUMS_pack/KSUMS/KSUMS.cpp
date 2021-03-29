#include "KSUMS.h"

KSUMS::KSUMS(){}

KSUMS::KSUMS(std::vector<std::vector<int>> &NN, std::vector<std::vector<double>> &NND, int c_true){
    this->N = NN.size();
    this->knn = NN[0].size();
    this->c_true = c_true;
    this->NN = NN;
    this->NND = NND;

    //check NND
    for (int i = 0; i < N; i++){
        if (NN[i][0] != i){
            std::cout << "Error opening file" << std::endl;
            exit(EXIT_FAILURE);
        }
    }

    // allocate memory
    y.assign(N, 0);

    hi = new double[c_true];
    hi_TF = new int[c_true];
    hi_count = new int[c_true];
    knn_c = new int[knn];

    // initialize
    srand((unsigned)time(NULL));
    std::generate(y.begin(), y.end(), [c_true]() {return rand() % c_true;});

    KO = Keep_order(y, N, c_true);

    max_d = cf::maximum_2Dvec(NND);

    cf::symmetry(this->NN, this->NND, 0, max_d);
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
            for (int k = 0; k < knn; k++){
                tmp_nb = NN[sam_i][k];
                knn_c[k] = y[tmp_nb];
            }

            construct_hi(sam_i);

            // find minimun in knn
            h_min_ind = knn_c[0];
            h_min_val = hi[h_min_ind];
            for (int k = 1; k < knn; k++){
                tmp_c = knn_c[k];
                if (hi[tmp_c] < h_min_val){
                    h_min_ind = tmp_c;
                    h_min_val = hi[h_min_ind];
                }
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

    int tmp_c, tmp_ni;

    for (int k = 0; k < knn; k++){
        tmp_c = knn_c[k];
        hi[tmp_c] = 0;
        hi_count[tmp_c] = 0;
        hi_TF[tmp_c] = 0;
    }

    for (int k = 0; k < knn; k++){
        tmp_c = knn_c[k];
        hi[tmp_c] += NND[sam_i][k];
        hi_count[tmp_c] += 1;
    }

    for (int j = 0; j < knn; j++){
        tmp_c = knn_c[j];
        if (hi_TF[tmp_c] == 0){
            hi_TF[tmp_c] = 1;

            tmp_ni = KO.o2ni[KO.c2o[tmp_c]];
            hi[tmp_c] += (tmp_ni - hi_count[tmp_c]) * max_d;
        }
    }

}
