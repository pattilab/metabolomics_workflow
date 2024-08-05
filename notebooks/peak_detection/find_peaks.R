library("xcms")
library("CAMERA")

args = commandArgs(trailingOnly=TRUE)

pathData <- args[1] #path to your .mzML 
charge <- args[2]
ppm <- as.numeric(args[3])

setwd(pathData)
files = list.files(pattern = "*.mzML")
numFiles = length(files)

xs = readMSData(files,mode="onDisk",msLevel=1)

params <- CentWaveParam(ppm = ppm, peakwidth = c(3, 20))
xs2 <- findChromPeaks(xs,params,return.type="XCMSnExp")

pdp <- PeakDensityParam(sampleGroups = rep(1,numFiles),
                        minFraction = 1/numFiles,bw=2)

xs2 = groupChromPeaks(xs2,param=pdp)

xs3= fillChromPeaks(xs2)

xs4 = as(xs3, "xcmsSet")

ann = annotate(xs4,polarity=charge,maxcharge=2,ppm=ppm)

peaks = getPeaklist(ann)

write.csv(peaks,"peaks_xcms.csv")
       