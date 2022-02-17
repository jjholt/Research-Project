from Modelling import *

for job in jobs:
    mdb.jobs[job].writeInput()
    mdb.jobs[job].submit(consistencyChecking=OFF)    
    mdb.jobs[job].waitForCompletion()