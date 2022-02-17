from Modelling import *

mesh_sizes = [0.01, 0.005, 0.0025, 0.00125]
############################### Main loop ###############################
for i, mesh_size in enumerate(mesh_sizes):
    model_name = 'Model-%d'%i
    job_name = 'Job-%d_mesh-%d-mm'%(i,mesh_size*1000.0)

    model = Model(model_name)
    model.mesh_size = mesh_size
    model.new()
    model.job(job_name, jobs)