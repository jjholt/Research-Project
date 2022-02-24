from Modelling import *
from itertools import combinations
# from Modelling.Modelling import *
jobs = []

pairs = [
    (1.0, 0.0, 0,0),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, -1.0)
]
force_directions = list(combinations(pairs,2))


for i, force_direction in enumerate(force_directions):
    curves = [
        Curve(200e-6, 0, "Cos", 2*math.pi*100),
        Curve(0, 200e-6, "Sin", 2*math.pi*100),
    ]
    forces = [
        Force(curves[0].name, 0.001, force_direction[0]),
        Force(curves[1].name, 0.001, force_direction[1])
    ]
    model_name = 'Model-%d'%i
    job_name = 'Job-%d'%i


    model = Model(model_name)
    model.forces = forces
    model.curves = curves

    model.new()
    model.job(job_name, jobs)