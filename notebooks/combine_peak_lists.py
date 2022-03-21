import sys
import os
sys.path.append("../src/")
import pandas as pd

from detection_helper import *

polarities = ["negative","positive"]

batches = ["E","J","L","N","Q","R","AX/F","AX/G","AX/S"]

#polarities = ["negative"]

#batches = ["E","J","L"]

pathBase = "../detection/"

ppm = 20

for polarity in polarities:
    pathPol = pathBase + polarity[:3] + "/"
    peakLists = [pd.read_csv(pathPol+batch+"/peaks.csv") for batch in batches]
    mergedList = mergePeakLists(peakLists,batches,ppm=20,rtTol=.33)
    mergedList.to_csv(pathPol+"merged_peaks.csv")
