#include <iostream>
#include <fstream>
#include <string>
#include <cstring>  
#include <sstream>

#include <stdio.h>
#include <string.h>
#include <vector>
#include <algorithm>
#include <cmath>


using namespace std;

bool taketranspose = false;
float norm = 2;
vector<vector<int> > final_vector; //vector that holds vectors or transpose of vector
string demarker = ",";
const char *demarchar = demarker.c_str();
string parsingfile;
string outputfile;

int main(){
   
   cout << "\nWhich file would you like to run?\n";
   cin >> parsingfile;
   outputfile = parsingfile.substr(0,parsingfile.length()-4)+"_norm_"+to_string(norm)+".csv"; 
   cout << "The output File will be named: "<< outputfile << "\n";
   

   fstream newfile;
   
   newfile.open(parsingfile,ios::in); //open a file to perform read operation using file object
   if (newfile.is_open()){   //checking whether the file is open
      vector<vector<int> > cell_count_holding_vector; //vector that holds vectors	
      string tp;
      bool firstlinepassed = false;
      while(getline(newfile, tp)){ //read data from file object and put it into string.
	 
	// if you remove this conditional, the whole thing breaks lol. It skips the first line of the csv.
         if (!firstlinepassed){ 
		firstlinepassed = true;
		continue;}

	 char* token; // creates pointer variable used in string remarking function
	 char *dup = strdup(tp.c_str()); // duplicates each line of csv than can be split by a comma
	
	vector<int> vect;
	while ((token = strtok_r(dup, demarchar, &dup))) //iterates through comma separated values on each line
		{
		string totem = token; //removes spaces from string to get consistent results
		remove(totem.begin(), totem.end(), ' ');
		try {
		vect.push_back(stoi(totem)); //attempts to turn string to int to store in vector
		} 
		catch(invalid_argument) {}
		}
         cell_count_holding_vector.push_back(vect); //adds vector of containing comma separated values to other vectors
      }
      newfile.close(); //close the file object.

	cout <<  "The current dimensions of this matrix are: "<<cell_count_holding_vector.size() << "x" << cell_count_holding_vector[0].size() << ", (with this interpretation, There are " << cell_count_holding_vector.size() << " cells and " << cell_count_holding_vector[0].size() << " genes.) \n"; //pnt csv dims
	string transpose_tracker;


	cout << "Would you like to take the transpose of this matrix, converting this to a matrix of " << cell_count_holding_vector[0].size() << " cells and " << cell_count_holding_vector.size() << " genes? (Respond Y/N)\n\n" ;

	cin >> transpose_tracker;
	
	if (transpose_tracker == "Y" || transpose_tracker == "y"){taketranspose = true;}
	

	final_vector = cell_count_holding_vector;

	if (taketranspose){ //if transpose option is taken, take transpose of and store in final_vector
		
		long double distmat[final_vector.size()][final_vector.size()];
		std::ofstream out(outputfile);
		for (int caprow = 0; caprow < final_vector[0].size() ;caprow++){
			distmat[caprow][caprow] = 0;
			for (int botrow = 0; botrow < final_vector[0].size() ;botrow++){
				long double aggregate_dist = 0;
				if (botrow < caprow){//cout << "less";
					for (int vector_looper = 0; vector_looper < final_vector.size(); vector_looper++){
						double diff = abs(final_vector[vector_looper][botrow] - final_vector[vector_looper][caprow]) ;
						aggregate_dist = aggregate_dist + pow(diff,norm);
					}
				aggregate_dist = powl(aggregate_dist, 1/norm);
				}
				out << aggregate_dist << ",";
				}
			out << "\n";
			}
		out.close();
	} else {
		//cout << "test\n";
		//long double distmat[final_vector.size()][final_vector.size()];
		std::ofstream out(outputfile);
		out << "first line test\n";
		for (int caprow = 0; caprow < final_vector.size() ;caprow++){
			//distmat[caprow][caprow] = 0;
			for (int botrow = 0; botrow < final_vector.size() ;botrow++){
				long double aggregate_dist = 0;
				if (true){
					for (int vector_looper = 0; vector_looper < final_vector[botrow].size(); vector_looper++){
						double diff = abs(final_vector[botrow][vector_looper] - final_vector[caprow][vector_looper]) ;
						aggregate_dist = aggregate_dist + pow(diff,norm);
					}
				aggregate_dist = powl(aggregate_dist, 1/norm);
				}
				out << aggregate_dist << ",";
				}
			out << "\n";
			if (caprow % 100 == 0){
				cout << float(caprow)/float(final_vector.size()) * 100 << " percent completed \n";
				}
			}
		out.close();

	}
	
   }
	


}