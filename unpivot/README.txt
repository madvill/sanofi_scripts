Unpivot function

The purpose of this script is to do a unpivot of the columns of a xlsx file or xlsx files that are in the same directory

The code is divided in two parts :
    --> main_unpivot.py : it is the executable part that we have to call to unpivot our files
    --> fct_unpivot.py : it contains the functions that will be called in the main

To permit the code to work, you need put your file(s) inside the folder wich has the name of the country
(Warning : for JP, there is two different versions --> intage is in JP, other file will be in JP2)

An example of execution will be :

python3 main_unpivot.py --dir PATH/"country ISO"/file.xlsx

The code will create a csv file in the same folder as the initial file with "_unpivoted" at the end of the name.