import sys
import os
#sys.path.append("../src/")

from detection_helper import *

polarity= "positive"

batches = ["E","J","L","N","Q","R"]

#polarities = ["negative"]

#batches = ["L"]

#pathBase = "../detection/"

ppm = 20

path = "../data/peak_picking_data_batchA/"

#run xcms (centwave, camera)
#os.system("Rscript find_peaks.R " + path + " " + polarity + " " + str(ppm))

#load xcms output
peakList = PeakList()
peakList.readXCMSPeakList(path + "peaks_xcms.csv")

peakList.to_csv(path + "peaks_f1.csv")


#filter for adducts and isotopes
peakList.filterAdductsIsotopes(adductsToKeep = ["[M+H]","[M+H+NH3]","[M+Na]"])

peakList.to_csv(path + "peaks_f2.csv")

#perform backgroun subtraction
peakList.backgroundSubtract("lank","atch",factor=3)

#write results
peakList.to_csv(path + "peaks.csv")

print(peakList.peakList)