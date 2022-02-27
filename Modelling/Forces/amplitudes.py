from Modelling import *
jobs =[]

amplitudes = [1e-2, 5e-3, 1e-3, 2e-4]
for i, amplitude in enumerate(amplitudes):
    curves = [Curve(amplitude, 0, "Cos", 100*2*math.pi)]
    model_name = 'Model-%d'%i
    job_name = 'Job-%d_%d_um_impulse'%(i, amplitude*1e6)

    model = Model(model_name)
    model.curves = curves

    model.new()
    model.job(job_name, jobs)