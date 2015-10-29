# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 22:32:19 2015


"""
import numpy as np
import math
#A is a header Raman Shift data (X-Axis) B is heade for Raman Intensity data(Y-Axis)
#Example of how to access data, float changes it string to float
#Example = float(pureComponentData[9][990]['A'])
#Example2 = float(sampleMixtureData[9]['A'])

def specdata(scan):
    x1 = []
    y1 = []
    index_array = np.arange(len(scan))
    for dex in index_array:
        #A is Raman Shift(X-Axis) B is Raman Intensity(Y-Axis)
        x1.append(float(scan[dex]['A']))
        y1.append(float(scan[dex]['B']))
    return x1, y1

def compare(raman1, raman2):
    [x1, y1] = specdata(raman1)
    [x2, y2] = specdata(raman2)
    #The minimum x for comparison is the largest of the two min x's being compared.
    #The maximum x for comparison is the smallest of the two max x's being compared.
        
    x_start = max(x1[0], x2[0])
    x_final = min(x1[len(x1) - 1], x2[len(x1) - 1])
    
    x_new = np.arange(x_start, x_final, 1)
    y_new1 = []
    y_new2 = []
    a1 = 0
    b1 = 0
    a2 = 0;
    b2 = 0;
    
    for new in range(0, len(x_new)):
        for x in range(0, len(x1)):
            if x1[x] <= x_new[new]:
                a1 = x
            if x1[x] >= x_new[new]:
                b1 = x
                break
        for x in range(0, len(x2)):
            if x2[x] <= x_new[new]:
                a2 = x
            if x2[x] >= x_new[new]:
                b2 = x
                break
        #interpolate
        y_new1.append(y1[a1]+ (y1[b1] - y1[a1]) * (x_new[new] - x1[a1])/(x1[b1] - x1[a1])) 
        y_new2.append(y2[a2]+ (y2[b2] - y2[a2]) * (x_new[new] - x2[a2])/(x2[b2] - x2[a2]))
    
    return x_new, y_new1, y_new2

#superposition ysuper = i*y1+j*y2. Ex. ysuper= .75*y1+.25*y2
def superposition(raman1, raman2, i, j):
    [x_super, ynew1, ynew2] = compare(raman1, raman2)
    y_super = []
    for sup in range(0, len(x_super)):        
        y_super.append(i * ynew1[sup] + j * ynew2[sup])
        
    return x_super, y_super
    
def reduce(ramanPure, ramanMix):
    [x_red, yPure, yMix] = compare(ramanPure, ramanMix)
    y_red = []
    for red in range(0, len(x_red)):        
        y_red.append(yMix[red] - yPure[red])
        
    return x_red, y_red
    
def normalizer(ramanIntensity):
    s = np.array(ramanIntensity)
    maxRaman = np.nanmax(s)
    minRaman = np.nanmin(s)
    normie = 0
    normRaman = []
    for raman in range(0, len(ramanIntensity)):
        normie = (ramanIntensity[raman] - minRaman)/(maxRaman - minRaman)
        normRaman.append(normie)
    return normRaman

def normCompare(pureRaman, mixRaman):
    [xcom, ycomPure, ycomMix] = compare(pureRaman, mixRaman)
    ynormPure = normalizer(ycomPure)
    ynormMix = normalizer(ycomMix)
    return xcom, ynormPure, ynormMix

def euclidean(pureRaman, mixRaman):
    #x = float('nan')
    sqdist = 0
    #weight = (1-.999)/.999
    weight = 1
    [xcom, ynormPure, ynormMix] = normCompare(pureRaman, mixRaman)
    for point in range(0, len(xcom)):
        dist = math.pow((ynormMix[point] - ynormPure[point]), 2)
        if (math.isnan(dist) == True):
            dist = 0
        elif (ynormPure[point] > ynormMix[point] and ynormMix[point] != 0) :
            dist = weight * dist
        elif (ynormPure[point] > ynormMix[point] and ynormMix[point] == 0) :
            dist = dist / weight
        else:
            dist = dist
        sqdist = sqdist + dist
    
    weightEuclid = math.sqrt(sqdist)
    return weightEuclid

def cityblock(pureRaman, mixRaman):
    [xcom, ynormPure, ynormMix] = normCompare(pureRaman, mixRaman)
    blocky = 0
    for point in range(0, len(xcom)):
        dist = abs(ynormMix[point] - ynormPure[point])
        if (math.isnan(dist) == True):
            dist = 0
        blocky = blocky + dist
    return blocky

def cosiner(pureRaman, mixRaman):
    [xcom, ynormPure, ynormMix] = normCompare(pureRaman, mixRaman)
    cosin = 0
    pureSum = 0
    mixSum = 0
    multSum = 0
    for point in range(0, len(xcom)):
        mixSumPart = math.pow(ynormMix[point],2)
        pureSumPart = math.pow(ynormPure[point],2)
        multSumPart = ynormMix[point] * ynormPure[point]
        if (math.isnan(mixSumPart) == True or math.isnan(pureSumPart) == True or math.isnan(pureSumPart)):
              mixSumPart = 0
              pureSumPart = 0
              multSumPart = 0
        pureSum = pureSum + pureSumPart
        mixSum = mixSum + mixSumPart
        multSum = multSum + multSumPart
    cosin = multSum / (math.sqrt(pureSum) * math.sqrt(mixSum))
    return cosin

def correlationPearson(pureRaman, mixRaman):
    [xcom, ynormPure, ynormMix] = normCompare(pureRaman, mixRaman)
    n = len(xcom)
    topSum = 0
    bottomMix = 0
    bottomPure = 0
    correlation = 0
    yPure = np.array(ynormPure)
    yMix = np.array(ynormMix)
    meanMix = np.nanmean(yMix)
    meanPure = np.nanmean(yPure)
    for point in range(0, len(xcom)):
        topSumPart = (ynormMix[point] * ynormPure[point]) 
        bottomMixPart = math.pow(ynormMix[point],2) 
        bottomPurePart = math.pow(ynormPure[point],2) 
        if (math.isnan(topSumPart) == True or math.isnan(bottomMixPart) == True or math.isnan(bottomPurePart)):
              topSumPart = 0
              bottomMixPart = 0
              bottomPurePart = 0
        topSum = topSum + topSumPart
        bottomMix = bottomMix + bottomMixPart
        bottomPure = bottomPure + bottomPurePart
    correlation = (topSum - (n * meanMix * meanPure))/ (math.sqrt(bottomMix- (n * math.pow(meanMix,2))) * math.sqrt(bottomPure- (n * math.pow(meanPure,2)))) 
    return correlation    
    
def euclideanAll(pureList, pureCompData, mixData):
    metric = []
    smallest = 0;
    for x in range(0, len(pureList)):
        #finf euclidean metric for each pure spectrum compared to mixture
        metric.append(euclidean(pureCompData[x], mixData))
        #index with smallest euclidean metric    
        if (metric[x] < metric[smallest]):
            smallest = x
    return smallest
 
def cityblockAll(pureList, pureCompData, mixData):
    metric = []
    smallest = 0;
    for x in range(0, len(pureList)):
        #find cityblock metric for each pure spectrum compared to mixture
        metric.append(cityblock(pureCompData[x], mixData))
        #index with smallest metric  
        if (metric[x] < metric[smallest]):
            smallest = x
    return smallest

def cosinerAll(pureList, pureCompData, mixData):
    metric = []
    largest = 0;
    for x in range(0, len(pureList)):
        #find cosine similarity for each pure spectrum compared to mixture
        metric.append(cosiner(pureCompData[x], mixData))
        #index with slargest metric  
        if (metric[x] > metric[largest]):
            largest = x
    return largest
    
def pearsonAll(pureList, pureCompData, mixData):
    metric = []
    largest = 0;
    for x in range(0, len(pureList)):
        #find cosine similarity for each pure spectrum compared to mixture
        metric.append(correlationPearson(pureCompData[x], mixData))
        #index with largest coefficient
        if (metric[x] > metric[largest]):
            largest = x
    return largest

