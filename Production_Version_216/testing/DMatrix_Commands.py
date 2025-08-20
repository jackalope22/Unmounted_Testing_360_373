import DMatrix_Util as util
import DMatrix_Processing as proc
import DMatrix_internal as dm
import datetime
import logging
import ctypes
import os
import yaml
from testing.DMatrix_Redis import getRedisClient

redis_client = getRedisClient()

log = logging.getLogger(__name__)

class Dmatrix:

    def __init__(self, wonumber, testtype, serialnums):
        self.hostip = "192.168.1.148"
        self.deviceip = "192.168.1.149"
        self.wonumber = wonumber
        self.testtype = testtype
        self.serialnums = serialnums
        self.metadata = {}

    def initMeta(self, time, hv):
        basesettings = {}
        now = datetime.datetime.now()
        basesettings["date time"] = now.strftime("%Y-%m-%d %H:%M:%S")
        basesettings["work order"] = self.wonumber
        basesettings["test type"] = self.testtype
        basesettings["collect time"] = time
        basesettings["hv"] = hv
        self.metadata.update(basesettings)

    def writeMeta(self, test, testtype):
        path = f"/media/evfile01/eV common/Production/Test & Measurement Results/keV-{testtype}/Unmounted Data/{self.wonumber}"
        findpath = os.path.exists(path)
        if not findpath: 
            os.makedirs(path)
        with open(f"{path}/{test}_metadata.yaml", 'w') as metafile:
            yaml.dump(self.metadata, metafile, sort_keys=False)
        metafile.close()
        log.info(f"Metadata written to {path}/{test}_metadata.yaml")

    def read_test_config(self, config_file_path="test_config.yaml"):
        """Read configuration values from test config file"""
        try:
            # Check if config file exists in the testing directory first
            testing_dir_path = os.path.join(os.path.dirname(__file__), config_file_path)
            if os.path.exists(testing_dir_path):
                config_path = testing_dir_path
            elif os.path.exists(config_file_path):
                config_path = config_file_path
            else:
                log.warning(f"Config file not found at {config_file_path} or {testing_dir_path}, using default values")
                return {}
            
            with open(config_path, 'r') as config_file:
                config = yaml.safe_load(config_file)
                config_file.close()
                log.info(f"Loaded configuration from {config_path}")
                return config if config else {}
        except yaml.YAMLError as e:
            log.error(f"Error parsing YAML config file: {e}")
            return {}
        except Exception as e:
            log.error(f"Error reading config file: {e}")
            return {}

    #ThresholdScan(wonumber, collectTime, hv, serialnums, testtype):
    def main(self):
        # Load configuration at the beginning
        config_path = "/media/evfile01/eV common/Production/Config Files/360_373_unmounted_testing/test_config_left.yaml"
        config = self.read_test_config(config_path)
        logging.info(config)

        if self.testtype == "pulser":
            # Use config values if available, otherwise use defaults
            collect_time = config.get('test_settings', {}).get('pulser', {}).get('collect_time', 22)
            hv = config.get('test_settings', {}).get('pulser', {}).get('hv', 0)
            log.info("Setting up to run Pulser test")
            connect = util.connectToApi(self.hostip, self.deviceip)
            log.info(f"Connected to device {connect}")
            if connect == False:
                return "Connection Failed"
            self.initMeta(collect_time, hv)
            hardwaresettings = util.getsettings()
            self.metadata.update(hardwaresettings)
            pulsedata = proc.pulserScan(self.wonumber, collect_time, hv, self.serialnums, 360)#102 DAC value = -600 real voltage# 185 DAC value = -1150 real voltage
            if pulsedata is not True:
                return pulsedata
            for i in self.serialnums:
                if i != "":
                    self.writeMeta(i, 360)
            return True

        elif self.testtype == "360":
            # Use config values if available, otherwise use defaults
            collect_time = config.get('test_settings', {}).get('360', {}).get('collect_time', 22)
            hv = config.get('test_settings', {}).get('360', {}).get('hv', 137)
            connect = util.connectToApi(self.hostip, self.deviceip)
            log.info(f"Connected to device {connect}")
            if connect == False:
                return "Connection Failed"
            self.initMeta(collect_time, hv)
            hardwaresettings = util.getsettings()
            self.metadata.update(hardwaresettings)
            thresholddata = proc.ThresholdScan(self.wonumber, collect_time, hv, self.serialnums, 360)
            if thresholddata is not True:
                return thresholddata
            for i in self.serialnums:
                if i != "":
                    self.writeMeta(i, 360)
            return True
        
        elif self.testtype == "373":
            collect_time = config.get('test_settings', {}).get('373', {}).get('collect_time', 22)
            findhv = config.get('test_settings', {}).get('373', {}).get('hv')
            logging.info(f"findhv {findhv}")
            hv = config.get('test_settings', {}).get('373', {}).get('hv', 200)
            connect = util.connectToApi(self.hostip, self.deviceip)
            log.info(f"Connected to device {connect}")
            if connect == False:
                return "Connection Failed"
            self.initMeta(collect_time, hv)
            hardwaresettings = util.getsettings()
            self.metadata.update(hardwaresettings)
            thresholddata = proc.ThresholdScan(self.wonumber, collect_time, hv, self.serialnums, 373)
            if thresholddata is not True:
                return thresholddata
            for i in self.serialnums:
                if i != "":
                    self.writeMeta(i, 373)
            return True
        
        else:
            pass
