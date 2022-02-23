from odbAccess import *
from odbMaterial import *
from odbSection import *
from abaqusConstants import *

import csv

vars_of_interest = ["U1", "U2", "U3"]

for job in jobs:
    my_odb_path=job + ".odb"
    odb=openOdb(my_odb_path)

    for var_of_interest in vars_of_interest:
        for keys in odb.steps['Step-1'].historyRegions.keys():  
            history_region = odb.steps['Step-1'].historyRegions[keys]
            history_output = history_region.historyOutputs[var_of_interest].data # Now all the data for time + var_of_interest is in this variable 

            # Separate the data, each into their own column. If processing in python, just export the data from here.
            def column(matrix, i):
                return [row[i] for row in matrix]
                
            u_values=column(history_output,1)
            t_values=column(history_output,0) 

        
        #### Take u and t values for each row and order them. This is a requirement for csv.writerows to print each set as a new row.
            ordered_values = []
            for i in range(len(u_values)):
                ordered_values.append([t_values[i], u_values[i]])
        
        # Print data into an csv in the ./csv/ folder with a header.
        csv_name = job + "_" + var_of_interest + ".csv"
        with open("csv/"+csv_name, "wb") as csv_name:
            csv.writer(csv_name).writerow(["Time", var_of_interest]) # Header row
            csv.writer(csv_name).writerows(ordered_values)