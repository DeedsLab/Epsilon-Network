# Internal_Waddington
Internal Scripts for creation of figures for Waddington Paper

This Readme is in progress. It will contain comments on how to use code for Waddington Pipeline

Current_Version of the Pipeline will be as follows

1) Generate Distance Matrixes
   Both python and c++ versions of the code will be uploaded but the format should result in a .txt file with the appending of Dist_Form.txt,
   Each file will have 3 columns but with no header. First Column represents out edges Second column represents in-edges. As distances matrixes, mirrored duplicates are expected. Dataset_Name as well as step along scRNA-seq should be noted

   CellXGene matrix used as input should have the first column as cell_type or any other metadata for each cell

2) Calculate Degree Distributions
  Two versions
  -purity_Epsilon_Gen_degree: takes in only Dist_Form.txt, output a csv named Neighborhoods in a folder that has run details in a super folder named Epsilon_Degree_Only
  -

3) Plot Degree Distribution
    -Two versions
    -plots degree_dist_: Takes in Neighborhoods.csv in a folder named after run details in Epsilon_Degree_Only, plots degree distribution. Takes in number of bins to logbinns 


This Readme will be updated in the future as well.
