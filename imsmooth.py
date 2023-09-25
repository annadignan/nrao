###PURPOSE: run imsmooth on all of the VLA data

#########################################################
#create two lists:
#(1) all of the files we want to run imsmooth on and 
#(2) all of the directories containing the files from (1)
#########################################################

#import statements
import os
from pathlib import Path
import glob
import numpy as np

#change path to where the data is
path = '/lustre/cv/students/adignan/data/'

#ignore the misc folder
exclude='misc'

#initialize empty lists
folders = []
files = []

for (root, dirs, file) in os.walk(path):
    #ignore the misc folder
    dirs[:] = [d for d in dirs if d not in exclude]
    #creating list (2)
    for f in dirs:
        if 'NGC' in f:
            # added this "not in" to avoid double counting a source due to a subdirectory
            if f not in folders:
                folders.append(f)
    #creating list (1)
    for f in file:
        if 'ngc' in f:
            files.append(f)
            
#create a list of just the #### part of the filenames for later use

#initialize empty list
names=[]

for f in files:
    name=f[3:7]
    names.append(name)

#convert list to set to remove duplicates
names=set(names)

#getting list of paths to files
filenames=[]

for i in names:
    filename=glob.glob(path+'NGC'+str(i)+'/ngc'+str(i)+'*')
    filenames=filenames+filename 

#making a list of savenames (complete path)
savenames=[]    

for f in filenames:
    savename=str(f[:-5])+'.gbt_resmatched'
    savenames.append(savename)
    
#########################################################
#run imsmooth!!!
#########################################################

#read in csv file with beam info
# beamfile=pd.read_csv('/lustre/cv/students/adignan/beam_info.csv')
beamfile=np.genfromtxt('/lustre/cv/students/adignan/beam_info.csv', delimiter=',',dtype=str,unpack=True,skip_header=1)
source,bmaj,bmin=beamfile

for i,j in (zip(filenames[:5],savenames[:5])):
    #get the beam values for each source
        index=np.where((source)==str(i[33:40]))
        bmajor=float(bmaj[index])   
        imsmooth(imagename=str(i),kernel='gauss',targetres=True,major=bmajor,minor=bmajor,pa='0deg',outfile=str(j))