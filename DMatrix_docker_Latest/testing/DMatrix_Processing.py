import DMatrix_internal as dm
import DMatrix_INTERNALAPI_Aliases as wrap
import DMatrix_Util as util
import logging
import time
from ctypes import POINTER, CFUNCTYPE, c_void_p
from collections import defaultdict
import os
import pandas as pd
import csv

log = logging.getLogger(__name__)

binarydata1 = []
binarydata2 = []
binarydata3 = []
binarydata4 = []
 
def dataCallback(pixelData : POINTER(dm.DMatrixData), userData: c_void_p):
   
    global binarydata1
    global binarydata2
    global binarydata3
    global binarydata4

    if pixelData[0].GMID == 0:
        binarydata1.append([pixelData[0].AMID, pixelData[0].GMID, pixelData[0].Timestamp, pixelData[0].PixelNumber, 
        pixelData[0].Energy, pixelData[0].EnergyPosEvent, pixelData[0].ExceededThreshold, pixelData[0].TimeDetect, 
        pixelData[0].TimeDetectPosEvent])
    elif pixelData[0].GMID == 1:
        binarydata2.append([pixelData[0].AMID, pixelData[0].GMID, pixelData[0].Timestamp, pixelData[0].PixelNumber, 
        pixelData[0].Energy, pixelData[0].EnergyPosEvent, pixelData[0].ExceededThreshold, pixelData[0].TimeDetect, 
        pixelData[0].TimeDetectPosEvent])
    elif pixelData[0].GMID == 2:
        binarydata3.append([pixelData[0].AMID, pixelData[0].GMID, pixelData[0].Timestamp, pixelData[0].PixelNumber, 
        pixelData[0].Energy, pixelData[0].EnergyPosEvent, pixelData[0].ExceededThreshold, pixelData[0].TimeDetect, 
        pixelData[0].TimeDetectPosEvent])
    elif pixelData[0].GMID == 3:
        binarydata4.append([pixelData[0].AMID, pixelData[0].GMID, pixelData[0].Timestamp, pixelData[0].PixelNumber, 
        pixelData[0].Energy, pixelData[0].EnergyPosEvent, pixelData[0].ExceededThreshold, pixelData[0].TimeDetect, 
        pixelData[0].TimeDetectPosEvent])

    dataReceived = None

def set_data_recvd_callback(callback_func):
    global dataReceived

    DATA_RECEIVED_FN = CFUNCTYPE(None, POINTER(dm.DMatrixData), c_void_p)
    dataReceived = dm.wrap.data_recvd_function(callback_func)
    wrap.LIB.api_set_dataRecvdCallback(dataReceived,0)

def SetDataCallback():
    set_data_recvd_callback(dataCallback)

def collect_and_get_counts(collectTime):
    dm.sys_resetFrameCounts()
    count = 0
#def collect_and_get_counts(accum_steps, n_frames, threshold, numpfbs):
    # 400*250 us = 100 ms
    # xr2_write_RGA(11, hex(accum_steps << 16))
    # standard_time = .1  # This is empirical
    #standard_time = 3 * 250E-6 * max(accum_steps , 4)  # 3 times the integration time, with minimum of 10 ms.
    collectAllLists = []
    #pfbs = [pfb0, pfb1, pfb2, pfb3, pfb4, pfb5]
    SetDataCallback()
    dm.collect_setCollectionDelay(100)
    dm.collect_start()
    time.sleep(collectTime)
    while count < collectTime:
        dm.api_processEvents()
        count += 1
    dm.collect_stop()

    #for lists in range(numpfbs):
        #collectAllLists.append(pfbs[lists])
    #convertAndStoreData(collectAllLists, n_frames, numpfbs)
def convertData(wonumber, serialnums, testtype):
    global binarydata1
    global binarydata2
    global binarydata3
    global binarydata4

    log.info(serialnums)
    print("Writing data to Storage")
    log.info("Writing data to Storage")
    # print("Writing csv files")
    # log.info("Writing csv files")
    # print("Writing csv file for GM0")
    # createCSV(binarydata1, 0, wonumber)
    # print("Writing csv file for GM1")
    # createCSV(binarydata2, 1, wonumber)
    # print("writing csv file for GM2")
    # createCSV(binarydata3, 2, wonumber)
    # print("Writing csv file for GM3")
    # createCSV(binarydata4, 3, wonumber)
    print("Writing binary files")
    log.info("Writing binary files")
    if serialnums[0] != "":
        print("Saving binary file for GM0")
        log.info("Saving binary file for GM0")
        createBinary(binarydata1, 0, wonumber, serialnums[0], testtype)
    else:
        print("GM0 not needed, no data saved")
        log.info("GM0 not needed, no data saved")
    if serialnums[1] != "":
        print("Saving binary file for GM1")
        log.info("Saving binary file for GM1")
        createBinary(binarydata2, 1, wonumber, serialnums[1], testtype)
    else:
        print("GM1 not needed, no data saved")
        log.info("GM1 not needed, no data saved")
    if serialnums[2] != "":
        print("Saving binary file for GM2")
        log.info("Saving binary file for GM2")
        createBinary(binarydata3, 2, wonumber, serialnums[2], testtype)
    else:
        print("GM2 not needed, no data saved")
        log.info("GM2 not needed, no data saved")
    if serialnums[3] != "":
        print("Saving binary file for GM3")
        log.info("Saving binary file for GM3")
        createBinary(binarydata4, 3, wonumber, serialnums[3], testtype)
    else:
        print("GM3 not needed, no data saved")
        log.info("GM3 not needed, no data saved")

def createCSV(datafile, gmid, wonumber, serialnum):
    with open(f"/media/evfile01/eV common/Production/Test & Measurement Results/keV-360/Unmounted Data Test/{serialnum}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["AMID", "GMID", "Timestamp", "PixelNumber", "Energy", "EnergyPosEvent", "ExceededThreshold", "TimeDetect", "TimeDetectPosEvent"])
        writer.writerows(datafile)
    csvfile.close()

def createBinary(datafile, gmid, wonumber, serialnum, testtype):
    badvalues = [3,5,7,9,13,15,17,19,21,22,23,27,29,31,32,33,34,35,36,37,41,43,44,45,46,47,48,49,63,66,70,74,76,78,
                80,81,82,84,85,86,90,91,92,93,94,95,96,97,98,99,102,103,104,105,106,108,110,114,115,116,117,118,120,126]
    if testtype == 360:
        path = f"/storage/eV common/Production/Test & Measurement Results/keV-360/Unmounted Data Test/{wonumber}"
    elif testtype == 373:
        path = f"/storage/eV common/Production/Test & Measurement Results/keV-373/Unmounted Data Test/{wonumber}"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        print("new directory created")
        log.info("new directory created")
    with open(path+f"/{serialnum}.dat", "wb") as binaryfile:
        for i in datafile:
            binaryfile.write(i[0].to_bytes(1, "big"))
            binaryfile.write(i[1].to_bytes(1, "big"))
            binaryfile.write(i[2].to_bytes(2, "big"))
            binaryfile.write(i[3].to_bytes(2, "big"))
            binaryfile.write(i[4].to_bytes(2, "big"))
            binaryfile.write(i[5].to_bytes(1, "big"))
            binaryfile.write(i[6].to_bytes(1, "big"))
            binaryfile.write(i[7].to_bytes(2, "big"))
            binaryfile.write(i[8].to_bytes(1, "big"))
    binaryfile.close()
    datafile.clear()

def pulserScan(wonumber, collectTime, hv, serialnums):
    util.turnHVOn(hv)
    collect_and_get_counts(collectTime)
    if not binarydata1 or not binarydata2 or not binarydata3 or not binarydata4:
        print("There was no data collected, trying again")
        log.error("There was no data collected, trying again")
        collect_and_get_counts(collectTime)
    isData = convertData(wonumber, serialnums)
    if isData is False:
        util.turnHVOff()
        return "No Data"
    else:
        util.turnHVOff()
        return True
    util.turnHVOff()

def ThresholdScan(wonumber, collectTime, hv, serialnums, testtype):
    util.turnHVOn(hv)
    print("HV on, Starting Testing")
    log.info("HV on, Starting Testing")
    collect_and_get_counts(collectTime)
    if not binarydata1 or not binarydata2 or not binarydata3 or not binarydata4:
        print("There was no data collected, trying again")
        log.error("There was no data collected, trying again")
        collect_and_get_counts(collectTime)
    isData = convertData(wonumber, serialnums, testtype)
    if isData is False:
        util.turnHVOff()
        return "No Data"
    else:
        util.turnHVOff()
        return True
    util.turnHVOff()
