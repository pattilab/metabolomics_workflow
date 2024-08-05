from DecoID.DecoID import DecoID
import sys

#sets database to use
libFile = "MoNA_mzCloud_reference.db"

#mzCloud key if necessary
key = "none"
mzCloudLib = "reference"

#number of parallel processes to use
numCores = 8

#filename of query MS/MS data
file = sys.argv[1]

#filename of peak list
peakFile = "../detection/neg/merged_peaks.csv"

#set parameters
usePeaks = True
DDA = True #data is DDA
massAcc = 30 #ppm tolerance
fragThresh= 0.01 #require non-zero dot product threshold
offset = .75 #half of isolation window width. Only for non-thermo data
useIso = True #use predicted M+1 isotopolgoue spectra
threshold = 0 #minimum dot product for reporting
lam = 5.0 #LASSO parameter
rtTol = float("inf") #retention time tolerance for database, inf means ignore RT
fragCutoff = 1000 #intensity threshold for MS/MS peaks


if __name__ == '__main__':

    #create DecoID object
    decID = DecoID(libFile, mzCloudLib, numCores,api_key=key)

    #read in data
    decID.readData(file, 2, usePeaks, DDA, massAcc,offset,peakDefinitions=peakFile,frag_cutoff=fragCutoff)

    #identify unknowns compounds for on-the-fly unknown library
    decID.identifyUnknowns(iso=useIso,rtTol=rtTol,dpThresh=80,resPenalty=lam)

    #search spectra
    decID.searchSpectra("y", lam , fragThresh, useIso, threshold,rtTol=rtTol)
