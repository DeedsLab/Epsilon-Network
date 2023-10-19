/*
   C++ code for finding giant components for epsilon graphs from distance matricies
*/

#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <string>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <algorithm>
#include <unordered_map>

using namespace std ;

void read_distance_matrix(ifstream&,vector<string>&,unordered_map<string, int>&,vector< vector <double> >&, vector <vector <int> >&,double) ; // function to read in the data
void calculate_eps_graph (vector<vector <int> >&, vector<vector <double> >&, vector<vector <int> >&, double) ; //function to calculate the epsilon graph

void run_dfs_from_i (vector<vector <int> >&, int, vector<int>&, vector<string>&, vector<string>&) ; //function to call the dfs from a node i and calculate its connected component
void dfs (vector<vector <int> >&, int, vector<int>&, vector<string>&, vector<string>&) ;

int main (int argc, char ** argv)
{
  if (argc != 6)
    {
      cout << "./gc.exe Input_data eps_min eps_max eps_step output_GC_size_v_epsilon" << endl ; // input the desired ring size, the number of monomers to start, and the outfile
      exit (1) ;
    }

  ifstream in_distances ; // input stream for the data
  in_distances.open(argv[1]);
  double eps_min = atof(argv[2]) ; // minimum epsilon for making the graph
  double eps_max = atof(argv[3]) ; // max epsilon for making the graph
  double eps_step = atof(argv[4]) ; // step size in epsilon
  ofstream out_GC_v_eps ; // Output for GC_size vs. epsilon
  out_GC_v_eps.open(argv[5]) ;

  vector <string> cell_names ; // vector that holds the names of the cells
  unordered_map <string, int> name_to_index_map ; // maps the cell's name to its index in cell_names vector

  vector <vector <double> > distance_matrix ; // data structure that holds the distance matrix
  vector <vector <int> > index_matrix ; //data structure that holds the corresponding indices of our friendly nodes

  /* First, read in the distance matrix */
  read_distance_matrix(in_distances, cell_names, name_to_index_map, distance_matrix, index_matrix, eps_max) ;

  double eps = eps_min ;
  while (eps <= eps_max)
    {
        vector <vector<int > > adjacency_list ; //adjacency list for this value of epsilon
	vector <int> M ; //"marker" for the DFS
	vector <vector<string> > comps ; // Components in the graph!
	int gc_this_rep_size = 0 ;
	int gc_this_rep_index = -1 ;
	
	//Initialize relevant data structures
	for (int i = 0 ; i < cell_names.size() ; i++)
	  {
	    vector<int> tmp ;
	    adjacency_list.push_back(tmp) ;
	    M.push_back(0) ; // Initialize the M vector to all 0's!
	  }
      
      calculate_eps_graph(adjacency_list, distance_matrix, index_matrix, eps) ;

      for (int i = 0 ; i < cell_names.size() ; i++)
	{
	  if (!M[i])
	    {
	      vector <string> tmp_comp ; 
	      run_dfs_from_i(adjacency_list, i, M, tmp_comp, cell_names) ;
	      comps.push_back(tmp_comp) ;
	    }
	}
      
      for (int i = 0 ; i < comps.size() ; i++ )
	{
	  if(comps[i].size() > gc_this_rep_size)
	    {
	      gc_this_rep_size = comps[i].size() ;
	      gc_this_rep_index = i ;
	    }
	}

      out_GC_v_eps << eps << "\t" << gc_this_rep_size << endl ;
      eps += eps_step ;
    }
}

void read_distance_matrix(ifstream& in, vector<string>& cell_names, unordered_map<string,int>& name_to_index_map, vector<vector<double> >& distance_matrix, vector<vector<int> >& index_matrix,double eps_max)
{
  string name1 ;
  string name2 ;
  double distance ;
  int current_cell_index = 0 ;

  while (!in.eof())
    {
      in >> name1 >> name2 >> distance ;
      if (in.eof()){break;}
      // first we make sure we've added the two cells in question to our list of cell names
      if(name_to_index_map.find(name1) == name_to_index_map.end())
	{
	  // First we add our new cell to our list of names
	  cell_names.push_back(name1) ;
	  // Then we add it to our map from names to indices
	  name_to_index_map[name1] = current_cell_index;
	  // Now we generate a placeholder so we can add distances for this cell into our distance matrix
	  vector<double> temp1 ;
	  distance_matrix.push_back(temp1) ;
	  // Now we do the same thing for the index_matrix
	  vector<int> temp2 ;
	  index_matrix.push_back(temp2) ;
	  // Update the cell index so we can make the maps properly
	  current_cell_index ++ ;
	}
      if(name_to_index_map.find(name2) == name_to_index_map.end())
	{
	  // See above for the logic of these steps
	  cell_names.push_back(name2) ;
	  name_to_index_map[name2] = current_cell_index;
	  vector<double> temp1 ;
	  distance_matrix.push_back(temp1) ;
	  vector<int> temp2 ;
	  index_matrix.push_back(temp2) ;
	  current_cell_index ++ ;
	}

      if ((name1 != name2)&&(distance <= eps_max)) // Avoid the trivial case of self-distances being 0. Also, no need to put data into the list if it is bigger than eps_max
	{
	  // now we add the distance to our internal distance matrix
	  distance_matrix[name_to_index_map[name1]].push_back(distance) ;
	  distance_matrix[name_to_index_map[name2]].push_back(distance) ;

	  // Now we do the same thing for the indices for our adjacency matrix
	  index_matrix[name_to_index_map[name1]].push_back(name_to_index_map[name2]) ;
	  index_matrix[name_to_index_map[name2]].push_back(name_to_index_map[name1]) ;
	}
    }
}

void calculate_eps_graph (vector<vector<int> >& adjacency_list, vector<vector<double> >& distance_matrix , vector<vector< int> >& index_matrix, double c)
{
  for (int i = 0 ;  i < distance_matrix.size() ; i++)
    {
      for (int j = 0 ; j < distance_matrix[i].size() ; j++)
	{
	  if (distance_matrix[i][j] < c)
	    {
	      adjacency_list[i].push_back(index_matrix[i][j]) ;
	    }
	}
    }
}

void run_dfs_from_i(vector<vector<int> >& adjacency_list, int i, vector<int>& M, vector<string>& comp, vector<string>& cell_names)
{
  M[i] = 1;
  comp.push_back(cell_names[i]) ;
  for (int j = 0 ; j < adjacency_list[i].size() ; j++)
    {
      int index_j = adjacency_list[i][j] ; //this is the index of the "jth" contact of our node "i"
      if (!M[index_j])
	{
	  dfs(adjacency_list,index_j,M,comp,cell_names) ;
	}
    }
}

void dfs(vector<vector<int> >& adjacency_list, int i, vector<int>& M, vector<string>& comp, vector<string>& cell_names)
{
  M[i] = 1 ;
  comp.push_back(cell_names[i]) ;
   for (int j = 0 ; j < adjacency_list[i].size() ; j++)
    {
      int index_j = adjacency_list[i][j] ; //this is the index of the "jth" contact of our node "i"
      if (!M[index_j])
	{
	  dfs(adjacency_list,index_j,M,comp,cell_names) ;
	}
    }
}
