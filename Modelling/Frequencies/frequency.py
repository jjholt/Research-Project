from Modelling import *
import math
# from Modelling.Modelling import (Force, Model, Curve)

frequencies = [1, 10, 20, 30, 40]
for i in range(50,901, 50):
    frequencies.append(i)

jobs = []
for i, frequency in enumerate(frequencies):
    model_name = 'Model-%d'%(i)
    prefix = "0" if i < 10 else ""
    job_name = 'Job-' + prefix + '%d_%d-Hz' %(i, frequency)
    
    frequency = frequency*2*math.pi
    model = Model(model_name) # Create new model
    # Set the variables we're changing in this run
    model.curves[0].frequency = frequency # Seems like sometimes there's a bug that makes this be not correctly multiply inside the Model class.
    print("Angular frequency", model.frequency)
    # Generate the model
    model.new()
    # Generate the jobs. Jobs are not run at this step!

    model.job(job_name, jobs)