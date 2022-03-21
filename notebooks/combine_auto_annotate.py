import DecoID.DecoID as DecoID
import numpy as np
import os

#parameters
datadir = "../MSMS/"
polarities = ["pos/","neg/"]
subdirs = ["data/ORBI/","data/QTOF/"]

decoID = DecoID.DecoID("none", "reference", numCores=1)

for pol in polarities:
    filenamesToCombine = []
    for subdir in subdirs:
        filenamesToCombine += [datadir + pol + subdir + x.replace("_decoID.csv","") for x in os.listdir(datadir + pol + subdir) if "inHouse_decoID.csv" in x]
        decoID.combineResultsAutoAnnotate(filenamesToCombine,datadir + pol + "combined_resultsTOP1_above80_in-house.csv",numHits=1,min_score=80)