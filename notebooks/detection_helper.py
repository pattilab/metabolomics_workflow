import numpy as np
import pandas as pd


class PeakList():
    def __init__(self,peakList = None):
        if type(peakList) == type(None):
            self.peakList = pd.DataFrame()
        else:
            self.peakList = peakList
            
    def from_csv(self,fn):
        self.peakList = pd.read_csv(fn)
        self.sampleCols = [x for x in self.peakList.columns.values if x not in ["mz","rt_start","rt_end","isotope","adduct","peak group"]] 
        
    def to_csv(self,fn):
        self.peakList.to_csv(fn)
        
    def readXCMSPeakList(self,filename,key=".mzML"):
        data = pd.read_csv(filename,index_col=0)
        data_form = {}
        self.sampleCols = [x for x in data.columns.values if key in x]
        for col in self.sampleCols:
            data[col] = data[col].fillna(0)
        for index,row in data.iterrows():
            data_form[index] = {"mz":row["mz"],"rt_start":row["rtmin"]/60,"rt_end":row["rtmax"]/60,"isotope":row["isotopes"],"adduct":row["adduct"],"peak group":row["pcgroup"]}
            for col in self.sampleCols:
               data_form[index][col] = row[col]
               
        self.peakList = pd.DataFrame.from_dict(data_form,orient="index")
        
    def filterAdductsIsotopes(self,adductsToKeep = ["[M+H]","[M-H]","[M+H+NH3]","[M+Na]"],isotopesToKeep = ["[M]"]):
        goodRows = []
        for index,row in self.peakList.iterrows():
            if (pd.isna(row["adduct"]) or any(x in row["adduct"] for x in adductsToKeep)) and (pd.isna(row["isotope"]) or any(x in row["isotope"] for x in isotopesToKeep)):
                goodRows.append(index)
        self.peakList = self.peakList.loc[goodRows,:]
        
    def backgroundSubtract(self,blank_key,sample_key,factor=3):
        goodRows = []
        blankCols = [x for x in self.sampleCols if blank_key in x]
        sampleCols = [x for x in self.sampleCols if sample_key in x and x not in blankCols]
        for index,row in self.peakList.iterrows():
            blankInt = np.mean(row[blankCols])
            sampleInt = np.mean(row[sampleCols])
            if sampleInt >= factor * blankInt:
                goodRows.append(index)
                
        self.peakList = self.peakList.loc[goodRows,:]
        

def compareRT(feat1,feat2,rtTol):

    rt1 = np.mean([feat1["rt_start"],feat1["rt_end"]])
    rt2 = np.mean([feat2["rt_start"],feat2["rt_end"]])
    
    if np.abs(rt1-rt2) < rtTol:
        return True
        
    return False

def mergePeakLists(peakLists,names,ppm=20,rtTol=.5):
    peakLists = [x[["mz","rt_start","rt_end"]].reset_index() for x in peakLists]
    mergedList = pd.DataFrame()
    peakFounders = {n:{} for n in names}

    for x,n in zip(peakLists,names):
        for index,row in x.iterrows():
            new = True
            mz_bounds = [row["mz"] - ppm*row["mz"]/1e6,row["mz"] + ppm*row["mz"]/1e6]
            if len(mergedList) > 0:
                filt = mergedList[(mergedList["mz"] > mz_bounds[0]) & (mergedList["mz"] < mz_bounds[1])]            
                for index2,row2 in filt.iterrows():
                    if compareRT(row,row2,rtTol):
                        new = False
                        peakFounders[n][index2] = 1 
                        break
            if new:
                ind = len(mergedList)
                mergedList = pd.concat((mergedList,x.iloc[index:index+1,:]),axis=0,ignore_index=True)
                for n2 in names:
                    peakFounders[n2][ind] = 0
                peakFounders[n][ind] = 1
                
      
                            
    peakFounders = pd.DataFrame.from_dict(peakFounders,orient="index").transpose()
    mergedList = pd.concat((mergedList,peakFounders),axis=1,ignore_index=False)
    return mergedList
            
        
        
        
                
        
    
     
        