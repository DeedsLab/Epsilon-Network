/*
   C++ code for calculating cell-cell distance matricies from scRNA-seq data
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

/* This is the class that holds our data */
/* We use a "sparse" represntation of the data, so that all the 0s in the expression matrix are not carried around in memory or used for the distance calculation */
class cell {
 public:
  string name ; // The "name" of the cell from the dataset
  vector <int> genes_expressed ; // A vector that contains the indices of all the genes that have non-zero expression values for this cell
  unordered_map <int, double> expression_values ; // A map from the index of the gene to the actual expression value of the data
} ;

void read_data(ifstream&,vector<cell>&); //Reads the data in

int main (int argc, char ** argv)
{
  if (argc != 5)
    {
      cout << "./gc.exe Input_data output_file imin imax" << endl ; // input the desired ring size, the number of monomers to start, and the outfile
      exit (1) ;
    }

  ifstream in_data ; // input stream for the data
  in_data.open(argv[1]);
  ofstream out_matrix ; // Output for the distance matrix
  out_matrix.open(argv[2]) ;
  int imin = atoi(argv[3]) ;
  int imax = atoi(argv[4]) ;

  vector<cell> cell_data ; //expression data for the cells

  read_data(in_data,cell_data) ;

  cout << "Number of cells in data set: " << cell_data.size()  << endl ;

  double distance = 0.0 ;
  int gene_index = 0 ;

  /* Below are error conditions on the parameters of imin and imax that would cause the code to either not run or not run correctly */
  if (imin >= cell_data.size()) {cout << "minimum value of i: " << imin << " is greater than the number of cells in the data set." << endl ; exit(1) ; }
  if (imax >= cell_data.size()) {cout << "maximum value of i: " << imax << " is greater than the number of cells in the data set." << endl ; exit(1) ; }

  if (imin < 0) {cout << "minimum value of i: " << imin << " is less than zero." << endl ; exit(1) ; }
  if (imax < 0) {cout << "maximum value of i: " << imax << " is less than zero." << endl ; exit(1) ; }

  if (imin >= imax) {cout << "minimum value of i: " << imin << " is greater than or equal to the maximum value of i: " << imax << endl ; exit(1) ;}
  
  for (int i = imin ; i < imax ; i++)
    {
      out_matrix << cell_data[i].name << "\t" << cell_data[i].name << "\t0.0" << endl ;
      for (int j = i+1 ; j < cell_data.size() ; j++)
	{
	  distance = 0.0 ;
	  unordered_map<int,int> done ; // tells us if a gene "g" has been seen yet

	  /* First we loop over the genes expressed in cell "i" */
	  for (int g = 0 ; g < cell_data[i].genes_expressed.size() ; g++)
	    {
	      gene_index = cell_data[i].genes_expressed[g] ;
	      
	      /* there are two scenarios. in one, the gene is expressed in only cell "i" and is not found in cell j's list of expressed genes*/
	      if (cell_data[j].expression_values.find(gene_index) == cell_data[j].expression_values.end())
		{
		  distance += cell_data[i].expression_values[gene_index]*cell_data[i].expression_values[gene_index] ;
		}
	      /* in the other scenario, it is expressed in both */
	      else
		{
		  distance += (cell_data[i].expression_values[gene_index] - cell_data[j].expression_values[gene_index])*(cell_data[i].expression_values[gene_index] - cell_data[j].expression_values[gene_index]) ;
		}
	      done[gene_index] = 1 ;
	    }

	  /* Now we go through the genes in cell "j", skipping the ones that have already been dealt with while going through the expressed genes for cell "i"*/
	  for (int g = 0 ; g < cell_data[j].genes_expressed.size() ; g++)
	    {
	      gene_index = cell_data[j].genes_expressed[g] ;
	      /* chec if we saw this gene already */
	      if (done.find(gene_index) == done.end())
		{
		  /* we did not see this gene yet. So we know it is not expressed in cell "i," so gene expression for "i" is 0. So we add this to the distance in the obvious way */
		  distance += cell_data[j].expression_values[gene_index]*cell_data[j].expression_values[gene_index] ;
		}
	    }
	  /* now we do the proper Euclidean thing by taking the square root of the distance */
	  distance = sqrt(distance) ;
	  out_matrix << cell_data[i].name << "\t" << cell_data[j].name << "\t" << distance << endl ;
	}
    }
}

void read_data (ifstream& in, vector<cell>& cell_data)
{
  string line_in, value ;
  int gene_counter ;
  double exp_val ;

  /* First we read in the header line. It is the first line of the file and is just ignored here */
  getline(in, line_in) ;

  while(getline(in, line_in))
    {
      cell new_cell ; // temporary cell to create with this data
      
      istringstream X(line_in) ; // stringstream for reading in the CSV values
      
      getline(X, value, ',') ; //reads the cell's name!

      new_cell.name = value ;

      getline(X, value, ',') ; //reads the cell type. In this version of the code, this data is ignored.
      
      gene_counter = 0 ; //count the genes you are reading in
      while(getline(X, value, ','))
	{
	  exp_val = stod(value) ;
	  if (exp_val > 0)
	    {
	      new_cell.genes_expressed.push_back(gene_counter) ;
	      new_cell.expression_values[gene_counter] = exp_val ;
	    }
	  gene_counter ++ ;
	}
      cell_data.push_back(new_cell) ;
    }
}
