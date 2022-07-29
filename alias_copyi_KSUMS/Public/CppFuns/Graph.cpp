#include "Graph.h"

Graph::Graph(){}

Graph::Graph(int V){
    this->V = V;
    // adj = new list<int>[V];
    adj.resize(V);
    adj_R.resize(V);
    // adj_R = new list<int>[V];
    y = vector<int>(V, 0);
    num_clu = 0;
}

Graph::~Graph(){
    adj.clear();
    adj.shrink_to_fit();
    adj_R.clear();
    adj_R.shrink_to_fit();
    // delete[] adj;
}

// method to add an undirected edge
void Graph::addEdge(int v, int w){
    adj[v].push_back(w);
    adj[w].push_back(v);
}

void Graph::RList_f(){
	for (int i = 0; i < V; i++){
		for (auto &ele : adj[i]){
			adj_R[ele].push_back(i);
		}
	}
}

void Graph::connectedComponents(){
	RList_f();

    fill(y.begin(), y.end(), -1);

    vector<int> tmpL;
	// std::list<int> tmpL;
	int id = 0;
	num_clu = 0;
	for (int i = 0; i < V; i++) if (y[i] == -1){

		tmpL.push_back(i);
		y[i] = num_clu;

		while (tmpL.size() > 0){
			id = tmpL.back();
			tmpL.pop_back();


			for (auto &ele : adj[id]) if (y[ele] == -1){
                tmpL.push_back(ele);
				y[ele] = num_clu;
			}

			for (auto &ele : adj_R[id])	if (y[ele] == -1) {
                tmpL.push_back(ele);
				y[ele] = num_clu;
			}
		}

		num_clu ++;
	}
}
