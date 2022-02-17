from Modelling import *

frequencies = [1, 10, 20, 30, 40]
for i in range(50,901, 50):
    frequencies.append(i)


for frequency in enumerate(frequencies):
    model_name = 'Model-%d'%(i)
    job_name = 'Job-%d_%d-Hz' %(i, frequency)

    model = Model(model_name) # Create new model
    
    # Set the variables we're changing in this run
    model.frequency = frequency

    # Generate the model
    model.new()

    # Generate the jobs. Jobs are not run at this step!
    model.job(job_name, jobs)