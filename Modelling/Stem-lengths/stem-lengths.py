from Modelling import *
import math
# from Modelling.Modelling import (Force, Model, Curve)

stem_heights = [8e-2, 12e-2, 16e-2]

jobs = []
for i, stem_height in enumerate(stem_heights):
    model_name = 'Model-%d'%(i)
    prefix = "0" if i < 10 else ""
    job_name = 'Job-' + prefix + '%d_%d-cm' %(i, stem_height*100.0)
    
    model = Model(model_name) # Create new model

    model.stem_height = stem_height
    
    # Generate the model
    model.new()
    # Generate the jobs. Jobs are not run at this step!

    model.job(job_name, jobs)