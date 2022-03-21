
setwd("X:/LLFS/letter/ES_plotting_analysis")
source("EigenMS/EigenMS/EigenMS.R")

data = read.csv("data/peak_areas_lipid_pos_imputted_rel.csv")

info = data[,c(1,1)]

ints = log2(data[,2:ncol(data)])

grps = as.factor(rep(1,ncol(ints)))

m_ints_eig1 = eig_norm1(m=ints,treatment=grps,prot.info=info)
m_ints_norm1 = eig_norm2(rv=m_ints_eig1) 
write.csv(m_ints_norm1$normalized,"data/peak_areas_lipid_pos_imputted_rel_eigen_ms_normalized.csv")
