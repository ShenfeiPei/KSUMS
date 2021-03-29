#include "Keep_order.h"
Keep_order::Keep_order() {}

Keep_order::Keep_order(std::vector<int> &y, int N, int c){
    this->N = N;
    this->c = c;
    // new
    o2ni = vector<int>(c);
    o2c = vector<int>(c);
    c2o = vector<int>(c);

    // o2ni = new int[c];
    // o2c = new int[c];
    // c2o  = new int[c];
    ni2o = new lr_ind[N];

    // initialize

    // (1) o2ni and o2c
    // o2ni = 5, 4, 2, 9, 1
    // o2c  = 0, 1, 2, 3, 4
    // order: N, N, N, N, N
    std::fill(o2ni.begin(), o2ni.end(), 0);
    // std::fill(o2ni, o2ni + c, 0);
    for (int i = 0; i < N; i++){
        o2ni[y[i]] += 1;
    }

    // o2ni = 1, 2, 4, 5, 9
    // o2c  = 4, 2, 1, 0, 3
    // order: 0, 1, 2, 3, 4
    cf::argsort_f(o2ni, o2c);
    std::sort(o2ni.begin(), o2ni.end());

    // (2) c2o
    // c2o = 3, 2, 1, 4, 0
    // c   = 0, 1, 2, 3, 4
    for (int i = 0; i < c; i++){
        c2o[o2c[i]] = i;
    }

    // (3) ni2o
    for (int i = 0; i < N; i++){
        ni2o[i].l = -1;
        ni2o[i].r = -1;
    }

    int ni = 0;
    for (int i = 0; i < c; i++){
        // Left
        ni = o2ni[i];
        if (ni2o[ni].l == -1){
            ni2o[ni].l = i;
        }

        // right
        if (i==c-1){
            ni2o[ni].r = i;
        }else if (ni != o2ni[i+1]) {
            ni2o[ni].r = i;
        }
    }
}

Keep_order::~Keep_order() {}

// id denotes rank, order, index
void Keep_order::sub(int id){
    int old_l = 0, ni = 0;
    ni = o2ni[id];

    // 6,    8,    8 8 8   8, 9
    //      old_l, ..., old_r  (ni = 8)
    old_l = ni2o[ni].l;

    ni2o[ni].l ++;
    if (ni2o[ni].l > ni2o[ni].r){
        ni2o[ni].l = -1;
        ni2o[ni].r = -1;
    }

    ni2o[ni-1].r = old_l;
    if (ni2o[ni-1].l == -1){
        ni2o[ni-1].l = ni2o[ni-1].r;
    }

    // o2ni, maintain order
    o2ni[old_l] --;

    std::swap(o2c[id], o2c[old_l]);

    c2o[o2c[old_l]] = old_l;
    c2o[o2c[id]] = id;
}

// id denotes rank, order, index
void Keep_order::add(int id){
    int old_r = 0, ni = 0;
    ni = o2ni[id];

    // 6,    8,    8 8 8   8, 9
    //      old_l, ..., old_r  (ni = 8)
    old_r = ni2o[ni].r;

    ni2o[ni].r --;
    if (ni2o[ni].r < ni2o[ni].l){
        ni2o[ni].l = -1;
        ni2o[ni].r = -1;
    }

    ni2o[ni+1].l = old_r;
    if (ni2o[ni+1].r == -1){
        ni2o[ni+1].r = ni2o[ni+1].l;
    }

    // o2ni, maintain order
    o2ni[old_r] ++;

    std::swap(o2c[id], o2c[old_r]);

    c2o[o2c[old_r]] = old_r;
    c2o[o2c[id]] = id;
}
