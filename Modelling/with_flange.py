# -*- coding: mbcs -*-
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

import math
# frequencies = [1, 10, 20, 30, 40]
# for i in range(50,901, 50):
#     frequencies.append(i)
jobs = []
frequencies = [100]
for i, frequency in enumerate(frequencies):
    period = 40.0/frequency
    increment = 1/(frequency*2.0*20)
    prefix = "" if i >= 10 else "0" 
    job_name = "Job-" + prefix + "%d_%d-Hz"%(i, frequency)
    model_name = "Model-%d"%(i)

    mdb.Model(modelType=STANDARD_EXPLICIT, name=model_name)
    mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=0.4)
    mdb.models[model_name].sketches['__profile__'].ConstructionLine(point1=(0.0, 
        -0.2), point2=(0.0, 0.2))
    mdb.models[model_name].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        0.0, 0.12))
    mdb.models[model_name].sketches['__profile__'].Line(point1=(0.0, 0.12), point2=(
        0.005, 0.12))
    mdb.models[model_name].sketches['__profile__'].Line(point1=(0.005, 0.12), 
        point2=(0.006, 0.0))
    mdb.models[model_name].sketches['__profile__'].Line(point1=(0.006, 0.0), point2=
        (0, 0))
    mdb.models[model_name].sketches['__profile__'].FilletByRadius(curve1=
        mdb.models[model_name].sketches['__profile__'].geometry[4], curve2=
        mdb.models[model_name].sketches['__profile__'].geometry[5], nearPoint1=(
        0.00317779183387756, 0.119968019425869), nearPoint2=(0.00496279075741768, 
        0.116709597408772), radius=0.0045)
    mdb.models[model_name].Part(dimensionality=THREE_D, name='stem', type=
        DEFORMABLE_BODY)
    mdb.models[model_name].parts['stem'].BaseSolidRevolve(angle=360.0, 
        flipRevolveDirection=OFF, sketch=
        mdb.models[model_name].sketches['__profile__'])
    del mdb.models[model_name].sketches['__profile__']
    mdb.models[model_name].parts['stem'].DatumPlaneByPrincipalPlane(offset=0.0, 
        principalPlane=YZPLANE)
    mdb.models[model_name].parts['stem'].DatumPlaneByPrincipalPlane(offset=0.0, 
        principalPlane=XYPLANE)
    mdb.models[model_name].parts['stem'].PartitionCellByDatumPlane(cells=
        mdb.models[model_name].parts['stem'].cells.getSequenceFromMask(('[#1 ]', ), 
        ), datumPlane=mdb.models[model_name].parts['stem'].datums[2])
    mdb.models[model_name].parts['stem'].PartitionCellByDatumPlane(cells=
        mdb.models[model_name].parts['stem'].cells.getSequenceFromMask(('[#3 ]', ), 
        ), datumPlane=mdb.models[model_name].parts['stem'].datums[3])
    mdb.models[model_name].parts['stem'].DatumPlaneByPrincipalPlane(offset=0.02, 
        principalPlane=XZPLANE)
    mdb.models[model_name].parts['stem'].PartitionCellByDatumPlane(cells=
        mdb.models[model_name].parts['stem'].cells.getSequenceFromMask(('[#f ]', ), 
        ), datumPlane=mdb.models[model_name].parts['stem'].datums[6])
    mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    mdb.models[model_name].sketches['__profile__'].sketchOptions.setValues(
        decimalPlaces=3)
    mdb.models[model_name].sketches['__profile__'].ConstructionLine(point1=(0.0, 
        -0.05), point2=(0.0, 0.05))
    mdb.models[model_name].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(0.014, 0.006))
    mdb.models[model_name].Part(dimensionality=THREE_D, name='collar', type=
        DEFORMABLE_BODY)
    mdb.models[model_name].parts['collar'].BaseSolidRevolve(angle=360.0, 
        flipRevolveDirection=OFF, sketch=
        mdb.models[model_name].sketches['__profile__'])
    del mdb.models[model_name].sketches['__profile__']
    mdb.models[model_name].parts['collar'].DatumPlaneByPrincipalPlane(offset=0.0, 
        principalPlane=YZPLANE)
    mdb.models[model_name].parts['collar'].DatumPlaneByPrincipalPlane(offset=0.0, 
        principalPlane=XYPLANE)
    mdb.models[model_name].parts['collar'].PartitionCellByDatumPlane(cells=
        mdb.models[model_name].parts['collar'].cells.getSequenceFromMask(('[#1 ]', 
        ), ), datumPlane=mdb.models[model_name].parts['collar'].datums[2])
    mdb.models[model_name].parts['collar'].PartitionCellByDatumPlane(cells=
        mdb.models[model_name].parts['collar'].cells.getSequenceFromMask(('[#3 ]', 
        ), ), datumPlane=mdb.models[model_name].parts['collar'].datums[3])
    mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    mdb.models[model_name].sketches['__profile__'].sketchOptions.setValues(
        decimalPlaces=3)
    mdb.models[model_name].sketches['__profile__'].ConstructionLine(point1=(0.0, 
        -0.05), point2=(0.0, 0.05))
    mdb.models[model_name].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(0.009, 0.045))
    mdb.models[model_name].Part(dimensionality=THREE_D, name='base', type=
        DEFORMABLE_BODY)
    mdb.models[model_name].parts['base'].BaseSolidRevolve(angle=360.0, 
        flipRevolveDirection=OFF, sketch=
        mdb.models[model_name].sketches['__profile__'])
    del mdb.models[model_name].sketches['__profile__']
    mdb.models[model_name].parts['base'].DatumPlaneByPrincipalPlane(offset=0.0, 
        principalPlane=YZPLANE)
    mdb.models[model_name].parts['base'].DatumPlaneByPrincipalPlane(offset=0.0, 
        principalPlane=XYPLANE)
    mdb.models[model_name].parts['base'].PartitionCellByDatumPlane(cells=
        mdb.models[model_name].parts['base'].cells.getSequenceFromMask(('[#1 ]', ), 
        ), datumPlane=mdb.models[model_name].parts['base'].datums[2])
    mdb.models[model_name].parts['base'].PartitionCellByDatumPlane(cells=
        mdb.models[model_name].parts['base'].cells.getSequenceFromMask(('[#3 ]', ), 
        ), datumPlane=mdb.models[model_name].parts['base'].datums[3])
    mdb.models[model_name].parts['base'].DatumPlaneByPrincipalPlane(offset=0.001, 
        principalPlane=XZPLANE)
    mdb.models[model_name].parts['base'].PartitionCellByDatumPlane(cells=
        mdb.models[model_name].parts['base'].cells.getSequenceFromMask(('[#f ]', ), 
        ), datumPlane=mdb.models[model_name].parts['base'].datums[6])
    mdb.models[model_name].Material(name='Titanium')
    mdb.models[model_name].materials['Titanium'].Density(table=((4430, ), ))
    mdb.models[model_name].materials['Titanium'].Elastic(table=((114000000000.0, 
        0.33), ))
    mdb.models[model_name].HomogeneousSolidSection(material='Titanium', name=
        'Section-1', thickness=None)
    mdb.models[model_name].parts['collar'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        cells=mdb.models[model_name].parts['collar'].cells.getSequenceFromMask(
        mask=('[#f ]', ), )), sectionName='Section-1', thicknessAssignment=
        FROM_SECTION)
    mdb.models[model_name].parts['base'].SectionAssignment(offset=0.0, offsetField=
        '', offsetType=MIDDLE_SURFACE, region=Region(
        cells=mdb.models[model_name].parts['base'].cells.getSequenceFromMask(mask=(
        '[#ff ]', ), )), sectionName='Section-1', thicknessAssignment=FROM_SECTION)
    mdb.models[model_name].parts['stem'].SectionAssignment(offset=0.0, offsetField=
        '', offsetType=MIDDLE_SURFACE, region=Region(
        cells=mdb.models[model_name].parts['stem'].cells.getSequenceFromMask(mask=(
        '[#ff ]', ), )), sectionName='Section-1', thicknessAssignment=FROM_SECTION)
    mdb.models[model_name].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models[model_name].rootAssembly.Instance(dependent=ON, name='base-1', part=
        mdb.models[model_name].parts['base'])
    mdb.models[model_name].rootAssembly.Instance(dependent=ON, name='collar-1', 
        part=mdb.models[model_name].parts['collar'])
    mdb.models[model_name].rootAssembly.Instance(dependent=ON, name='stem-1', part=
        mdb.models[model_name].parts['stem'])
    mdb.models[model_name].rootAssembly.translate(instanceList=('collar-1', ), 
        vector=(0.0, 0.045, 0.0))
    mdb.models[model_name].rootAssembly.translate(instanceList=('stem-1', ), vector=
        (0.0, 0.051, 0.0))
    mdb.models[model_name].rootAssembly.Surface(name='base_top', side1Faces=
        mdb.models[model_name].rootAssembly.instances['base-1'].faces.getSequenceFromMask(
        ('[#3048000 ]', ), ))
    mdb.models[model_name].rootAssembly.Surface(name='collar_bottom', side1Faces=
        mdb.models[model_name].rootAssembly.instances['collar-1'].faces.getSequenceFromMask(
        ('[#8214 ]', ), ))
    mdb.models[model_name].rootAssembly.Surface(name='collar_top', side1Faces=
        mdb.models[model_name].rootAssembly.instances['collar-1'].faces.getSequenceFromMask(
        ('[#3048 ]', ), ))
    mdb.models[model_name].rootAssembly.Surface(name='stem_bottom', side1Faces=
        mdb.models[model_name].rootAssembly.instances['stem-1'].faces.getSequenceFromMask(
        ('[#80448000 ]', ), ))
    mdb.models[model_name].Tie(adjust=ON, main=
        mdb.models[model_name].rootAssembly.surfaces['stem_bottom'], name=
        'stem-collar', positionToleranceMethod=COMPUTED, secondary=
        mdb.models[model_name].rootAssembly.surfaces['collar_top'], thickness=ON, 
        tieRotations=ON)
    mdb.models[model_name].Tie(adjust=ON, main=
        mdb.models[model_name].rootAssembly.surfaces['base_top'], name='collar-base'
        , positionToleranceMethod=COMPUTED, secondary=
        mdb.models[model_name].rootAssembly.surfaces['collar_bottom'], thickness=ON, 
        tieRotations=ON)
    mdb.models[model_name].parts['stem'].setMeshControls(algorithm=ADVANCING_FRONT, 
        elemShape=HEX_DOMINATED, regions=
        mdb.models[model_name].parts['stem'].cells.getSequenceFromMask(('[#ff ]', ), 
        ), technique=SWEEP)
    mdb.models[model_name].parts['stem'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.1, size=0.0025)
    mdb.models[model_name].parts['stem'].generateMesh()
    mdb.models[model_name].parts['collar'].setMeshControls(algorithm=ADVANCING_FRONT
        , elemShape=HEX_DOMINATED, regions=
        mdb.models[model_name].parts['collar'].cells.getSequenceFromMask(('[#f ]', 
        ), ), technique=SWEEP)
    mdb.models[model_name].parts['collar'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.1, size=0.0025)
    mdb.models[model_name].parts['collar'].generateMesh()
    mdb.models[model_name].parts['base'].setMeshControls(elemShape=TET, regions=
        mdb.models[model_name].parts['base'].cells.getSequenceFromMask(('[#ff ]', ), 
        ), technique=FREE)
    mdb.models[model_name].parts['base'].setElementType(elemTypes=(ElemType(
        elemCode=C3D20R, elemLibrary=STANDARD), ElemType(elemCode=C3D15, 
        elemLibrary=STANDARD), ElemType(elemCode=C3D10, elemLibrary=STANDARD)), 
        regions=(mdb.models[model_name].parts['base'].cells.getSequenceFromMask((
        '[#ff ]', ), ), ))
    mdb.models[model_name].parts['base'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.1, size=0.0025)
    
    mdb.models[model_name].rootAssembly.Set(name='vise_points', vertices=
        mdb.models[model_name].rootAssembly.instances['stem-1'].vertices.getSequenceFromMask(
        ('[#11 ]', ), ))
    mdb.models[model_name].rootAssembly.Set(name='sensor_stem', vertices=
        mdb.models[model_name].rootAssembly.instances['stem-1'].vertices.getSequenceFromMask(
        ('[#80 ]', ), ))
    mdb.models[model_name].rootAssembly.Set(name='force_point', vertices=
        mdb.models[model_name].rootAssembly.instances['base-1'].vertices.getSequenceFromMask(
        ('[#10 ]', ), ))
    mdb.models[model_name].rootAssembly.Set(name='sensor_base', vertices=
        mdb.models[model_name].rootAssembly.instances['base-1'].vertices.getSequenceFromMask(
        ('[#2000 ]', ), ))
    mdb.models[model_name].rootAssembly.Set(name='sensor_collar', vertices=
        mdb.models[model_name].rootAssembly.instances['collar-1'].vertices.getSequenceFromMask(
        ('[#80 ]', ), ))
    mdb.models[model_name].EncastreBC(createStepName='Initial', localCsys=None, 
        name='BC-1', region=mdb.models[model_name].rootAssembly.sets['vise_points'])

    mdb.models[model_name].ImplicitDynamicsStep(
        initialInc=increment,  maxNumInc= int(1e7),
        name='Step-1', noStop=OFF, nohaf=OFF, previous='Initial', timeIncrementationMethod=FIXED, 
        timePeriod=period
    )




    mdb.models[model_name].FieldOutputRequest(createStepName='Step-1', frequency=1, 
        name='sensor_stem', rebar=EXCLUDE, region=
        mdb.models[model_name].rootAssembly.sets['sensor_stem'], sectionPoints=
        DEFAULT, variables=('U', ))
    mdb.models[model_name].HistoryOutputRequest(createStepName='Step-1', frequency=1
        , name='sensor_stem', rebar=EXCLUDE, region=
        mdb.models[model_name].rootAssembly.sets['sensor_stem'], sectionPoints=
        DEFAULT, variables=('U1', 'U2', 'U3'))
    mdb.models[model_name].FieldOutputRequest(createStepName='Step-1', frequency=1, 
        name='sensor_collar', rebar=EXCLUDE, region=
        mdb.models[model_name].rootAssembly.sets['sensor_collar'], sectionPoints=
        DEFAULT, variables=('U', ))
    mdb.models[model_name].HistoryOutputRequest(createStepName='Step-1', frequency=1
        , name='sensor_collar', rebar=EXCLUDE, region=
        mdb.models[model_name].rootAssembly.sets['sensor_collar'], sectionPoints=
        DEFAULT, variables=('U1', 'U2', 'U3'))
    mdb.models[model_name].FieldOutputRequest(createStepName='Step-1', frequency=1, 
        name='sensor_base', rebar=EXCLUDE, region=
        mdb.models[model_name].rootAssembly.sets['sensor_base'], sectionPoints=
        DEFAULT, variables=('U', ))
    mdb.models[model_name].HistoryOutputRequest(createStepName='Step-1', frequency=1
        , name='sensor_base', rebar=EXCLUDE, region=
        mdb.models[model_name].rootAssembly.sets['sensor_base'], sectionPoints=
        DEFAULT, variables=('U1', 'U2', 'U3'))
    del mdb.models[model_name].historyOutputRequests['H-Output-1']


    mdb.models[model_name].PeriodicAmplitude(a_0=0.0, data=((0.0002, 0), ), 
        frequency=frequency*2*math.pi, name='Cos', start=0.0, timeSpan=STEP)


    mdb.models[model_name].ConcentratedForce(amplitude='Cos', cf1=-1.0, cf2=0.0, cf3=
        0.0, createStepName='Step-1', distributionType=UNIFORM, field='', 
        localCsys=None, name='Load-0', region=
        mdb.models[model_name].rootAssembly.sets['force_point'])
    mdb.models[model_name].parts['base'].DatumPlaneByPrincipalPlane(offset=-0.02, 
        principalPlane=XYPLANE)
    mdb.models[model_name].ConstrainedSketch(gridSpacing=0.003, name='__profile__', 
        sheetSize=0.129, transform=
        mdb.models[model_name].parts['base'].MakeSketchTransform(
        sketchPlane=mdb.models[model_name].parts['base'].datums[12], 
        sketchPlaneSide=SIDE1, 
        sketchUpEdge=mdb.models[model_name].parts['base'].edges[16], 
        sketchOrientation=RIGHT, origin=(0.0, 0.0225, -0.02)))
    mdb.models[model_name].sketches['__profile__'].sketchOptions.setValues(
        decimalPlaces=3)
    mdb.models[model_name].parts['base'].projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=mdb.models[model_name].sketches['__profile__'])
    mdb.models[model_name].sketches['__profile__'].rectangle(point1=(0.00675, 
        -0.0225), point2=(0.0165, 0.01125))
    mdb.models[model_name].sketches['__profile__'].FilletByRadius(curve1=
        mdb.models[model_name].sketches['__profile__'].geometry[4], curve2=
        mdb.models[model_name].sketches['__profile__'].geometry[3], nearPoint1=(
        0.0092452485114336, 0.0111499400436878), nearPoint2=(0.00667477631941438, 
        0.00609940752387047), radius=0.005)
    mdb.models[model_name].parts['base'].CutExtrude(flipExtrudeDirection=OFF, 
        sketch=mdb.models[model_name].sketches['__profile__'], sketchOrientation=
        RIGHT, sketchPlane=mdb.models[model_name].parts['base'].datums[12], 
        sketchPlaneSide=SIDE1, sketchUpEdge=
        mdb.models[model_name].parts['base'].edges[16])
    del mdb.models[model_name].sketches['__profile__']
    mdb.models[model_name].ConstrainedSketch(name='__edit__', objectToCopy=
        mdb.models[model_name].parts['base'].features['Cut extrude-1'].sketch)
    mdb.models[model_name].parts['base'].projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=mdb.models[model_name].sketches['__edit__'], 
        upToFeature=mdb.models[model_name].parts['base'].features['Cut extrude-1'])
    del mdb.models[model_name].sketches['__edit__']
    mdb.models[model_name].parts['base'].features['Cut extrude-1'].setValues(
        flipExtrudeDirection=True)
    mdb.models[model_name].parts['base'].regenerate()
    mdb.models[model_name].parts['base'].regenerate()
    del mdb.models[model_name].parts['base'].features['Cut extrude-1']
    mdb.models[model_name].ConstrainedSketch(gridSpacing=0.003, name='__profile__', 
        sheetSize=0.129, transform=
        mdb.models[model_name].parts['base'].MakeSketchTransform(
        sketchPlane=mdb.models[model_name].parts['base'].datums[12], 
        sketchPlaneSide=SIDE1, 
        sketchUpEdge=mdb.models[model_name].parts['base'].edges[16], 
        sketchOrientation=RIGHT, origin=(0.0, 0.0225, -0.02)))
    mdb.models[model_name].sketches['__profile__'].sketchOptions.setValues(
        decimalPlaces=3)
    mdb.models[model_name].parts['base'].projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=mdb.models[model_name].sketches['__profile__'])
    mdb.models[model_name].sketches['__profile__'].rectangle(point1=(0.00675, 
        -0.0225), point2=(0.01425, 0.0105))
    mdb.models[model_name].sketches['__profile__'].FilletByRadius(curve1=
        mdb.models[model_name].sketches['__profile__'].geometry[3], curve2=
        mdb.models[model_name].sketches['__profile__'].geometry[4], nearPoint1=(
        0.00680914893746376, 0.00671872772276402), nearPoint2=(0.00997525826096535, 
        0.010411229878664), radius=0.005)
    mdb.models[model_name].parts['base'].CutExtrude(flipExtrudeDirection=ON, sketch=
        mdb.models[model_name].sketches['__profile__'], sketchOrientation=RIGHT, 
        sketchPlane=mdb.models[model_name].parts['base'].datums[12], 
        sketchPlaneSide=SIDE1, sketchUpEdge=
        mdb.models[model_name].parts['base'].edges[16])
    del mdb.models[model_name].sketches['__profile__']
    mdb.models[model_name].parts['base'].generateMesh()
    mdb.models[model_name].rootAssembly.Set(name='force_point', vertices=
    mdb.models[model_name].rootAssembly.instances['base-1'].vertices.getSequenceFromMask(
    ('[#10 ]', ), ))
    mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=0.06)
    mdb.models[model_name].sketches['__profile__'].sketchOptions.setValues(
        decimalPlaces=3)
    mdb.models[model_name].sketches['__profile__'].ConstructionLine(point1=(0.0, 
        -0.03), point2=(0.0, 0.03))
    mdb.models[model_name].sketches['__profile__'].FixedConstraint(entity=
        mdb.models[model_name].sketches['__profile__'].geometry[2])
    mdb.models[model_name].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        0.0, 0.009))
    mdb.models[model_name].sketches['__profile__'].VerticalConstraint(addUndoState=
        False, entity=mdb.models[model_name].sketches['__profile__'].geometry[3])
    mdb.models[model_name].sketches['__profile__'].ParallelConstraint(addUndoState=
        False, entity1=mdb.models[model_name].sketches['__profile__'].geometry[2], 
        entity2=mdb.models[model_name].sketches['__profile__'].geometry[3])
    mdb.models[model_name].sketches['__profile__'].CoincidentConstraint(
        addUndoState=False, entity1=
        mdb.models[model_name].sketches['__profile__'].vertices[0], entity2=
        mdb.models[model_name].sketches['__profile__'].geometry[2])
    mdb.models[model_name].sketches['__profile__'].undo()
    mdb.models[model_name].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        0.009, 0.0))
    mdb.models[model_name].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models[model_name].sketches['__profile__'].geometry[3])
    mdb.models[model_name].sketches['__profile__'].PerpendicularConstraint(
        addUndoState=False, entity1=
        mdb.models[model_name].sketches['__profile__'].geometry[2], entity2=
        mdb.models[model_name].sketches['__profile__'].geometry[3])
    mdb.models[model_name].sketches['__profile__'].CoincidentConstraint(
        addUndoState=False, entity1=
        mdb.models[model_name].sketches['__profile__'].vertices[0], entity2=
        mdb.models[model_name].sketches['__profile__'].geometry[2])
    mdb.models[model_name].sketches['__profile__'].Line(point1=(0.009, 0.0), point2=
        (0.009, 0.009))
    mdb.models[model_name].sketches['__profile__'].VerticalConstraint(addUndoState=
        False, entity=mdb.models[model_name].sketches['__profile__'].geometry[4])
    mdb.models[model_name].sketches['__profile__'].PerpendicularConstraint(
        addUndoState=False, entity1=
        mdb.models[model_name].sketches['__profile__'].geometry[3], entity2=
        mdb.models[model_name].sketches['__profile__'].geometry[4])
    mdb.models[model_name].sketches['__profile__'].setAsConstruction(objectList=(
        mdb.models[model_name].sketches['__profile__'].geometry[3], ))
    mdb.models[model_name].sketches['__profile__'].setAsConstruction(objectList=(
        mdb.models[model_name].sketches['__profile__'].geometry[4], ))
    mdb.models[model_name].sketches['__profile__'].Line(point1=(0.009, 0.0), point2=
        (0.0, 0.0))
    mdb.models[model_name].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models[model_name].sketches['__profile__'].geometry[5])
    mdb.models[model_name].sketches['__profile__'].ParallelConstraint(addUndoState=
        False, entity1=mdb.models[model_name].sketches['__profile__'].geometry[3], 
        entity2=mdb.models[model_name].sketches['__profile__'].geometry[5])
    mdb.models[model_name].sketches['__profile__'].undo()
    mdb.models[model_name].sketches['__profile__'].Line(point1=(0.009, 0.0), point2=
        (0.018, 0.0))
    mdb.models[model_name].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models[model_name].sketches['__profile__'].geometry[5])
    mdb.models[model_name].sketches['__profile__'].ParallelConstraint(addUndoState=
        False, entity1=mdb.models[model_name].sketches['__profile__'].geometry[3], 
        entity2=mdb.models[model_name].sketches['__profile__'].geometry[5])
    mdb.models[model_name].sketches['__profile__'].setAsConstruction(objectList=(
        mdb.models[model_name].sketches['__profile__'].geometry[5], ))
    mdb.models[model_name].sketches['__profile__'].undo()
    mdb.models[model_name].sketches['__profile__'].undo()
    mdb.models[model_name].sketches['__profile__'].Line(point1=(0.009, 0.009), 
        point2=(0.0179999999618158, 0.009))
    mdb.models[model_name].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models[model_name].sketches['__profile__'].geometry[5])
    mdb.models[model_name].sketches['__profile__'].PerpendicularConstraint(
        addUndoState=False, entity1=
        mdb.models[model_name].sketches['__profile__'].geometry[4], entity2=
        mdb.models[model_name].sketches['__profile__'].geometry[5])
    mdb.models[model_name].sketches['__profile__'].setAsConstruction(objectList=(
        mdb.models[model_name].sketches['__profile__'].geometry[5], ))
    mdb.models[model_name].sketches['__profile__'].ArcByCenterEnds(center=(0.009, 
        0.009), direction=COUNTERCLOCKWISE, point1=(0.009, 0.0), point2=(
        0.0179999999618158, 0.009))
    mdb.models[model_name].sketches['__profile__'].offset(distance=0.001, 
        objectList=(mdb.models[model_name].sketches['__profile__'].geometry[6], ), 
        side=LEFT)
    mdb.models[model_name].sketches['__profile__'].Line(point1=(0.017, 0.009), 
        point2=(0.018, 0.009))
    mdb.models[model_name].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models[model_name].sketches['__profile__'].geometry[8])
    mdb.models[model_name].sketches['__profile__'].PerpendicularConstraint(
        addUndoState=False, entity1=
        mdb.models[model_name].sketches['__profile__'].geometry[7], entity2=
        mdb.models[model_name].sketches['__profile__'].geometry[8])
    mdb.models[model_name].sketches['__profile__'].Line(point1=(0.009, 0.001), 
        point2=(0.009, 0.0))
    mdb.models[model_name].sketches['__profile__'].VerticalConstraint(addUndoState=
        False, entity=mdb.models[model_name].sketches['__profile__'].geometry[9])
    mdb.models[model_name].sketches['__profile__'].PerpendicularConstraint(
        addUndoState=False, entity1=
        mdb.models[model_name].sketches['__profile__'].geometry[7], entity2=
        mdb.models[model_name].sketches['__profile__'].geometry[9])
    mdb.models[model_name].sketches['__profile__'].sketchOptions.setValues(
        constructionGeometry=ON)
    mdb.models[model_name].sketches['__profile__'].assignCenterline(line=
        mdb.models[model_name].sketches['__profile__'].geometry[2])
    mdb.models[model_name].Part(dimensionality=THREE_D, name='flange', type=
        DEFORMABLE_BODY)
    mdb.models[model_name].parts['flange'].BaseSolidRevolve(angle=360.0, 
        flipRevolveDirection=OFF, sketch=
        mdb.models[model_name].sketches['__profile__'])
    del mdb.models[model_name].sketches['__profile__']

    mdb.models['Model-0'].parts['flange'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        cells=mdb.models['Model-0'].parts['flange'].cells.getSequenceFromMask(
        mask=('[#1 ]', ), )), sectionName='Section-1', thicknessAssignment=
        FROM_SECTION)
    mdb.models[model_name].rootAssembly.Instance(dependent=ON, name='flange-1', 
        part=mdb.models[model_name].parts['flange'])
    mdb.models[model_name].rootAssembly.translate(instanceList=('flange-1', ), 
        vector=(0.0, 0.04, 0.0))
    mdb.models[model_name].Tie(adjust=ON, main=Region(
        side1Faces=mdb.models[model_name].rootAssembly.instances['flange-1'].faces.getSequenceFromMask(
        mask=('[#8 ]', ), )), name='Constraint-3', positionToleranceMethod=COMPUTED
        , secondary=Region(
        side1Faces=mdb.models[model_name].rootAssembly.instances['base-1'].faces.getSequenceFromMask(
        mask=('[#8014057 ]', ), )), thickness=ON, tieRotations=ON)
    mdb.models[model_name].parts['flange'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=0.0025)
    mdb.models[model_name].parts['flange'].setMeshControls(elemShape=TET, regions=
        mdb.models[model_name].parts['flange'].cells.getSequenceFromMask(('[#1 ]', 
        ), ), technique=FREE)
    mdb.models[model_name].parts['flange'].setElementType(elemTypes=(ElemType(
        elemCode=C3D20R, elemLibrary=STANDARD), ElemType(elemCode=C3D15, 
        elemLibrary=STANDARD), ElemType(elemCode=C3D10, elemLibrary=STANDARD)), 
        regions=(mdb.models[model_name].parts['flange'].cells.getSequenceFromMask((
        '[#1 ]', ), ), ))
    mdb.models[model_name].parts['flange'].generateMesh()

    mdb.Job(
        atTime=None, contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE,
        model=model_name,
        name=job_name, 
        nodalOutputPrecision=SINGLE, numCpus=6, numDomains=6, numGPUs=0, 
        numThreadsPerMpiProcess=1, queue=None, resultsFormat=ODB, scratch='',
        type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0, modelPrint=OFF, multiprocessingMode=DEFAULT,
    )
    jobs.append(job_name)