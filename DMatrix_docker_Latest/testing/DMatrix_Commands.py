import DMatrix_Util as util
import DMatrix_Processing as proc
import DMatrix_internal as dm
import datetime
import logging
import ctypes
import yaml


log = logging.getLogger(__name__)

class Dmatrix:

    def __init__(self, wonumber, testtype, serialnums):
        self.hostip = "192.168.1.148"
        self.deviceip = "192.168.1.149"
        self.wonumber = wonumber
        self.testtype = testtype
        self.serialnums = serialnums
        self.metadata = {}

    def initMeta(self):
        basesettings = {}
        now = datetime.datetime.now()
        basesettings["date time"] = now.strftime("%Y-%m-%d %H:%M:%S")
        self.metadata.update(basesettings)

    def writeMeta(self, test):
        path = f"/media/evfile01/eV common/Production/Test Measurement Results/keV-360/Unmounted Data Test/{self.wonumber}"
        with open(f"{path}/{test}_metadata.yaml", 'w') as metafile:
            yaml.dump(self.metadata, metafile, sort_keys=False)
        metafile.close()
        log.info(f"Metadata written to {path}/{test}_metadata.yaml")

    def main(self):
        if self.testtype == "pulser":
            connect = util.connectToApi(self.hostip, self.deviceip)
            if connect == False:
                return "Connection Failed"
            pulsedata = proc.pulserScan(self.wonumber, 10, 0, self.serialnums)#102 DAC value = -600 real voltage# 185 DAC value = -1150 real voltage
            if pulsedata is not True:
                return pulsedata
            else:
                return True
        elif self.testtype == "360":
            connect = util.connectToApi(self.hostip, self.deviceip)
            if connect == False:
                return "Connection Failed"
            thresholddata = proc.ThresholdScan(self.wonumber, 22, 185, self.serialnums, 360)
            if thresholddata is not True:
                return thresholddata
            else:
                return True
        elif self.testtype == "373":
            connect = util.connectToApi(self.hostip, self.deviceip)
            if connect == False:
                return "Connection Failed"
            thresholddata = proc.ThresholdScan(self.wonumber, 22, 200, self.serialnums, 373)
            if thresholddata is not True:
                return thresholddata
            else:
                return True
        else:
            pass