from Modelling import *
jobs = []

max_height = 0.040
offsets = range(1, int(max_height*1000), 2) #From 1 to 35 mm, this is converted to SI inside the loop.

############################### Main loop ###############################
for i, offset_from_spigot in enumerate(offsets):
    model_name = 'Model-%d'%i
    prefix = "0" if i < 10 else ""

    job_name = "Job-" + prefix + "%d_offset-%d-mm"%(i,offset_from_spigot)

    offset_from_spigot = offset_from_spigot/1000.0
    model = Model(model_name)
    model.forces[0].offset_from_spigot = offset_from_spigot
    
    model.new()
    model.job(job_name, jobs)
    