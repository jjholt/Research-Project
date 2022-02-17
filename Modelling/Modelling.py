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

class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        self.force_offset_from_base = 0.001
        self.force_direction = (0.0, 0.0, -1.0)
        self.mesh_size = 0.01
        self._frequency = 2*math.pi*900
        self.amplitude = 200e-6
        self.curve_name = "Sinewave"
        self.stem_height = 0.12
        self.stem_radius = 0.006
        self.stem_tip_radius = 0.005
        self.collar_radius = 0.014
        self.collar_height = 0.006
        self.base_height = 0.045
        self.base_radius = 0.009
        self.stem_fillet = 0.0045
        self.sensors = ['sensor_stem', 'sensor_collar']
        mdb.Model(modelType=STANDARD_EXPLICIT, name=model_name)
    def __create_stem(self,name, height,radius,tip_radius, stem_fillet):
        # Create stem
        mdb.models[self.model_name].ConstrainedSketch(name='__profile__', sheetSize=0.4)
        mdb.models[self.model_name].sketches['__profile__'].ConstructionLine(point1=(0.0, -0.2), point2=(0.0, 0.2)) # Construction line
        mdb.models[self.model_name].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.0, height))
        mdb.models[self.model_name].sketches['__profile__'].Line(point1=(0.0, height), point2=(tip_radius, height))
        mdb.models[self.model_name].sketches['__profile__'].Line(point1=(tip_radius, height), point2=(radius, 0.0))
        mdb.models[self.model_name].sketches['__profile__'].Line(point1=(radius, 0.0), point2=(0,0),)
        mdb.models[self.model_name].sketches['__profile__'].FilletByRadius(
            curve1= mdb.models[self.model_name].sketches['__profile__'].geometry[4],
            curve2= mdb.models[self.model_name].sketches['__profile__'].geometry[5],
            nearPoint1=( 0.00317779183387756, 0.119968019425869), nearPoint2=(0.00496279075741768, 0.116709597408772), radius=stem_fillet
        )
        mdb.models[self.model_name].Part(dimensionality=THREE_D, name=name, type=DEFORMABLE_BODY)
        mdb.models[self.model_name].parts["stem"].BaseSolidRevolve(angle=360.0, flipRevolveDirection=OFF, sketch=mdb.models[self.model_name].sketches['__profile__'])
        del mdb.models[self.model_name].sketches['__profile__']
        return name
    def __create_cylinder(self,name, radius,height):
        # Create collar
        mdb.models[self.model_name].ConstrainedSketch(name='__profile__', sheetSize=0.1)
        mdb.models[self.model_name].sketches['__profile__'].sketchOptions.setValues(decimalPlaces=3)
        mdb.models[self.model_name].sketches['__profile__'].ConstructionLine(point1=(0.0,-0.05), point2=(0.0, 0.05))
        mdb.models[self.model_name].sketches['__profile__'].rectangle(point1=(0.0, 0.0), point2=(radius, height))
        mdb.models[self.model_name].Part(dimensionality=THREE_D, name=name, type= DEFORMABLE_BODY)
        mdb.models[self.model_name].parts[name].BaseSolidRevolve(
            angle=360.0, flipRevolveDirection=OFF, sketch=mdb.models[self.model_name].sketches['__profile__']
        )
        del mdb.models[self.model_name].sketches['__profile__']
        return name
    def __quarter(self, name):
        mdb.models[self.model_name].parts[name].DatumPlaneByPrincipalPlane(offset=0.0, principalPlane=YZPLANE)
        mdb.models[self.model_name].parts[name].DatumPlaneByPrincipalPlane(offset=0.0, principalPlane=XYPLANE)
        mdb.models[self.model_name].parts[name].PartitionCellByDatumPlane(
            cells=mdb.models[self.model_name].parts[name].cells.getSequenceFromMask(('[#1 ]', ), ),
            datumPlane=mdb.models[self.model_name].parts[name].datums[2]
        )
        mdb.models[self.model_name].parts[name].PartitionCellByDatumPlane(
            cells=mdb.models[self.model_name].parts[name].cells.getSequenceFromMask(('[#3 ]', ),),
            datumPlane=mdb.models[self.model_name].parts[name].datums[3]
            )
    def __set_force_offset(self, force_offset):
        mdb.models[self.model_name].parts["base"].DatumPlaneByPrincipalPlane(
        offset=force_offset, principalPlane=XZPLANE
        )
        mdb.models[self.model_name].parts["base"].PartitionCellByDatumPlane(
            cells= mdb.models[self.model_name].parts["base"].cells.getSequenceFromMask(('[#f ]', ), ),
            datumPlane=mdb.models[self.model_name].parts["base"].datums[6]
        )
    def __horizontal_partition(self, name):
        mdb.models[self.model_name].parts[name].DatumPlaneByPrincipalPlane(offset=0.02, principalPlane=XZPLANE)
        mdb.models[self.model_name].parts[name].PartitionCellByDatumPlane(
            cells=mdb.models[self.model_name].parts[name].cells.getSequenceFromMask(('[#f ]', ), ),
            datumPlane=mdb.models[self.model_name].parts[name].datums[6]
        )
    def __assign_material(self, name, range):
        mdb.models[self.model_name].parts[name].SectionAssignment(
            offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
            region=Region(cells=mdb.models[self.model_name].parts[name].cells.getSequenceFromMask(mask=(range, ), )),
            sectionName='Section-1', thicknessAssignment=FROM_SECTION
        )
    def __mesh_part(self, name, size, region):
        mdb.models[self.model_name].parts[name].setMeshControls(
            algorithm=ADVANCING_FRONT, 
            elemShape=HEX_DOMINATED,
            regions=mdb.models[self.model_name].parts[name].cells.getSequenceFromMask((region, ),),
            technique=SWEEP
        )
        mdb.models[self.model_name].parts[name].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=size)
        mdb.models[self.model_name].parts[name].generateMesh()
    def __output_requests(self, sensors):
        for sensor in sensors:
            mdb.models[self.model_name].FieldOutputRequest(
                createStepName='Step-1', frequency=1, 
                name=sensor, rebar=EXCLUDE, region=mdb.models[self.model_name].rootAssembly.sets[sensor],
                sectionPoints=DEFAULT, variables=('U', )
            )
            mdb.models[self.model_name].HistoryOutputRequest(
                createStepName='Step-1', name=sensor, rebar=EXCLUDE,
                region= mdb.models[self.model_name].rootAssembly.sets[sensor],
                sectionPoints=DEFAULT, variables=('U1', 'U2', 'U3')
            )
        del mdb.models[self.model_name].historyOutputRequests['H-Output-1']
    def __create_titanium(self):
        mdb.models[self.model_name].Material(name="Titanium")
        mdb.models[self.model_name].materials["Titanium"].Density(table=((4430, ), ))
        mdb.models[self.model_name].materials["Titanium"].Elastic(table=((114e9, 0.33), ))
        mdb.models[self.model_name].HomogeneousSolidSection(material="Titanium", name='Section-1', thickness=None)
    def __assemble(self):
        mdb.models[self.model_name].rootAssembly.DatumCsysByDefault(CARTESIAN)
        mdb.models[self.model_name].rootAssembly.Instance(dependent=ON, name='base-1', part=mdb.models[self.model_name].parts["base"])
        mdb.models[self.model_name].rootAssembly.Instance(dependent=ON, name='collar-1', part=mdb.models[self.model_name].parts["collar"])
        mdb.models[self.model_name].rootAssembly.Instance(dependent=ON, name='stem-1', part=mdb.models[self.model_name].parts["stem"])
        ############################### Move pieces to right places ###############################
        mdb.models[self.model_name].rootAssembly.translate(instanceList=('collar-1', ), vector=(0.0, self.base_height, 0.0))
        mdb.models[self.model_name].rootAssembly.translate(instanceList=('stem-1', ), vector=(0.0, self.base_height+self.collar_height, 0.0))
    def __tie(self):
        ### Name the surfaces
        mdb.models[self.model_name].rootAssembly.Surface(
            name='base_top', side1Faces= mdb.models[self.model_name].rootAssembly.instances['base-1'].faces.findAt(
                ((0.005898, self.base_height, 0.000776), ),
                ((-0.005898, self.base_height, 0.000776), ), 
                ((-0.005898, self.base_height, -0.000776), ), 
                ((0.005898, self.base_height, -0.000776), ), 
            )
        )
        mdb.models[self.model_name].rootAssembly.Surface(name='collar_bottom', side1Faces=mdb.models[self.model_name].rootAssembly.instances['collar-1'].faces.getSequenceFromMask(('[#8214 ]', ), ))
        mdb.models[self.model_name].rootAssembly.Surface(name='collar_top', side1Faces=mdb.models[self.model_name].rootAssembly.instances['collar-1'].faces.getSequenceFromMask(('[#3048 ]', ), ))
        mdb.models[self.model_name].rootAssembly.Surface(name='stem_bottom', side1Faces=mdb.models[self.model_name].rootAssembly.instances['stem-1'].faces.getSequenceFromMask(('[#80448000 ]', ), ))
        ### Tie the surfaces
        mdb.models[self.model_name].Tie(
            adjust=ON, main= mdb.models[self.model_name].rootAssembly.surfaces['stem_bottom'],
            name='stem-collar', positionToleranceMethod=COMPUTED, secondary=mdb.models[self.model_name].rootAssembly.surfaces['collar_top'],
            thickness=ON, tieRotations=ON
        )
        mdb.models[self.model_name].Tie(
            adjust=ON, main= mdb.models[self.model_name].rootAssembly.surfaces['base_top'],
            name='collar-base', positionToleranceMethod=COMPUTED, secondary= mdb.models[self.model_name].rootAssembly.surfaces['collar_bottom'],
            thickness=ON, tieRotations=ON
        )
    def __points_of_interest(self):        
        mdb.models[self.model_name].rootAssembly.Set(
            name='vise_points',
            vertices= mdb.models[self.model_name].rootAssembly.instances['stem-1'].vertices.findAt(((0.005833, 0.071, 0.0), ), ((-0.005833, 0.071, 0.0), ), )
        )
        mdb.models[self.model_name].rootAssembly.Set(
            name='force_point',
            vertices= mdb.models[self.model_name].rootAssembly.instances['base-1'].vertices.findAt(((0.0, self.force_offset_from_base, self.base_radius), ))
        )
        mdb.models[self.model_name].rootAssembly.Set(
            name='sensor_collar',
            vertices=mdb.models[self.model_name].rootAssembly.instances['collar-1'].vertices.findAt(((0.0, self.base_height+self.collar_height, self.collar_radius), ))
        )
        mdb.models[self.model_name].rootAssembly.Set(
            name='sensor_stem',
            vertices= mdb.models[self.model_name].rootAssembly.instances['stem-1'].vertices.findAt(((0.0, 0.166537, 0.005037), ))
        )
    def __boundaries(self):
        mdb.models[self.model_name].EncastreBC(
            createStepName='Initial', localCsys=None, name='BC-1', region=mdb.models[self.model_name].rootAssembly.sets['vise_points']
        )
    def __step(self):
        mdb.models[self.model_name].ImplicitDynamicsStep(
            initialInc=1e-05, minInc=1e-06, maxNumInc=10000, name='Step-1', previous='Initial', timePeriod=float(1.0/self.frequency)
        )
    def __apply_force(self, force_direction):
        mdb.models[self.model_name].ConcentratedForce(
            amplitude=self.curve_name,
            cf1=force_direction[0], cf2=force_direction[1], cf3=force_direction[2],
            createStepName='Step-1', distributionType=UNIFORM, field='', localCsys=None, name='Load-1',
            region= mdb.models[self.model_name].rootAssembly.sets['force_point']
        )
    def __create_curve(self):
        mdb.models[self.model_name].PeriodicAmplitude(
            a_0=0.0, data=((0.0, self.amplitude), ), frequency=self.frequency, name=self.curve_name, start=0.0, timeSpan=STEP
        )

    @property
    def frequency(self):
        return self._frequency
    @frequency.setter
    def frequency(self, freq): # Linear frequency!!!!
        self._frequency = 2*math.pi*freq
    def job(self, job_name, job_list):
        mdb.Job(
            atTime=None, contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE,
            model=self.model_name,
            name=job_name, 
            nodalOutputPrecision=SINGLE, numCpus=6, numDomains=6, numGPUs=0, 
            numThreadsPerMpiProcess=1, queue=None, resultsFormat=ODB, scratch='',
            type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0, modelPrint=OFF, multiprocessingMode=DEFAULT,
        )
        job_list.append(job_name)
    def new(self):
        stem = self.__create_stem("stem", self.stem_height, self.stem_radius, self.stem_tip_radius, self.stem_fillet)
        self.__quarter(stem)
        self.__horizontal_partition(stem)
        collar = self.__create_cylinder("collar", self.collar_radius, self.collar_height)
        self.__quarter(collar)
        base = self.__create_cylinder("base", self.base_radius, self.base_height)
        self.__quarter(base)
        self.__set_force_offset(self.force_offset_from_base)
        ############################### Materials ###############################
        self.__create_titanium()

        ############################### Assign material ###############################
        self.__assign_material(collar, '[#f ]')
        self.__assign_material(base,'[#ff ]')
        self.__assign_material(stem, "[#ff ]")

        ############################### Assemble ###############################
        self.__assemble()
        self.__tie()

        ############################### _mesh ###############################
        self.__mesh_part(stem, self.mesh_size,"[#ff ]")
        self.__mesh_part(collar, self.mesh_size,"[#f ]")
        self.__mesh_part(base, self.mesh_size,"[#ff ]")

        ############################## Create points of interest ###############################
        self.__points_of_interest()
        self.__boundaries()
        self.__step()

        ############################### Request outputs ###############################

        self.__output_requests(self.sensors)
        ############################### Apply periodic force ###############################
        self.__create_curve()
        self.__apply_force(self.force_direction)

jobs = []
models = []

############# Things you probably want to change ###########
# force_offset_from_base = 0.001
# force_direction = (0.0, 0.0, -1.0)
# mesh_size = 0.01
# frequency = 2*math.pi*900
# amplitude = 200e-6
# stem_height = 0.12
# stem_radius = 0.006
# stem_tip_radius = 0.005
# collar_radius = 0.014
# collar_height = 0.006
# base_height = 0.045
# base_radius = 0.009
# stem_fillet = 0.0045
# sensors = [ # Requires a bit of setup to include more sensors.
#     'sensor_stem', 'sensor_collar',
# ]