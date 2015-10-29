# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 20:11:11 2015

"""
import databringer
import specanalysis


dname = 'Pure Components' #Name of your folder for pure Component xlsx files
pureComponentData = databringer.fileloop(dname)#loops through folder to import pure component data
pureComponentList = databringer.filenamer(dname)#creates list of pure components from folder names
mixedFolderName = "Sample Mixtures/.....xlsx"
sampleMixtureData =  databringer.xlsx(mixedFolderName)#brings in data of sample to analayze


#Examples
pureRaman1 = pureComponentData[0]
pureRaman2 = pureComponentData[1]
mixRaman = sampleMixtureData


#[xsuper, ysuper] = specanalysis.superposition(pureRaman1,pureRaman2,.9999,.0001)
[xcom, ycom1, ycom2] = specanalysis.compare(pureRaman1, pureRaman2)
ynorm1 = specanalysis.normalizer(ycom1)


oxidizer = specanalysis.pearsonAll(pureComponentList, pureRaman1,mixRaman)



