API for WHO

The purpose of this function is to get the data from the reports 2, 12 and 16 of the flumart repositories of the WHO.

The ode is divided in two parts :
    --> api_who.py : it is the executable part
    --> fct_who.py : it contains all the functions that will be called by the main

An example of exection is : python3 api_who.py --country Mexico --StartYear 2018 --StartWeek 1 --EndYear 2022 --EndWeek 53
(with of course the arguments you want)

It will create csv files of the 3 reports in the same folder as the code

THINGS TO UPGRADE :
    -> interesting to create an error handling for data that doesn't exist,
    for example we can't select Japan for the report 16 and it raises an error that dump the code

ALREADY EXISTS :
    -> there is a selenium version for the report 2 and 12 that is more adaptable than the actual version