# -*- coding: mbcs -*-
from lib2to3.pgen2.token import AMPER
from unicodedata import name
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

# Python-specific packages
import math

# Separate running jobs from building models
jobs = []
def get_jobs():
    return jobs

# Interfaces
class Curve:
    def __init__(self,name, amp, freq):
        self.name = name
        self.amp = amp
        self.freq = freq
############################### Setup ###############################

stem_height = 0.12
stem_radius = 0.006
stem_tip_radius = 0.005
collar_radius = 0.014
collar_height = 0.006
base_height = 0.045
base_radius = 0.009
stem_fillet = 0.0045
sensors = [
    'sensor_stem', 'sensor_collar',
]

force_offset = 0.001 #Offset from base for point where force will be applied. 0 < force_offset < base_height
mesh_size = 0.01

# Populate frequencies
frequencies = [1,10,20,30,40]
for f in range (50,901, 50):
    frequencies.append(f)


############################### Main loop ###############################
for i, frequency in enumerate(frequencies):
     # Change amplitude of sinewave here
    curve = Curve("Sinewave", 0.01, 2*math.pi*frequency)

    model_name = 'Model-%d'%i
    job_name = 'Job-%d_%d-Hz'%(i,frequency)
##################################################################################
############################### Define subroutines ###############################
##################################################################################
    def create_stem(name, height,radius,tip_radius):
        # Create stem
        mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=0.4)
        mdb.models[model_name].sketches['__profile__'].ConstructionLine(point1=(0.0, -0.2), point2=(0.0, 0.2)) # Construction line
        mdb.models[model_name].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.0, height))
        mdb.models[model_name].sketches['__profile__'].Line(point1=(0.0, height), point2=(tip_radius, height))
        mdb.models[model_name].sketches['__profile__'].Line(point1=(tip_radius, height), point2=(radius, 0.0))
        mdb.models[model_name].sketches['__profile__'].Line(point1=(radius, 0.0), point2=(0,0),)
        mdb.models[model_name].sketches['__profile__'].FilletByRadius(
            curve1= mdb.models[model_name].sketches['__profile__'].geometry[4],
            curve2= mdb.models[model_name].sketches['__profile__'].geometry[5],
            nearPoint1=( 0.00317779183387756, 0.119968019425869), nearPoint2=(0.00496279075741768, 0.116709597408772), radius=stem_fillet
        )
        mdb.models[model_name].Part(dimensionality=THREE_D, name=name, type=DEFORMABLE_BODY)
        mdb.models[model_name].parts["stem"].BaseSolidRevolve(angle=360.0, flipRevolveDirection=OFF, sketch=mdb.models[model_name].sketches['__profile__'])
        del mdb.models[model_name].sketches['__profile__']
        return name
    def create_cylinder(name, radius,height):
        # Create collar
        mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=0.1)
        mdb.models[model_name].sketches['__profile__'].sketchOptions.setValues(decimalPlaces=3)
        mdb.models[model_name].sketches['__profile__'].ConstructionLine(point1=(0.0,-0.05), point2=(0.0, 0.05))
        mdb.models[model_name].sketches['__profile__'].rectangle(point1=(0.0, 0.0), point2=(radius, height))
        mdb.models[model_name].Part(dimensionality=THREE_D, name=name, type= DEFORMABLE_BODY)
        mdb.models[model_name].parts[name].BaseSolidRevolve(
            angle=360.0, flipRevolveDirection=OFF, sketch=mdb.models[model_name].sketches['__profile__']
        )
        del mdb.models[model_name].sketches['__profile__']
        return name
    def quarter(name):
        mdb.models[model_name].parts[name].DatumPlaneByPrincipalPlane(offset=0.0, principalPlane=YZPLANE)
        mdb.models[model_name].parts[name].DatumPlaneByPrincipalPlane(offset=0.0, principalPlane=XYPLANE)
        mdb.models[model_name].parts[name].PartitionCellByDatumPlane(
            cells=mdb.models[model_name].parts[name].cells.getSequenceFromMask(('[#1 ]', ), ),
            datumPlane=mdb.models[model_name].parts[name].datums[2]
        )
        mdb.models[model_name].parts[name].PartitionCellByDatumPlane(
            cells=mdb.models[model_name].parts[name].cells.getSequenceFromMask(('[#3 ]', ),),
            datumPlane=mdb.models[model_name].parts[name].datums[3]
            )
    def horizontal_partition(name):
        mdb.models[model_name].parts[name].DatumPlaneByPrincipalPlane(offset=0.02, principalPlane=XZPLANE)
        mdb.models[model_name].parts[name].PartitionCellByDatumPlane(
            cells=mdb.models[model_name].parts[name].cells.getSequenceFromMask(('[#f ]', ), ),
            datumPlane=mdb.models[model_name].parts[name].datums[6]
        )
    def assign_material(name, range):
        mdb.models[model_name].parts[name].SectionAssignment(
            offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
            region=Region(cells=mdb.models[model_name].parts[name].cells.getSequenceFromMask(mask=(range, ), )),
            sectionName='Section-1', thicknessAssignment=FROM_SECTION
        )
    def mesh(name, size, region):
        mdb.models[model_name].parts[name].setMeshControls(
            algorithm=ADVANCING_FRONT, 
            elemShape=HEX_DOMINATED,
            regions=mdb.models[model_name].parts[name].cells.getSequenceFromMask((region, ),), technique=SWEEP
        )
        mdb.models[model_name].parts[name].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=size)
        mdb.models[model_name].parts[name].generateMesh()
    def output_requests(sensor):
        mdb.models[model_name].FieldOutputRequest(
            createStepName='Step-1', frequency=1, 
            name=sensor, rebar=EXCLUDE, region=mdb.models[model_name].rootAssembly.sets[sensor],
            sectionPoints=DEFAULT, variables=('U', )
        )
        mdb.models[model_name].HistoryOutputRequest(
            createStepName='Step-1', name=sensor, rebar=EXCLUDE,
            region= mdb.models[model_name].rootAssembly.sets[sensor],
            sectionPoints=DEFAULT, variables=('U1', 'U2', 'U3')
        )
    ############################### Create model ###############################
    mdb.Model(modelType=STANDARD_EXPLICIT, name=model_name)
    stem = create_stem("stem", stem_height, stem_radius, stem_tip_radius)
    quarter(stem)
    horizontal_partition(stem)
    collar = create_cylinder("collar", collar_radius,collar_height)
    quarter(collar)
    base = create_cylinder("base", base_radius,base_height)
    quarter(base)
    plane = mdb.models[model_name].parts[base].DatumPlaneByPrincipalPlane(
        offset=force_offset, principalPlane=XZPLANE
    )
    if force_offset > base_height or force_offset <= 0:
        print("Offset is outside of base bounds. Pick something between 0 and %d, non-inclusive" %base_height)
    else:
        mdb.models[model_name].parts[base].PartitionCellByDatumPlane(
            cells= mdb.models[model_name].parts[base].cells.getSequenceFromMask(('[#f ]', ), ),
            datumPlane=mdb.models[model_name].parts[base].datums[6]
        )

    ############################### Materials ###############################
    mdb.models[model_name].Material(name="Titanium")
    mdb.models[model_name].materials["Titanium"].Density(table=((4430, ), ))
    mdb.models[model_name].materials["Titanium"].Elastic(table=((114e9, 0.33), ))
    mdb.models[model_name].HomogeneousSolidSection(material="Titanium", name='Section-1', thickness=None)

    ############################### Assign material ###############################
    assign_material(collar, '[#f ]')
    assign_material(base,'[#ff ]')
    assign_material(stem, "[#ff ]")

    ############################### Assembly ###############################
    mdb.models[model_name].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models[model_name].rootAssembly.Instance(dependent=ON, name='base-1', part=mdb.models[model_name].parts[base])
    mdb.models[model_name].rootAssembly.Instance(dependent=ON, name='collar-1', part=mdb.models[model_name].parts[collar])
    mdb.models[model_name].rootAssembly.Instance(dependent=ON, name='stem-1', part=mdb.models[model_name].parts[stem])
    ############################### Move pieces to right places ###############################
    mdb.models[model_name].rootAssembly.translate(instanceList=('collar-1', ), vector=(0.0, base_height, 0.0))
    mdb.models[model_name].rootAssembly.translate(instanceList=('stem-1', ), vector=(0.0, base_height+collar_height, 0.0))


    ############################### Create ties between parts ###############################
    ### Name the surfaces
    mdb.models[model_name].rootAssembly.Surface(
        name='base_top', side1Faces= mdb.models[model_name].rootAssembly.instances['base-1'].faces.findAt(
            ((0.005898, base_height, 0.000776), ),
            ((-0.005898, base_height, 0.000776), ), 
            ((-0.005898, base_height, -0.000776), ), 
            ((0.005898, base_height, -0.000776), ), 
        )
    )
    mdb.models[model_name].rootAssembly.Surface(name='collar_bottom', side1Faces=mdb.models[model_name].rootAssembly.instances['collar-1'].faces.getSequenceFromMask(('[#8214 ]', ), ))
    mdb.models[model_name].rootAssembly.Surface(name='collar_top', side1Faces=mdb.models[model_name].rootAssembly.instances['collar-1'].faces.getSequenceFromMask(('[#3048 ]', ), ))
    mdb.models[model_name].rootAssembly.Surface(name='stem_bottom', side1Faces=mdb.models[model_name].rootAssembly.instances['stem-1'].faces.getSequenceFromMask(('[#80448000 ]', ), ))
    ### Tie the surfaces
    mdb.models[model_name].Tie(
        adjust=ON, main= mdb.models[model_name].rootAssembly.surfaces['stem_bottom'],
        name='stem-collar', positionToleranceMethod=COMPUTED, secondary=mdb.models[model_name].rootAssembly.surfaces['collar_top'],
        thickness=ON, tieRotations=ON
    )
    mdb.models[model_name].Tie(
        adjust=ON, main= mdb.models[model_name].rootAssembly.surfaces['base_top'],
        name='collar-base', positionToleranceMethod=COMPUTED, secondary= mdb.models[model_name].rootAssembly.surfaces['collar_bottom'],
        thickness=ON, tieRotations=ON
    )
    ############################### Mesh ###############################
    mesh(stem, mesh_size,"[#ff ]")
    mesh(collar, mesh_size,"[#f ]")
    mesh(base, mesh_size,"[#ff ]")

    ############################### Create points of interest ###############################
    mdb.models[model_name].rootAssembly.Set(
        name='vise_points',
        vertices= mdb.models[model_name].rootAssembly.instances['stem-1'].vertices.findAt(((0.005833, 0.071, 0.0), ), ((-0.005833, 0.071, 0.0), ), )
    )
    mdb.models[model_name].rootAssembly.Set(
        name='force_point',
        vertices= mdb.models[model_name].rootAssembly.instances['base-1'].vertices.findAt(((0.0, force_offset, base_radius), ))
    )
    mdb.models[model_name].rootAssembly.Set(
        name='sensor_collar',
        vertices=mdb.models[model_name].rootAssembly.instances['collar-1'].vertices.findAt(((0.0, base_height+collar_height, collar_radius), ))
    )
    mdb.models[model_name].rootAssembly.Set(
        name='sensor_stem',
        vertices= mdb.models[model_name].rootAssembly.instances['stem-1'].vertices.findAt(((0.0, 0.166537, 0.005037), ))
    )

    ############################### Boundary conditions ###############################
    mdb.models[model_name].EncastreBC(
        createStepName='Initial', localCsys=None, name='BC-1', region=mdb.models[model_name].rootAssembly.sets['vise_points']
    )
    ############################### Create step ###############################

    mdb.models[model_name].ImplicitDynamicsStep(
        initialInc=1e-05, minInc=1e-06, maxNumInc=10000, name='Step-1', previous='Initial', timePeriod=float(1.0/frequency)
    )
    ############################### Request outputs ###############################
    for sensor in sensors:
        output_requests(sensor)
    del mdb.models[model_name].historyOutputRequests['H-Output-1']
    ############################### Apply periodic force ###############################
    mdb.models[model_name].PeriodicAmplitude(
        a_0=0.0, data=((0.0, curve.amp), ), frequency=curve.freq, name=curve.name, start=0.0, timeSpan=STEP
    )
    mdb.models[model_name].ConcentratedForce(
        amplitude=curve.name,
        cf3=-1.0, createStepName='Step-1', distributionType=UNIFORM, field='', localCsys=None, name='Load-1',
        region= mdb.models[model_name].rootAssembly.sets['force_point']
    )
    
    ############################### Create job ###############################
    jobs.append(job_name)
    mdb.Job(
        atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
        memory=90, memoryUnits=PERCENTAGE, model=model_name, modelPrint=OFF, 
        multiprocessingMode=DEFAULT, name=job_name, nodalOutputPrecision=SINGLE, 
        numCpus=6, numDomains=6, numGPUs=0, numThreadsPerMpiProcess=1, queue=None, 
        resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=
        0, waitMinutes=0
    )