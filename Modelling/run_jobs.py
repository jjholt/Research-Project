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

from generate_models import get_jobs
jobs = get_jobs()

for job in jobs:
    mdb.jobs[job].writeInput()
    mdb.jobs[job].submit(consistencyChecking=OFF)    
    mdb.jobs[job].waitForCompletion()