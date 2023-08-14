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


float norm = 2;
//vector<vector<int> > final_vector; //vector that holds vectors or transpose of vector
string demarker = ",";
const char *demarchar = demarker.c_str();
string parsingfile;
string outputfile;

int cap = 50;
float step = 0.1;

int main(){
   
   cout << "\nWhich file would you like to run?\n";
   cin >> parsingfile;
   outputfile = parsingfile.substr(0,parsingfile.length()-4)+"_epsilon_.csv"; 
   cout << outputfile << "\n";
   

   fstream newfile;
   
   newfile.open(parsingfile,ios::in); //open a file to perform read operation using file object
   if (newfile.is_open()){   //checking whether the file is open
      vector<vector<int> > cell_count_holding_vector; //vector that holds vectors	
      string tp;
      bool firstlinepassed = false;
      ofstream out(outputfile);
      //out << "step size:" << step << "\nthe first element in each row is the degree with epsilon 0, the second element is degree with epsilon " << step <<" etc.\n";
	{
	float a = 0;
	while ( a < cap){
		out << a <<",";
		a = a + step;
		}
	out << "\n";
	}

      cout << "step size:" << step << "\nthe first element in each row is the degree with epsilon 0, the second element is degree with epsilon " << step <<" etc.\n";
      int line_counter = 0;
      while(getline(newfile, tp)){ //read data from file object and put it into string.
	 
	// if you remove this conditional, the whole thing breaks lol. It skips the first line of the csv.
        if (!firstlinepassed){ 
		firstlinepassed = true;
		continue;}

	char* token; // creates pointer variable used in string remarking function
	char *dup = strdup(tp.c_str()); // duplicates each line of csv than can be split by a comma
	
	
	vector<float> parser;
	while ((token = strtok_r(dup, demarchar, &dup))) //iterates through comma separated values on each line
		{
		string totem = token; //removes spaces from string to get consistent results
		remove(totem.begin(), totem.end(), ' ');
		try {
			//cout << stof(totem) << "\n";
			parser.push_back(stof(totem));
			} 
		catch(invalid_argument) {
			}
		
		}
	{
	sort(parser.begin(), parser.end());
	//cout << parser[0] << "\t" << parser[1] << "\t" << parser[5246] << "\t" << parser.size() << "\n";


	int step_counter = 0;
	for (int n = 0; n < parser.size(); n++){
		while (step_counter * step < parser[n]){
			//cout << n-1 << ",";
			out << n-1 << ",";
			step_counter = step_counter + 1;
			}
		}
	//string transpose_tracker;
	//cin >> transpose_tracker;
	out << "\n";
	line_counter = line_counter + 1;
	if (line_counter % 100 == 0){cout << line_counter << " lines completed\n";}
	}
      }
      out.close();
      newfile.close(); //close the file object.


	
   }
	

}