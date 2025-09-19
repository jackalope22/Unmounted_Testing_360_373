from icecream import ic
import DMatrix_Analysis_helper as ah
import logging
import pandas as pd
import os
from scipy.signal import find_peaks, peak_widths, peak_prominences
import matplotlib.pyplot as plt
import yaml


log = logging.getLogger(__name__)

class Analysis():

    #is the list of dictionaries that contain information for each pixel.
    allpixels = []
    #these are the numbers of the pixels that are used for a kev360 and kev373 becasue they do not fit a accending pattern
    pixelArray = [124, 127, 125, 123, 2, 4, 6, 0, 122, 121, 119, 12, 10, 8, 14, 
                 1, 112, 113, 111, 109, 16, 20, 18, 11, 100, 107, 101, 24, 26, 28, 30, 25, 88, 
                 89, 87, 83, 38, 40, 42, 39, 72, 77, 79, 56, 54, 52, 50, 51, 68, 73, 71, 75, 
                 62, 60, 58, 53, 64, 69, 67, 65, 59, 61, 57, 55]
    #this is where the config file is stored after it is read in
    loadSettings = {}
    #I find this very confusing but for some reaseon the pixels are backward for the gmids 0 and 1.  I do not know why that is and r and d does not like to help so this is a work around
    #this stores the position of the pixel since they are not in order.  it helps for searching the list of dictionaries
    pixelindex01 = {0: 56, 1: 48, 2: 59, 4: 58, 6: 57, 8: 50, 10: 51, 11: 40, 12: 52, 14: 49, 16: 43, 18: 41, 20: 42, 24: 36, 25: 32, 26: 35, 28: 34,
                    30: 33, 38: 27, 39: 24, 40: 26, 42: 25, 50: 17, 51: 16, 52: 18, 53: 8, 54: 19, 55: 0, 56: 20, 57: 1, 58: 9, 59: 3, 60: 10, 61: 2,
                    62: 11, 64: 7, 65: 4, 67: 5, 68: 15, 69: 6, 71: 13, 72: 23, 73: 14, 75: 12, 77: 22, 79: 21, 83: 28, 87: 29, 88: 31, 89: 30, 100: 39,
                    101: 37, 107: 38, 109: 44, 111: 45, 112: 47, 113: 46, 119: 53, 121: 54, 122: 55, 123: 60, 124: 63, 125: 61, 127: 62}
    
    pixelindex23 = {0: 7, 1: 15, 2: 4, 4: 5, 6: 6, 8: 13, 10: 12, 11: 23, 12: 11, 14: 14, 16: 20, 18: 22, 20: 21, 24: 27, 25: 31, 26: 28, 28: 29,
                    30: 30, 38: 36, 39: 39, 40: 37, 42: 38, 50: 46, 51: 47, 52: 45, 53: 55, 54: 44, 55: 63, 56: 43, 57: 62, 58: 54, 59: 60, 60: 53,
                    61: 61, 62: 52, 64: 56, 65: 59, 67: 58, 68: 48, 69: 57, 71: 50, 72: 40, 73: 49, 75: 51, 77: 41, 79: 42, 83: 35, 87: 34, 88: 32,
                    89: 33, 100: 24, 101: 26, 107: 25, 109: 19, 111: 18, 112: 16, 113: 17, 119: 10, 121: 9, 122: 8, 123: 3, 124: 0, 125: 2, 127: 1}
    #this is a dictionary of lists that store all of the energy values for each pixel
    pixelEnergy = {}
    #list of dead pixels
    deadPixels = []
    #nest dcitionary that stores the number of peaks and there values for each pixel
    pixelPeakData = {}

    def __init__(self, testname, wonumber, specfile, serialnumber):
        #add built in settings as we think of them
        self.testname = testname
        self.specfile = specfile
        self.wonumber = wonumber
        self.serialnumber = serialnumber
        self.min = -0.5
        self.max = 4096.5
        self.channels = 4097
        self.deadThreshold = 500.0
        self.breakdownCount = 50.0
        self.averageOffset = 500.0
        self.averageGain = 6.5
        self.weight = 1.0
        self.breakchannel = 15.0
        self.thresholdfraction = 0.35
        self.peakWindow = 30
        self.fitWidth = 8
        self.eLow = 59.5
        self.eHigh = 122.1
        self.ePPE = 70.0
        self.eWidth = 7.94
        self.channelReductionFactor = 4
        self.fitTypt = "Gaussian"
        self.smoothType = "Savitzy-Golay"
        self.ppethreshold = 35.0
        self.xmin = 500
        self.xmax = 3000
        self.excludefirst = 100
        self.excludelast = 0
        
        self.outputdata = pd.DataFrame()

    
    #this initilizes a list of dictionaries, each dictionary will hold all the values needed for eash pixel
    def initPixelMatrix(self):
        for pixel in Analysis.pixelArray:
            pixel = {"pixel":pixel}
            Analysis.allpixels.append(pixel)
        #ic(Analysis.allpixels)

    #initilize some settings
    def initPixelPassFail(self):
        for pixel in Analysis.allpixels:
            pixel["deadpass"] = True
            pixel["breakdownpass"] = True
            pixel["fwhmpass"] = True
            pixel["gainpass"] = True
            pixel["countspass"] = True
            pixel["shapepass"] = True
            pixel["photopass"] = True

    def initPixelBaseValues(self):
        for pixel in Analysis.allpixels:
            pixel["numberofbins"] = self.channels + 1
            pixel["countbelow"] = 0
            pixel["countover"] = 0
            pixel["countcorrect"] = 0
            pixel["deltax"] = (self.channels + 1) / (self.max - self.min)

    #loop over the binary data file to read in data TODO look at the process file to see how to read in binary data
    def processDataFile(self):
        #path = f"/storage/eV common/Production/Test & Measurement Results/keV-360/Unmounted Data Test/{self.wonumber}/{self.specfile}"
        path = f"/media/evfile01/eV common/Production/Test & Measurement Results/keV-360/Unmounted Data Test/{self.wonumber}/{self.specfile}"
        with open(path, mode="rb") as binaryfile:
            while True:
                testbit = binaryfile.read(1)
                amid = int.from_bytes(testbit, byteorder='big')
                gmid = int.from_bytes(binaryfile.read(1), byteorder='big')
                timestamp = int.from_bytes(binaryfile.read(2), byteorder='big')
                pixelnumber = int.from_bytes(binaryfile.read(2), byteorder='big')
                energy = int.from_bytes(binaryfile.read(2), byteorder='big')
                positive_energy = int.from_bytes(binaryfile.read(1), byteorder='big')
                flag = int.from_bytes(binaryfile.read(1), byteorder='big')
                time_detect = int.from_bytes(binaryfile.read(2), byteorder='big')
                positive_time_detect = int.from_bytes(binaryfile.read(1), byteorder='big')
                #print(f"pixel {pixelnumber}, energy {energy}, time detect {time_detect}")

                if not testbit:
                    break
                elif energy >= self.excludefirst and energy < self.channels - self.excludelast:
                    if pixelnumber in Analysis.pixelArray and (gmid == 0 or gmid == 1):
                        pixelindex = Analysis.pixelindex01
                        entry = Analysis.allpixels[pixelindex[pixelnumber]]
                        if energy < self.min:
                            entry["countbelow"] = entry["countbelow"] + 1
                        elif energy > self.max:
                            entry["countover"] = entry["countover"] + 1
                        else:
                            entry["countcorrect"] = entry["countcorrect"] + 1
                            if str(pixelnumber) not in Analysis.pixelEnergy:
                                Analysis.pixelEnergy[str(pixelnumber)] = []
                                energyOrganizer = (energy - self.min) / entry["deltax"]
                                energyOrganizer = energyOrganizer + self.weight
                                Analysis.pixelEnergy[str(pixelnumber)].append(energyOrganizer)
                            else:
                                energyOrganizer = (energy - self.min) / entry["deltax"]
                                energyOrganizer = energyOrganizer + self.weight
                                Analysis.pixelEnergy[str(pixelnumber)].append(energyOrganizer)
                    else:
                        pixelindex = Analysis.pixelindex23
                        entry = Analysis.allpixels[pixelindex[pixelnumber]]
                        if energy < self.min:
                            entry["countbelow"] = entry["countbelow"] + 1
                        elif energy > self.max:
                            entry["countover"] = entry["countover"] + 1
                        else:
                            entry["countcorrect"] = entry["countcorrect"] + 1
                            if str(pixelnumber) not in Analysis.pixelEnergy:
                                Analysis.pixelEnergy[str(pixelnumber)] = []
                                energyOrganizer = (energy - self.min) / entry["deltax"]
                                energyOrganizer = energyOrganizer + self.weight
                                Analysis.pixelEnergy[str(pixelnumber)].append(energyOrganizer)
                            else:
                                energyOrganizer = (energy - self.min) / entry["deltax"]
                                energyOrganizer = energyOrganizer + self.weight
                                Analysis.pixelEnergy[str(pixelnumber)].append(energyOrganizer)
                else:
                    ic("Could not proceed with pixel number")
                    pass
                
        binaryfile.close()

    def initDataFrame(self):
        templist = []
        for items in Analysis.allpixels:
            dict = items["pixel"], items["countcorrect"]
            templist.append(dict)
        self.outputdata = pd.DataFrame(templist, columns=["Pixel", "Area"])

    def getPassFailDeadBreakdown(self):
        results = []
        for pixel in Analysis.allpixels:
            pixelstring = str(pixel["pixel"])
            #print(f"pixel {pixel} pixelstring {pixelstring}")
            if pixelstring not in Analysis.pixelEnergy:
                print(f"{pixelstring}, Did not have any correct counts")
                pixel["deadpass"] = False
                pixel["breakdownpass"] = False
                Analysis.pixelEnergy[pixelstring] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                Analysis.deadPixels.append(pixel["pixel"])
            else:
                counts = ah.rawArea(self.min, self.channels, pixel["deltax"], Analysis.pixelEnergy[pixelstring])
                printpixel = pixel["pixel"]
                rawarea = counts
                if counts < self.deadThreshold:
                    pixel["deadpass"] = False
                    Analysis.deadPixels.append(pixel["pixel"])
                    print(printpixel, "Did not pass dead test")
                else:
                    value = 0.01 * self.breakchannel * (self.channels +1)
                    counts = 0.0
                    for i in range(int(value)):
                        counts += Analysis.pixelEnergy[pixelstring][i]
                    breakdownfail = 0.01 * self.breakdownCount * rawarea
                    if counts > breakdownfail:
                        pixel["breakdownpass"] = False
                        Analysis.deadPixels.append(pixel["pixel"])
                        print(printpixel, "Did not pass breakdown test")
            passfail = pixel["deadpass"] and pixel["breakdownpass"]
            results.append(passfail)
        self.outputdata.insert(1, "db pass", results, True)

    def smoothData(self, data):
        n = 2
        m = 3
        weightMatrix = []
        for i in range(7):
            weightMatrix.append([])
            for j in range(7):
                weight = ah.savitzkyGolay(n, m, i, j)
                weightMatrix[i].append(weight)
        #ic(weightMatrix)

        length = len(data)
        smoothedData = []
        for p in range(m):
            sumleft = 0.0
            sumright = 0.0
            for q in range(m):
                sumleft += weightMatrix[p][q] * data[q]
                sumright += weightMatrix[2 * m - p][2 * m - q] * data[length - 1 - q]
            smoothedData.insert(p,sumleft)
            smoothedData.insert((length -1 - p),sumright)
        for o in range(m, length - 1 - m):
            sum = 0.0
            for r in range(2 * m + 1):
                sum += weightMatrix[m][r] * data[o + r - m]
            if sum < 0.0:
                smoothedData.insert(o, 0.0)
            else:
                smoothedData.insert(o, sum)
        return smoothedData

    def GetPeaksandPPE(self, spread=4): # use 4 for spread 
        for key, values in Analysis.pixelEnergy.items():
            elow = self.eLow 
            ehigh = self.eHigh 
            eppe = self.ePPE 
            ewidth = self.eWidth
            Analysis.pixelPeakData[key] = {}
            raw_Histogram = ah.createHistogram(values)
            ah.storePlotsPerPixel(raw_Histogram, key, self.serialnumber, self.wonumber, "DAC", "Raw")
            rawpeaks, _ = find_peaks(raw_Histogram, prominence=35)
            #print(f"Raw Peaks {rawpeaks}")
            rawpeakdata, chigh, clow = ah.storePeaks(rawpeaks, raw_Histogram)
            Analysis.pixelPeakData[key]["Max Peak"] = rawpeakdata["Max Peak"]
            gain = (chigh - clow) / (ehigh - elow)
            offset = clow - gain * elow
            if gain == 0.0:
                Analysis.pixelPeakData[key]["Gain"] = gain
                gain = self.averageGain 
            else:
                Analysis.pixelPeakData[key]["Gain"] = gain
            if offset == 0.0:
                Analysis.pixelPeakData[key]["Offset"] = offset
                offset = self.averageOffset
            else:
                Analysis.pixelPeakData[key]["Offset"] = offset
            #print(f"Gain {gain} Offset {offset}")
            
            counts_Histogram = ah.Calibrate(raw_Histogram, gain, offset, self.min, self.max)
            smoothedHistogram = Analysis.smoothData(self, counts_Histogram)

            peaks, _ = find_peaks(smoothedHistogram, prominence=100)
            peakdata, cchigh, cclow = ah.storePeaks(peaks, smoothedHistogram)
            #print(f"smoothed peaks {peaks}")
            halfpeak = peak_widths(smoothedHistogram, peaks, rel_height=.5)
            #print(f"pixel {key} FWHM {fwhm}")
            fullpeak = peak_widths(smoothedHistogram, peaks, rel_height=1)
            ah.storePlotsPerPixel(smoothedHistogram[:150], key, self.serialnumber, self.wonumber, "Energy", "Calibrated", halfpeak, fullpeak)
            if len(halfpeak[0]) == 0:
                Analysis.pixelPeakData[key]["FWHM"] = 0.0
            elif len(halfpeak[0]) == 1:
                if cchigh == 0.0:
                    cchigh = cclow
                    if cclow == 0.0:
                        cchigh = 1.0
                calfwhm = 100 * (halfpeak[0][0] / cchigh)
                Analysis.pixelPeakData[key]["FWHM"] = calfwhm
            else:
                if cchigh == 0.0:
                    cchigh = cclow
                    if cclow == 0.0:
                        cchigh = 1.0
                calfwhm = 100 * (halfpeak[0][1] / cchigh)
                Analysis.pixelPeakData[key]["FWHM"] = calfwhm

            print(f"pixel {key} completed")
            if len(fullpeak[2]) < 2:
                Analysis.pixelPeakData[key]["PPE"] = 0.0
                Analysis.pixelPeakData[key]["Peak Area"] = 0.0
                continue
            #print(fullpeak)
            ppeMax = cchigh
            cppe = self.averageGain * eppe + self.averageOffset
            #print(f"ppeMax {ppeMax} cppe {cppe}")
            if ppeMax < cppe:
                Analysis.pixelPeakData[key]["PPE"] = 0.0
                Analysis.pixelPeakData[key]["Peak Area"] = 0.0
            delta = ewidth / ehigh
            upper = ehigh * (1.0 + delta)
            if upper > eppe:
                peakarea = ah.integrateone(fullpeak[2][0], fullpeak[3][0], 4097, -0.5, 4096.5, smoothedHistogram)
                #print(f"peakarea {peakarea}")
                Analysis.pixelPeakData[key]["Peak Area"] = peakarea
                if peakarea <= 0.0:
                    PPE = 0.0
                    Analysis.pixelPeakData[key]["PPE"] = PPE
                else:
                    PPE = 100.0 * peakarea / ah.integrateone(7.94, 70.0, 4097, -0.5, 4096.5, smoothedHistogram)
                    #PPE = 100.0 * peakarea / ah.integratetwo(0, 30, counts_Histogram)
                    #print(f"PPE {PPE}\n")
                    Analysis.pixelPeakData[key]["PPE"] = PPE
            else:
                Analysis.pixelPeakData[key]["PPE"] = 0.0
                Analysis.pixelPeakData[key]["Peak Area"] = 0.0

    def updateDataFramePeakData(self):
        fwhmlist = []
        ppelist = []
        offsetlist = []
        gainlist = []
        maxpeaklist = []
        peakarea = []
        pixels = self.outputdata["Pixel"].tolist()
        #print(pixels)
        for pixelnumber in pixels:
            for key, value in Analysis.pixelPeakData.items():
                if key == str(pixelnumber):
                    fwhmlist.append(Analysis.pixelPeakData[str(pixelnumber)]["FWHM"])
                    ppelist.append(Analysis.pixelPeakData[str(pixelnumber)]["PPE"])
                    offsetlist.append(Analysis.pixelPeakData[str(pixelnumber)]["Offset"])
                    gainlist.append(Analysis.pixelPeakData[str(pixelnumber)]["Gain"])
                    maxpeaklist.append(Analysis.pixelPeakData[str(pixelnumber)]["Max Peak"])
                    peakarea.append(Analysis.pixelPeakData[str(pixelnumber)]["Peak Area"])

        self.outputdata.insert(3, "FWHM", fwhmlist, True)
        self.outputdata.insert(4, "PPE", ppelist, True)
        self.outputdata.insert(5, "Offset", offsetlist, True)
        self.outputdata.insert(6, "Gain", gainlist, True)
        self.outputdata.insert(7, "Max Peak", maxpeaklist, True)
        self.outputdata.insert(8, "Peak Area", peakarea, True)

    def outputCSVFile(self):
        path = f"/media/evfile01/eV common/Production/Test & Measurement Results/keV-360/Unmounted Data Test/{self.wonumber}/{self.serialnumber}"
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            print("new directory created for csv output file")
        
        self.outputdata.to_csv(f"{path}/{self.serialnumber}.csv")

    def outputSettingsYamlFile(self):
        path = f"/media/evfile01/eV common/Production/Test & Measurement Results/keV-360/Unmounted Data Test/{self.wonumber}/{self.serialnumber}"
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            print("new directory created for settings meta file")

        metafile = {}
        metafile["Test Name"] = self.testname
        metafile["Binary File"] = self.specfile
        metafile["WO Number"] = self.wonumber
        metafile["Serial Number"] = self.serialnumber
        metafile["Min"] = self.min
        metafile["Max"] = self.max
        metafile["Channels"] = self.channels
        metafile["Dead Threshold"] = self.deadThreshold
        metafile["Breakdown Count"] = self.breakdownCount
        metafile["Average Offset"] = self.averageOffset
        metafile["Average Gain"] = self.averageGain
        metafile["Weight"] = self.weight
        metafile["Break Channel"] = self.breakchannel
        metafile["Threshold Fraction"] = self.thresholdfraction
        metafile["Peak Window"] = self.peakWindow
        metafile["Fit Width"] = self.fitWidth
        metafile["E Low"] = self.eLow
        metafile["E High"] = self.eHigh
        metafile["E PPE"] = self.ePPE
        metafile["E Width"] = self.eWidth
        metafile["Channel Reduction Factor"] = self.channelReductionFactor
        metafile["Fit Type"] = self.fitTypt
        metafile["Smooth Type"] = self.smoothType
        metafile["PPE Threshold"] = self.ppethreshold
        metafile["X Min"] = self.xmin
        metafile["X Max"] = self.xmax
        metafile["Exclude First"] = self.excludefirst
        metafile["Exclude Last"] = self.excludelast

        
        with open(f"{path}/{self.serialnumber}_meta.yaml", "w") as yamlfile:
            yaml.dump(metafile, yamlfile, sort_keys=False)
        
        yamlfile.close()


    def operationComplete(self):
        print("Analysis Complete")


    def printPixelExampleOne(self):
        #ic(Analysis.allpixels)
        for item in Analysis.allpixels:
            if item["pixel"] == 119:
                print(item)

    def printPixelExampleTwo(self):
        for item in Analysis.allpixels:
            if item["pixel"] == 20:
                print(item)
    
    def printPixelEnergyEntry(self):
        for item in Analysis.pixelEnergy:
            if item == "119":
                print(Analysis.pixelEnergy[item])
                #print(len(Analysis.pixelEnergy[item]))
    
    def printDeadPixels(self):
        print(Analysis.deadPixels)

    def printallpixels(self):
        for item in Analysis.allpixels:
            print(item["pixel"], item["countcorrect"])
        
    def printdataframe(self):
        print(self.outputdata)
    
    def printPixelSmoothedDataWeight(self):
        ic(Analysis.pixelSmoothingWeight)
        ic(Analysis.pixelSmoothingWeight[3])

    def printSmoothedEnergy(self):
        for item in Analysis.smoothedPixelEnergy:
            if item == "119":
                print(Analysis.smoothedPixelEnergy[item])

    def plotOriginalData(self):
        for item in Analysis.pixelEnergy:
            if item == "124":
                fig = plt.figure() 
                axs1 = fig.add_subplot(2, 1, 1)
                axs2 = fig.add_subplot(2, 1, 2)
                axs1.hist(Analysis.pixelEnergy[item], bins=200)
                axs2.hist(Analysis.smoothedPixelEnergy[item], bins=120)
                plt.show()

    def printPixelPeakData(self):
        for item in Analysis.pixelPeakData:
            if item == "55":
                print(Analysis.pixelPeakData[item])

        
a = Analysis("test", "00000", "43979-01.dat", "43979-01")
a.initPixelMatrix()
a.initPixelPassFail()
a.initPixelBaseValues()
a.processDataFile()
a.initDataFrame()
a.getPassFailDeadBreakdown()
#a.printPixelExampleOne()
#a.printPixelExampleTwo()
#a.printPixelEnergyEntry()
#a.printDeadPixels()
#a.printallpixels()
#a.printPixelSmoothedDataWeight()
#a.printSmoothedEnergy()
#a.plotOriginalData()
a.GetPeaksandPPE()
#a.printPixelPeakData()
a.updateDataFramePeakData()
#a.printdataframe()
a.outputCSVFile()
a.outputSettingsYamlFile()
a.operationComplete()


