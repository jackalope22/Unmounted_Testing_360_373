import DMatrix_internal as dm
import DMatrix_INTERNALAPI_Aliases as wrap
import DMatrix_Util as util
import logging
import time
from ctypes import POINTER, CFUNCTYPE, c_void_p
from collections import defaultdict
from testing.DMatrix_Redis import getRedisClient
import os
import pandas as pd
import csv

log = logging.getLogger(__name__)
redis_client = getRedisClient()

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

def checkForCancel():
    cancel = redis_client.get("cancel")
    cancel = cancel.decode("utf-8")
    print(f"cancel: {cancel}")
    logging.debug(f"cancel: {cancel}")
    if cancel == "True":
        return True
    else:
        return False

def collect_and_get_counts(collectTime):
    dm.sys_resetFrameCounts()
    count = 0
    SetDataCallback()
    dm.collect_setCollectionDelay(100)
    dm.collect_start()
    while count < collectTime:
        dm.api_processEvents()
        time.sleep(.9)
        count += 1
    dm.collect_stop()
    print("Data Collection Complete")
    print(f"binary data collected gm 0: {len(binarydata1)}")
    print(f"binary data collected gm 1: {len(binarydata2)}")
    print(f"binary data collected gm 2: {len(binarydata3)}")
    print(f"binary data collected gm 3: {len(binarydata4)}")
    #for lists in range(numpfbs):
        #collectAllLists.append(pfbs[lists])
    #convertAndStoreData(collectAllLists, n_frames, numpfbs)
def convertData(wonumber, serialnums, testtype, csvneeded=False):
    global binarydata1
    global binarydata2
    global binarydata3
    global binarydata4

    log.info(serialnums)
    print("Writing data to Storage")
    log.info("Writing data to Storage")
    if csvneeded == True:
        # print("Writing csv files")
        log.info("Writing csv files")
        if serialnums[0] != "":
            log.info("Writing csv file for GM0")
            csvflag0, error0 = createCSV(binarydata1, 0, wonumber, serialnums[0])
            if csvflag0 != True:
                return(False, error0)
        if serialnums[1] != "":
            log.info("Writing csv file for GM1")
            csvflag1, error1 = createCSV(binarydata2, 1, wonumber, serialnums[1])
            if csvflag1 != True:
                return(False, error1)
        if serialnums[2] != "":
            log.info("writing csv file for GM2")
            csvflag2, error2 = createCSV(binarydata3, 2, wonumber, serialnums[2])
            if csvflag2 != True:
                return(False, error2)
        if serialnums[3] != "":
            log.info("Writing csv file for GM3")
            csvflag3, error3 = createCSV(binarydata4, 3, wonumber, serialnums[3])
            if csvflag3 != True:
                return(False, error3)
    print("Writing binary files")
    log.info("Writing binary files")
    if serialnums[0] != "":
        print("Saving binary file for GM0")
        log.info("Saving binary file for GM0")
        iferror = createBinary(binarydata1, 0, wonumber, serialnums[0], testtype)
        if iferror != None:
            return False, iferror
    else:
        print("GM0 not needed, no data saved")
        log.info("GM0 not needed, no data saved")
        binarydata1.clear()
    if serialnums[1] != "":
        print("Saving binary file for GM1")
        log.info("Saving binary file for GM1")
        iferror = createBinary(binarydata2, 1, wonumber, serialnums[1], testtype)
        if iferror != None:
            return False, iferror
    else:
        print("GM1 not needed, no data saved")
        log.info("GM1 not needed, no data saved")
        binarydata2.clear()
    if serialnums[2] != "":
        print("Saving binary file for GM2")
        log.info("Saving binary file for GM2")
        iferror = createBinary(binarydata3, 2, wonumber, serialnums[2], testtype)
        if iferror != None:
            return False, iferror
    else:
        print("GM2 not needed, no data saved")
        log.info("GM2 not needed, no data saved")
        binarydata3.clear()
    if serialnums[3] != "":
        print("Saving binary file for GM3")
        log.info("Saving binary file for GM3")
        iferror = createBinary(binarydata4, 3, wonumber, serialnums[3], testtype)
        if iferror != None:
            return False, iferror
    else:
        print("GM3 not needed, no data saved")
        log.info("GM3 not needed, no data saved")
        binarydata4.clear()

    return True, "No Errors"

def createCSV(datafile, gmid, wonumber, serialnum):
    path = (f"/media/evfile01/eV common/Production/Test & Measurement Results/keV-360/Unmounted Data Test/{wonumber}")
    findpath = os.path.exists(path)
    if not findpath:
        try: 
            os.makedirs(path)
            with open(rf"Z:\\eV common\Production\Test & Measurement Results\keV-360\Unmounted Data\{wonumber}\{serialnum}.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["AMID", "GMID", "Timestamp", "PixelNumber", "Energy", "EnergyPosEvent", "ExceededThreshold", "TimeDetect", "TimeDetectPosEvent"])
                writer.writerows(datafile)
            csvfile.close()
            return(True, "CSV Created")
        except (PermissionError, FileNotFoundError) as error:
            log.debug("Do not have permission to create Folder or could not find file")
            log.debug(error)
            return("Do not have permission to create Folder or could not find file")
    else:
        with open(rf"Z:\\eV common\Production\Test & Measurement Results\keV-360\Unmounted Data Test\{wonumber}\{serialnum}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["AMID", "GMID", "Timestamp", "PixelNumber", "Energy", "EnergyPosEvent", "ExceededThreshold", "TimeDetect", "TimeDetectPosEvent"])
            writer.writerows(datafile)
        csvfile.close()
        return(True, "CSV Created")

def createBinary(datafile, gmid, wonumber, serialnum, testtype):
    redis_client.rpush("process_messages_43", "Saving Binary File")
    badvalues = [3,5,7,9,13,15,17,19,21,22,23,27,29,31,32,33,34,35,36,37,41,43,44,45,46,47,48,49,63,66,70,74,76,78,
                80,81,82,84,85,86,90,91,92,93,94,95,96,97,98,99,102,103,104,105,106,108,110,114,115,116,117,118,120,126]
    if testtype == 360:
        path = rf"Z:\\eV common\Production\Test & Measurement Results\keV-360\Unmounted Data\{wonumber}"
    elif testtype == 373:
        path = rf"Z:\\eV common\Production\Test & Measurement Results\keV-373\Unmounted Data\{wonumber}"
    isExist = os.path.exists(path)
    if not isExist:
        try:
            os.makedirs(path)
            print("new directory created")
            log.info(f"new directory created at {path}")
        except (PermissionError, FileNotFoundError) as error:
            log.debug("Do not have permission to create Folder or could not find file")
            log.debug(error)
            return("Do not have permission to create Folder or could not find file")
    try:
        with open(path+f"\{serialnum}.dat", "wb") as binaryfile:
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
    except (PermissionError, FileNotFoundError) as error:
        log.debug(error)
        datafile.clear()
        return "Do not have permission to ceate File or could not find file"

def pulserScan(wonumber, collectTime, hv, serialnums, testtype):
    stopTest = checkForCancel()
    if stopTest == True:
        logging.info("Test Cancelled")
        return "Test Cancelled"
    count = 0
    collections = [binarydata1, binarydata2, binarydata3, binarydata4]
    util.turnHVOn(hv)
    redis_client.rpush("process_messages_43", "Collecting Data")
    collect_and_get_counts(collectTime)
    for datafile in collections:
        if len(datafile) > 10:
            count += 1
    if count == 0:
        print("There was no data collected, trying again")
        log.error("There was no data collected, trying again")
        redis_client.rpush("process_messages_43", "No Data Collected, Trying Again")
        collect_and_get_counts(collectTime)
        count = 0
        for datafiles in collections:
            if len(datafiles) > 10:
                count += 1
        if count == 0:
            print("There was no data collected")
            log.error("There was no data collected")
            redis_client.rpush("process_messages_43", "No Data Collected")
            redis_client.rpush("process_messages_43", "Turning HV Off")
            util.turnHVOff()
            return "No Data Collected"
    isData, error = convertData(wonumber, serialnums, testtype)
    if isData is False:
        redis_client.rpush("process_messages_43", "Turning HV Off")
        util.turnHVOff()
        for i in collections:
            i.clear()
        return error
    else:
        redis_client.rpush("process_messages_43", "Turning HV Off")
        util.turnHVOff()
        return True

def ThresholdScan(wonumber, collectTime, hv, serialnums, testtype):
    stopTest = checkForCancel()
    if stopTest == True:
        logging.info("Test Cancelled")
        return "Test Cancelled"
    count = 0
    collections = [binarydata1, binarydata2, binarydata3, binarydata4]
    redis_client.rpush("process_messages_43", f"Ramping HV up to {hv}")
    util.turnHVOn(hv)
    print("HV on, Starting Testing")
    log.info("HV on, Starting Testing")
    redis_client.rpush("process_messages_43", "Collecting Data")
    collect_and_get_counts(collectTime)
    for datafile in collections:
        if len(datafile) > 10:
            count += 1
    if count == 0:
        print("There was no data collected, trying again")
        log.error("There was no data collected, trying again")
        redis_client.rpush("process_messages_43", "No Data Collected, Trying Again")
        collect_and_get_counts(collectTime)
        count = 0
        for datafiles in collections:
            if len(datafiles) > 10:
                count += 1
        if count == 0:
            print("There was no data collected")
            log.error("There was no data collected")
            redis_client.rpush("process_messages_43", "No Data Collected")
            redis_client.rpush("process_messages_43", "Turning HV Off")
            util.turnHVOff()
            return "No Data Collected"
    isData, errordata = convertData(wonumber, serialnums, testtype)
    if isData is False:
        redis_client.rpush("process_messages_43", "Turning HV Off")
        util.turnHVOff()
        for i in collections:
            i.clear()
        return errordata
    else:
        redis_client.rpush("process_messages_43", "Turning HV Off")
        util.turnHVOff()
        return True
