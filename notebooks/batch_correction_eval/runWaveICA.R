library(devtools)
devtools::install_github("dengkuistat/WaveICA_2.0",host="https://api.github.com")
library(WaveICA2.0)
library(dplyr)

setwd("X:/LLFS/letter/ES_plotting_analysis")

data = read.csv("data/peak_areas_lipid_pos_imputted_rel.csv")

info = data[,1:1]

ints = log2(data[,2:ncol(data)])

originalOrder = colnames(ints)

metadata = read.csv("data/batch_info_lipid_pos_rel.csv")

metadata_sorted = metadata[order(metadata$sample.order),]

metadata_sorted = metadata_sorted[metadata_sorted$peak.area.sample.name %in% as.list(originalOrder),]

data_t = as.data.frame(t(ints))

data_t = data_t[metadata_sorted$peak.area.sample.name,]

runOrder = c(1:length(data_t))

data_t = as.data.frame(t(data_t))

norm = WaveICA_2.0(data_t,Injection_Order = runOrder,alpha = 0,Cutoff = 0.1,K=10)

ints_norm = norm$data_wave

ints_norm = as.data.frame(ints_norm[,originalOrder])

output = as.data.frame(cbind(info,ints_norm))

write.csv(output,"data/peak_areas_lipid_pos_imputted_rel_waveICA_normalized.csv")
