import matplotlib.pyplot as plt
import os
from scipy.signal import find_peaks, peak_widths

# This file contains helper functions for the DMatrix_Analysis.py file

def rawArea(min, channels, deltax, pixeldict):
    lower = (0 - min) / deltax
    upper = (channels - min) / deltax
    sum = 0
    for i in range(int(lower), int(upper)):
        sum += pixeldict[i]
    return sum

def genFact(a, b):
    gf = 1
    for j in range(a - b + 1, a+1):
        gf *= j
    return gf

def gramPoly(i, mm, k, s):
    gp = 0.0
    if k > 0:
        gramPoly1 = gramPoly(i, mm, k - 1, s)
        gramPoly2 = gramPoly(i, mm, k - 1, s - 1)
        gramPoly3 = gramPoly(i, mm, k - 2, s)
        gp = (4 * k - 2) * (i * gramPoly1 + s * gramPoly2) - ((k - 1) * (2 * mm + k)) * gramPoly3
        gp /= (k * (2 * mm - k + 1))
    elif k == 0 and s == 0:
        gp = 1.0
    else:
        gp = 0.0
    return gp

def getWeight(i, t, mm, n, s):
    sum = 0.0
    for k in range(n+1):
        genfact1 = genFact(2 * mm, k)
        grampoly1 = gramPoly(i, mm, k, 0)
        grampoly2 = gramPoly(t, mm, k, s)
        genfact2 = genFact(2 * mm + k + 1, k + 1)
        sum += ((2 * k + 1) * genfact1) * grampoly1 * grampoly2 / genfact2
    return sum

def savitzkyGolay(n, m, k, l):
    i = k - m
    t = l - m
    a = getWeight(i, t, m, n, 0)
    return a


def createHistogram(data):
    histogram = [0] * 4097
    for j in data:
        histogram[int(j)] += 1
    
    return histogram

def reduceBinsHistogram(data, xmin, xmax, nobins):
    deltax = nobins / (xmax - xmin)
    channelreduction = 1024
    tdelta = channelreduction / (xmax - xmin)
    newhistogram = [0] * channelreduction
    for i in range(nobins):
        x = xmin + (i + 0.5) / deltax
        j = int((x - xmin) * tdelta)
        y = data[i] * deltax
        newhistogram[j] = newhistogram[j] + y
    return newhistogram

def Calibrate(data, gain, offset, mindac, maxdac):
    newmin = (mindac - offset) / gain
    newmax = (maxdac - offset) / gain
    numberofbins = 4097
    deltax = numberofbins / (newmax - newmin)
    newhistogram = [0] * numberofbins
    #print(f"newmin {newmin} newmax {newmax} deltax {deltax}")
    for i in range(numberofbins - 1):
        x = newmin + (i + 0.5) / deltax
        j = (x - offset) / gain
        k = (j - newmin) * deltax
        if j < newmin:
            continue
        elif j > newmax:
            continue
        else:
            newhistogram[int(k)] = newhistogram[int(k)] + data[i]
    return newhistogram



def integrateone(xmin, xmax, numberofCounts, xMin, xMax, data):
    deltax = numberofCounts / (xMax - xMin)
    lower = (xmin - xMin) * deltax
    upper = (xmax - xMin) * deltax
    sum = integratetwo(lower, upper, data)
    return sum

def integratetwo(lower, upper, data):
    sum = 0.0
    if len(data) < lower:
        return sum
    elif len(data) >= upper:
        for i in range(int(lower), int(upper)-1):
            sum += data[i]
    elif len(data) < upper:
        for i in range(int(lower), len(data)-1):
            sum += data[i]
    return sum


def storePlotsPerPixel(histogram, pixel, serialnumber, wonumber, label1, plottype, peaktype1=None, peaktype2=None):
    path = f"/media/evfile01/eV common/Production/Test & Measurement Results/keV-360/Unmounted Data Test/{wonumber}/{serialnumber}/plots"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        print("new directory created")
    
    
    plt.plot(histogram)
    plt.xlabel(label1)
    plt.ylabel("Number of Counts")
    plt.title(f"Pixel {pixel}")
    if peaktype1 != None:
        plt.hlines(*peaktype2[1:], color="C3")
    if peaktype2 != None:
        plt.hlines(*peaktype1[1:], color="C2")
    plt.savefig(path + f"/Pixel_{pixel}_{plottype}.png")
    plt.close()
    plt.clf()

def makeGroups(bin):
    group1 = []
    group2 = []
    transition = False
    for i in range(len(bin) - 1):
        if bin[i+1] - bin[i] < 30:
            if transition == False:
                group1.append(bin[i])
            else:
                group2.append(bin[i+1])
        elif bin[i+1] - bin[i] > 30:
            if transition == False:
                group1.append(bin[i])
                group2.append(bin[i+1])
                transition = True
    return group1, group2

def storePeaks(peaks, histogram):
    peakdata = {}
    length = len(peaks)
    if length > 0:
        peakdata["Number_of_peaks"] = length
        index = 1
        for p in peaks:
            peakdata[f"Peak_{index}"] = histogram[p]
            index += 1
    else:
        peakdata["Number_of_peaks"] = 0
        peakdata["Max Peak"] = 0
        return peakdata, 0.0, 0.0
    if length == 2:
        chigh = float(peaks[1])
        clow = float(peaks[0])
        peakdata["Max Peak"] = peaks[1]
        return peakdata, chigh, clow
    elif length == 3:
        lowergroup, uppergroup = makeGroups(peaks)
        if len(lowergroup) > 1:
            lowermax = max(lowergroup)
        else:
            lowermax = lowergroup[0]
        if len(uppergroup) > 1:
            uppermax = max(uppergroup)
        else:
            uppermax = uppergroup[0]

        chigh = float(uppermax)
        clow = float(lowermax)
        peakdata["Max Peak"] = uppermax
        return peakdata, chigh, clow
    elif length >= 4:
        lowergroup, uppergroup = makeGroups(peaks)
        if len(lowergroup) > 1:
            lowermax = max(lowergroup)
        else:
            lowermax = lowergroup[0]
        if len(uppergroup) > 1:
            uppermax = max(uppergroup)
        else:
            uppermax = uppergroup[0]
            
        chigh = float(uppermax)
        clow = float(lowermax)
        peakdata["Max Peak"] = uppermax
        return peakdata, chigh, clow
    else:
        chigh = 0.0
        clow = 0.0
        peakdata["Max Peak"] = max(peaks)
        return peakdata, chigh, clow

