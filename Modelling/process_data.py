from odbAccess import *
from odbMaterial import *
from odbSection import *
from abaqusConstants import *

import os
import shutil

from generate_models import get_jobs
jobs = get_jobs()

for job in jobs:
    file = open('Results_fromODB.txt' , 'w')
 
    path='./'                    # set odb path here
    myodbpath=path+job+'.odb'
    odb=openOdb(myodbpath)
    

    for keys in odb.steps['Step-1'].historyRegions.keys():
                    
        tipHistories = odb.steps['Step-1'].historyRegions[keys]
    
        HistoryOutput_RF2 = tipHistories.historyOutputs['RF2'].data

        def column(matrix, i):
            return [row[i] for row in matrix]
            
            
        RF2_values=column(HistoryOutput_RF2,1)
        Time_values=column(HistoryOutput_RF2,0)
        
        Load = RF2_values[-1]
        
        Total_load += Load
       
    odb.close()
    Displacement = 1.0
    Area = 20.0
    Original_length = 20.0
    
    Stress = -Total_load/Area
    Strain = Displacement/Original_length
        
    Homogenized_E = Stress/Strain
    
    Average_Homogenized_E += Homogenized_E
    
    file.write('\n Homogenized Youngs Modulus E from Job-%d is: %f '%(q,Homogenized_E))

    isFirstIP = True

    file.write('\n')  
    
Average_Homogenized_E = Average_Homogenized_E/(Max_iterations-1)
file.write('\n Averaged Homogenized Youngs Modulus E is: %f '%(Average_Homogenized_E))  
file.write('\n')        
file.close()    





# 9.4 - Save History Output results into tables that become CVS file
 
    odbF_Step = odbFile.steps['Step-1']
    Salvar_3_Modelos=[] 
    Salvar_2_Modelos=[] 
    
    Tabela_Tempo_U_temp=[]
    Tabela_Experimento_temp=[]
    Tabela_y_Defeito_temp=[]
    Tabela_x_Defeito_temp=[]
    Tabela_Forca_Defeito_temp=[]
    Tabela_Raio_Defeito_temp=[]   
    
    # For each defined region where history outputs are defined   
    for historyRegionsName in odbF_Step.historyRegions.keys():
         # If historyRegionsName = 'Assembly ASSEMBLY', meaning that it is the entire component
        if historyRegionsName == 'Assembly ASSEMBLY':
             # skip this element
            continue
        else:
            odb_hReg = odbF_Step.historyRegions[historyRegionsName]
             # Get point coordinates
            x_pos = odb_hReg.point.node.coordinates[0]
            y_pos = odb_hReg.point.node.coordinates[1]
            z_pos = odb_hReg.point.node.coordinates[2]
  
 ### 9.4.3 - Save U3 History output data
        
        #if SaveU3Data == True:
            # Make csv file name and path
    
        temporario_tempo=[]
        temporario_U3=[]
        
        for dataline in odb_hReg.historyOutputs['U1'].data:
            (TimeStamp, U3Val) = dataline
            temporario_tempo.append(TimeStamp)
            temporario_U3.append(U3Val)
            
        Salvar_3_Modelos.append(temporario_tempo)
        Salvar_3_Modelos.append(temporario_U3)
        
        ############### variavel U2 #############
        temporario_tempo_U2=[]
        temporario_U2=[]
        
        for dataline in odb_hReg.historyOutputs['U2'].data:
            (TimeStamp, U3Val) = dataline
            temporario_tempo.append(TimeStamp)
            temporario_U2.append(U3Val)
            
        Salvar_2_Modelos.append(temporario_tempo_U2)
        Salvar_2_Modelos.append(temporario_U2)
        
         ############################################   
        
        Tabela_Experimento_temp.append(experimento)
        Tabela_y_Defeito_temp.append(Defect_center[sim][1])
        Tabela_x_Defeito_temp.append(Defect_center[sim][0])
        Tabela_Forca_Defeito_temp=[]
        Tabela_Raio_Defeito_temp.append(Defect_radius[sim])
        
        Tabela_Experimento_temp.append(experimento)
        Tabela_y_Defeito_temp.append(Defect_center[sim][1])
        Tabela_x_Defeito_temp.append(Defect_center[sim][0])
        Tabela_Forca_Defeito_temp=[]
        Tabela_Raio_Defeito_temp.append(Defect_radius[sim])

    # Tabelas de tabelas para colocar defeitos suas caracteristicas na frente dos dados
    Tabela_Experimento.append(Tabela_Experimento_temp)
    Tabela_y_Defeito.append(Tabela_y_Defeito_temp)
    Tabela_x_Defeito.append(Tabela_x_Defeito_temp)
    Tabela_Forca_Defeito.append(Tabela_Forca_Defeito_temp)
    Tabela_Raio_Defeito.append(Tabela_Raio_Defeito_temp)
    experimento=experimento+1

    # Deletar a repeticao do tempo em todas as tabelas
    del Salvar_3_Modelos[2::2]
    del Salvar_2_Modelos[2::2]
    del Tabela_Experimento[sim][2::2]
    del Tabela_x_Defeito[sim][2::2]
    del Tabela_y_Defeito[sim][2::2]
    del Tabela_Raio_Defeito[sim][2::2]
    Salvar_Todo_Modelos.append(Salvar_3_Modelos)
    Salvar_Todo_Modelos.append(Salvar_2_Modelos)
   
# Unir todos os dados para poder imprimir no CSV    
for i in range (0,len(Salvar_Todo_Modelos)):
    for j in range (0,len(Salvar_Todo_Modelos[0])):
        Salvar_Todo_Modelos[i][j] =[ Tabela_Experimento[i][j]] + [Tabela_x_Defeito[i][j]] + [Tabela_y_Defeito[i][j]] + [Tabela_Raio_Defeito[i][j]]+ Salvar_Todo_Modelos[i][j]
        
    
# 9.5 - Save .cae file 
mdb.saveAs('Test.cae')


# Make csv file name and save data
csvName2 = 'batataFinal.csv'
ResultsFile = ResultsFolderPath_BASE + '/' + csvName2
with open(ResultsFile, 'wb') as csvFile2:
    for i in range (0,len(Salvar_Todo_Modelos)):
        for j in range (0,len(  Salvar_Todo_Modelos[0])):
            csv.writer(csvFile2).writerows([Salvar_Todo_Modelos[i][j]])
     


print('Simulations ended at ' + str(datetime.datetime.now()))
    