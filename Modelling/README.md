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

vars_of_interest = ["U1", "U2", "U3"]

for job in jobs:
    my_odb_path=job + ".odb"
    odb=openOdb(my_odb_path)

    for var_of_interest in vars_of_interest:
        for keys in odb.steps['Step-1'].historyRegions.keys():  
            history_region = odb.steps['Step-1'].historyRegions[keys]
            history_output = history_region.historyOutputs[var_of_interest].data
            # Now all the data for time + var_of_interest is in history_output 

            # Separate the data, each into their own column. If processing in python, just export the data from here.
            def column(matrix, i):
                return [row[i] for row in matrix]
                
            u_values=column(history_output,1)
            t_values=column(history_output,0) 
```
