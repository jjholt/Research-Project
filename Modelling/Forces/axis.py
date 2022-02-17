from Modelling import *
jobs = []
force_directions = []
for x in range (-1, 2, 1):
    for y in range (-1, 2, 1):
        for z in range (-1, 2, 1):
            if x == 0 and y == 0 and z == 0:
                continue
            else:
                force_directions.append((x,y,z))


for i, force_direction in enumerate(force_directions):
    model_name = 'Model-%d'%i
    j1 = 'Job-%d_axes_%d_%d_%d'%(i,force_direction[0],force_direction[1],force_direction[2])
    j2 = 'Job-0%d_axes_%d_%d_%d'%(i,force_direction[0],force_direction[1],force_direction[2])
    job_name = j1 if i > 10 else j2


    model = Model(model_name)
    model.force_direction = force_direction
    
    model.new()
    model.job(job_name, jobs)