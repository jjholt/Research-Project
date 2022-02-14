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

# Interfaces
class Curve:
    def __init__(self,name, amp, freq):
        self.name = name
        self.amp = amp
        self.freq = freq
############################### Setup ###############################
i=1

stem_height = 0.12
stem_radius = 0.006
stem_tip_radius = 0.005
collar_radius = 0.014
collar_height = 0.006
base_height = 0.045
base_radius = 0.009
stem_fillet = 0.0045
    
curves = [ # list[Curve]
    Curve("Sinewave", 0.01, 2*math.pi)
]
sensors = [
    'sensor_stem', 'sensor_collar',
]

##################################################################################
############################### Define subroutines ###############################
##################################################################################
def stem(name, height,radius,tip_radius):
    # Create stem
    mdb.models['Model-%d'%i].ConstrainedSketch(name='__profile__', sheetSize=0.4)
    mdb.models['Model-%d'%i].sketches['__profile__'].ConstructionLine(point1=(0.0, -0.2), point2=(0.0, 0.2)) # Construction line
    mdb.models['Model-%d'%i].sketches['__profile__'].FixedConstraint(entity=mdb.models['Model-%d'%i].sketches['__profile__'].geometry[2])
    mdb.models['Model-%d'%i].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.0, height))
    mdb.models['Model-%d'%i].sketches['__profile__'].Line(point1=(0.0, height), point2=(tip_radius, height))
    mdb.models['Model-%d'%i].sketches['__profile__'].Line(point1=(tip_radius, height), point2=(radius, 0.0))
    mdb.models['Model-%d'%i].sketches['__profile__'].Line(point1=(radius, 0.0), point2=(0,0),)
    mdb.models['Model-%d'%i].sketches['__profile__'].FilletByRadius(
        curve1= mdb.models['Model-%d'%i].sketches['__profile__'].geometry[4],
        curve2= mdb.models['Model-%d'%i].sketches['__profile__'].geometry[5],
        nearPoint1=( 0.00317779183387756, 0.119968019425869), nearPoint2=(0.00496279075741768, 0.116709597408772), radius=stem_fillet
    )
    mdb.models['Model-%d'%i].Part(dimensionality=THREE_D, name=name, type=DEFORMABLE_BODY)
    mdb.models['Model-%d'%i].parts["stem"].BaseSolidRevolve(angle=360.0, flipRevolveDirection=OFF, sketch=mdb.models['Model-%d'%i].sketches['__profile__'])
    del mdb.models['Model-%d'%i].sketches['__profile__']
def cylinder(name, radius,height):
    # Create collar
    mdb.models['Model-%d'%i].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    mdb.models['Model-%d'%i].sketches['__profile__'].sketchOptions.setValues(decimalPlaces=3)
    mdb.models['Model-%d'%i].sketches['__profile__'].ConstructionLine(point1=(0.0,-0.05), point2=(0.0, 0.05))
    mdb.models['Model-%d'%i].sketches['__profile__'].rectangle(point1=(0.0, 0.0), point2=(radius, height))
    mdb.models['Model-%d'%i].Part(dimensionality=THREE_D, name=name, type= DEFORMABLE_BODY)
    mdb.models['Model-%d'%i].parts[name].BaseSolidRevolve(
        angle=360.0, flipRevolveDirection=OFF, sketch=mdb.models['Model-%d'%i].sketches['__profile__']
    )
    del mdb.models['Model-%d'%i].sketches['__profile__']
def quarter(name):
    mdb.models['Model-%d'%i].parts[name].DatumPlaneByPrincipalPlane(offset=0.0, principalPlane=YZPLANE)
    mdb.models['Model-%d'%i].parts[name].DatumPlaneByPrincipalPlane(offset=0.0, principalPlane=XYPLANE)
    mdb.models['Model-%d'%i].parts[name].PartitionCellByDatumPlane(
        cells=mdb.models['Model-%d'%i].parts[name].cells.getSequenceFromMask(('[#1 ]', ), ),
        datumPlane=mdb.models['Model-%d'%i].parts[name].datums[2]
    )
    mdb.models['Model-%d'%i].parts[name].PartitionCellByDatumPlane(
        cells=mdb.models['Model-%d'%i].parts[name].cells.getSequenceFromMask(('[#3 ]', ),),
        datumPlane=mdb.models['Model-%d'%i].parts[name].datums[3]
        )
def horizontal_partition(name):
    mdb.models['Model-%d'%i].parts[name].DatumPlaneByPrincipalPlane(offset=0.02, principalPlane=XZPLANE)
    mdb.models['Model-%d'%i].parts[name].PartitionCellByDatumPlane(
        cells=mdb.models['Model-%d'%i].parts[name].cells.getSequenceFromMask(('[#f ]', ), ),
        datumPlane=mdb.models['Model-%d'%i].parts[name].datums[6]
    )
def assign_material(name, range):
    mdb.models['Model-%d'%i].parts[name].SectionAssignment(
        offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
        region=Region(cells=mdb.models['Model-%d'%i].parts[name].cells.getSequenceFromMask(mask=(range, ), )),
        sectionName='Section-1', thicknessAssignment=FROM_SECTION
    )
def mesh(name, size, region):
    mdb.models['Model-%d'%i].parts[name].setMeshControls(
        algorithm=ADVANCING_FRONT, 
        elemShape=HEX_DOMINATED,
        regions=mdb.models['Model-%d'%i].parts[name].cells.getSequenceFromMask((region, ),), technique=SWEEP
    )
    mdb.models['Model-%d'%i].parts[name].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=size)
    mdb.models['Model-%d'%i].parts[name].generateMesh()
def output_requests(sensor):
    mdb.models['Model-%d'%i].FieldOutputRequest(
        createStepName='Step-1', frequency=1, 
        name=sensor, rebar=EXCLUDE, region=mdb.models['Model-%d'%i].rootAssembly.sets[sensor],
        sectionPoints=DEFAULT, variables=('U', )
    )
    mdb.models['Model-%d'%i].HistoryOutputRequest(
        createStepName='Step-1', name=sensor, rebar=EXCLUDE,
        region= mdb.models['Model-%d'%i].rootAssembly.sets[sensor],
        sectionPoints=DEFAULT, variables=('U1', 'U2', 'U3', 'UR1', 'UR2', 'UR3')
    )
def define_curve(curve):
    mdb.models['Model-%d'%i].PeriodicAmplitude(
        a_0=0.0, data=((0.0, curve.amp), ), frequency=curve.freq, name=curve.name, start=0.0, timeSpan=STEP
    )
    return curve.name
def apply_periodic_force(curve_name):
    mdb.models['Model-%d'%i].ConcentratedForce(
        amplitude=curve_name,
        cf3=-1.0, createStepName='Step-1', distributionType=UNIFORM, field='', localCsys=None, name='Load-1',
        region= mdb.models['Model-%d'%i].rootAssembly.sets['force_point']
    )
############################### Create model ###############################
stem("stem", stem_height, stem_radius, stem_tip_radius)
quarter("stem")
horizontal_partition("stem")
cylinder("collar", collar_radius,collar_height)
quarter("collar")
cylinder("base", base_radius,base_height)
quarter("base")

############################### Materials ###############################
mdb.models['Model-%d'%i].Material(name="Titanium")
mdb.models['Model-%d'%i].materials["Titanium"].Density(table=((4430, ), ))
mdb.models['Model-%d'%i].materials["Titanium"].Elastic(table=((114e9, 0.33), ))
mdb.models['Model-%d'%i].HomogeneousSolidSection(material="Titanium", name='Section-1', thickness=None)

############################### Assign material ###############################
assign_material("collar", '[#f ]')
assign_material("base",'[#f ]')
assign_material("stem", "[#ff ]")

############################### Assembly ###############################
mdb.models['Model-%d'%i].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-%d'%i].rootAssembly.Instance(dependent=ON, name='base-1', part=mdb.models['Model-%d'%i].parts['base'])
mdb.models['Model-%d'%i].rootAssembly.Instance(dependent=ON, name='collar-1', part=mdb.models['Model-%d'%i].parts['collar'])
mdb.models['Model-%d'%i].rootAssembly.Instance(dependent=ON, name='stem-1', part=mdb.models['Model-%d'%i].parts['stem'])
############################### Move pieces to right places ###############################
mdb.models['Model-%d'%i].rootAssembly.translate(instanceList=('collar-1', ), vector=(0.0, base_height, 0.0))
mdb.models['Model-%d'%i].rootAssembly.translate(instanceList=('stem-1', ), vector=(0.0, base_height+collar_height, 0.0))


############################### Create ties between parts ###############################
### Name the surfaces
mdb.models['Model-%d'%i].rootAssembly.Surface(name='base_top', side1Faces= mdb.models['Model-%d'%i].rootAssembly.instances['base-1'].faces.getSequenceFromMask(('[#3048 ]', ), ))
mdb.models['Model-%d'%i].rootAssembly.Surface(name='collar_bottom', side1Faces=mdb.models['Model-%d'%i].rootAssembly.instances['collar-1'].faces.getSequenceFromMask(('[#8214 ]', ), ))
mdb.models['Model-%d'%i].rootAssembly.Surface(name='collar_top', side1Faces=mdb.models['Model-%d'%i].rootAssembly.instances['collar-1'].faces.getSequenceFromMask(('[#3048 ]', ), ))
mdb.models['Model-%d'%i].rootAssembly.Surface(name='stem_bottom', side1Faces=mdb.models['Model-%d'%i].rootAssembly.instances['stem-1'].faces.getSequenceFromMask(('[#80448000 ]', ), ))
### Tie the surfaces
mdb.models['Model-%d'%i].Tie(
    adjust=ON, main= mdb.models['Model-%d'%i].rootAssembly.surfaces['stem_bottom'],
    name='stem-collar', positionToleranceMethod=COMPUTED, secondary=mdb.models['Model-%d'%i].rootAssembly.surfaces['collar_top'],
    thickness=ON, tieRotations=ON
)
mdb.models['Model-%d'%i].Tie(
    adjust=ON, main= mdb.models['Model-%d'%i].rootAssembly.surfaces['base_top'],
    name='collar-base', positionToleranceMethod=COMPUTED, secondary= mdb.models['Model-%d'%i].rootAssembly.surfaces['collar_bottom'],
    thickness=ON, tieRotations=ON
)
############################### Mesh ###############################
mesh("stem", 0.01,"[#ff ]")
mesh("collar", 0.01,"[#f ]")
mesh("base", 0.01,"[#f ]")

############################### Create points of interest ###############################
mdb.models['Model-%d'%i].rootAssembly.Set(
    name='vise-points', vertices= mdb.models['Model-%d'%i].rootAssembly.instances['stem-1'].vertices.getSequenceFromMask(('[#c ]', ), )
)
mdb.models['Model-%d'%i].rootAssembly.Set(
    name='force_point', vertices=mdb.models['Model-%d'%i].rootAssembly.instances['base-1'].vertices.getSequenceFromMask(('[#100 ]', ), )
)
mdb.models['Model-%d'%i].rootAssembly.Set(
    name='sensor_collar', vertices=mdb.models['Model-%d'%i].rootAssembly.instances['collar-1'].vertices.getSequenceFromMask(('[#80 ]', ), )
)
mdb.models['Model-%d'%i].rootAssembly.Set(
    name='sensor_stem', vertices=mdb.models['Model-%d'%i].rootAssembly.instances['stem-1'].vertices.getSequenceFromMask(('[#80 ]', ), )
)

############################### Boundary conditions ###############################
mdb.models['Model-%d'%i].EncastreBC(
    createStepName='Initial', localCsys=None, name='BC-1', region=mdb.models['Model-%d'%i].rootAssembly.sets['vise-points']
)
############################### Create step ###############################
mdb.models['Model-%d'%i].ImplicitDynamicsStep(
    description='Implicit solution with 0.01 step size', 
    initialInc=0.01, maxNumInc=1000, name='Step-1', nlgeom=ON, noStop=OFF, 
    nohaf=OFF, previous='Initial', timeIncrementationMethod=FIXED
)
############################### Request outputs ###############################
for sensor in sensors:
    output_requests(sensor)
############################### Apply periodic force ###############################
for curve in curves:
    sinusoid = define_curve(curve)
    apply_periodic_force(sinusoid)

############################### Create job ###############################
mdb.Job(
    atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-%d'%i, modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
    numCpus=6, numDomains=6, numGPUs=0, numThreadsPerMpiProcess=1, queue=None, 
    resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=
    0, waitMinutes=0
)