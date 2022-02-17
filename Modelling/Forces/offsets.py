from Modelling import *
jobs = []
base_height = 0.045
offsets = range(1, int(base_height*1000), 5) #From 1 to 45 mm, this is converted to SI inside the loop.

############################### Main loop ###############################
i = 0
for i, force_offset_from_base in enumerate(offsets):
    model_name = 'Model-%d'%i
    job_name = 'Job-%d_offset-%d-mm'%(i,force_offset_from_base)
    jobs.append(job_name)

    force_offset_from_base = force_offset_from_base/1000.0
    model = Model(model_name)
    model.base_height = base_height # Just to guarantee it doesn't change anything if I change default values
    model.force_offset_from_base = force_offset_from_base

    model.new()
    model.job(job_name, jobs)
    