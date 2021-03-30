#ifndef _GRAPH_H
#define _GRAPH_H
// C++ program to print connected components in
// an undirected graph
#include<iostream>
#include <list>
#include <vector>

using namespace std;

// Graph class represents a undirected graph
// using adjacency list representation
class Graph {
public:
    int V;
    vector<vector<int>> adj;
    vector<vector<int>> adj_R;
    vector<int> y;
    int num_clu;
    Graph();
    Graph(int V);   // Constructor
    ~Graph();
    void addEdge(int v, int w);
    void RList_f();
    void connectedComponents();

};

#endif // _GRAPH_H
