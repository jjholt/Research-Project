# Coordinates showing in abaqus
```Python
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
```
# Procedure
## 1.
Create your custom settings for the model. It's like you will want something along the lines of:
```Python
from Modelling import *
jobs = []

amplitudes = [1e-2, 5e-3, 1e-3, 2e-4]
for i, amplitude in enumerate(amplitudes):
    model_name = 'Model-%d'%i
    job_name = 'Job-%d_%d_um_impulse'%(i, amplitude*1e6)

    model = Model(model_name)

    model.amplitude = amplitude

    model.new()
    model.job(job_name, jobs)
```

The only attributes public in the `Model` class are things you'd want to change.

At the end you will have a global variable `jobs` with all job names.
## 2.
In Abaqus, use `Run Script` on the routine. This should generate all models and all jobs. You can manually run the jobs of choice or automate them using `run_jobs.py`, which does the following
```Python
for job in jobs:
    mdb.jobs[job].writeInput()
    mdb.jobs[job].submit(consistencyChecking=OFF)    
    mdb.jobs[job].waitForCompletion()
```
## 3.
Extract the data using `extract_data.py`. If the data will be processed and visualised using python, a lot of it is redundant, and you may benefit from something like:
```Python
from odbAccess import *
from odbMaterial import *
from odbSection import *
from abaqusConstants import *

import csv
import os
path = "./"
if not os.path.exists('csv'):
    os.makedirs('csv')

# Make sure to set up the variable of interest
vars_of_interest = ["U1", "U2", "U3"]



def column(matrix, i):
    return [row[i] for row in matrix]

# Requires your jobs to all be named in an array called jobs.
for job in jobs:
    my_odb_path=job + ".odb"
    odb=openOdb(my_odb_path)

    u_values = {}
    ordered_values = {}
    for i, node in enumerate(odb.steps['Step-1'].historyRegions.keys()):
        u_values[node] = []
        ordered_values[node] = []

        for j, var_of_interest in enumerate(vars_of_interest):
            history_region = odb.steps['Step-1'].historyRegions[node]
            history_output = history_region.historyOutputs[var_of_interest].data # Now all the data for time + var_of_interest is in this variable 
            
            u_values[node].append([var_of_interest]) # Create header
            for item in column(history_output,1): # Populate with values
                u_values[node][j].append(item)
    # Populate time
    t_values=column(history_output,0) 
    t_values.insert(0,"Time")
    
    # Re-order so they are separated by row, not column
    
    for node in u_values.keys():
        for n in range(len(u_values[node][0])):
            row = [t_values[n]]
            for i in range(len(u_values[node])):
                row.append(u_values[node][i][n])
            ordered_values[node].append(row)
    
        
        # Print data into an csv in the ./csv/ folder with a header.
        csv_name = job + "_" + node + ".csv"
        with open("csv/"+csv_name, "wb") as csv_name:
            csv.writer(csv_name).writerows(ordered_values[node])
```
