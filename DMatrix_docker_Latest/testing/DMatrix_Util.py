
import DMatrix_internal as dm
import logging
import time
import csv

log = logging.getLogger(__name__)

def connectToApi(hostip, deviceip):
    checkConnect = dm.sys_isConnected()
    if checkConnect == True:
        print("Already Showing connection to API")
        log.info("Already Showing connected to API")
        return True
    else:
        connect = dm.sys_connect(hostip, deviceip)
        time.sleep(1)
        print(f"Connect to API: {connect}")
        log.info(f"Connect to API: {connect}")
        if connect == True:
            print("Connected on second try")
            return True
        elif connect == False:
            print("Failed to connect to API, Trying again ...")
            log.info("Failed to connect to API, Trying again ...")
            dm.sys_disconnect()
            time.sleep(2)
            secondconnect = dm.sys_connect(hostip, deviceip)
            print(f"Connect to API: {secondconnect}")
            log.info(f"Connect to API: {secondconnect}")
            if secondconnect == False:
                return False
            else:
                return True

def setSystemSettings(Powerflag):
    devicetype = dm.sys_set_deviceType(dm.DMatrixDevice_2x2)
    log.info(devicetype)
    if not dm.sys_set_enablePixelMapping(False):
        print("Pixel Mapping not set")
        log.debug("Pixel Mapping not set")
        return False
    if not dm.sys_set_hvSetType(dm.SetType_Stepped):
        print("Hv type not set")
        log.debug("Hv type not set")
        return False
    if not dm.sys_set_hvUpdateStep(20):#changed strp from 10 to 20 for faster ramping
        print("Hv update step not set")
        log.debug("Hv update step not set")
        return False
    if not dm.sys_set_hvUpdateStepInterval(5):
        print("Hv Step interval not set")
        log.debug("Hv Step interval not set")
        return False
    if not dm.sys_set_powerAllAm(True):
        print("AM's not Powered on")
        log.debug("AM's not Powered on")
        return False
    if not dm.sys_set_hvDACOffset(0):
        print("HV Dac offset not set")
        log.debug("HV Dac offset not set")
        return False
    dm.sys_set_fanCtl(dm.DMATRIX_FAN1, 255)
    #dm.sys_set_fanCtl(dm.DMATRIX_FAN2, 255)
    if Powerflag == False:
        print("Waiting 10 seconds for AM's to power up")
        log.info("Waiting 10 seconds for AM's to power up")
        time.sleep(12)
    if dm.sys_set_installedAM(0, True):
        print("all AM's installed")
        log.info("all AM's install and powered")

def setAmSettings():
    if not dm.am_set_active(0):
        print("AM Not set active")
        log.debug("AM Not set active")
        return False
    if not dm.am_set_updateType(dm.AMUpdateType_Broadcast):
        print("AM Update type not set")
        log.debug("AM Update type not set")
        return False
    time.sleep(.5)
    print("AM setting complete ...")
    log.info("AM setting complete ...")

def setGmSettings(pulsefreq, enablePulse, pulseCount):
    if not dm.gm_set_updateType(dm.GMUpdateType_Broadcast):
        print("GM Update type not set")
        log.debug("GM Update type not set")
        return False
    if not dm.gm_set_readoutMode(dm.GMReadout_Sparsified):
        print("GM Readout mode not set")
        log.debug("GM Readout mode not set")
        return False
    if not dm.gm_set_powerAsic(True):
        print("GM Set power asic not set")
        log.debug("GM Set power asic not set")
        return False
    dm.gm_set_pulserFrequency(pulsefreq)
    dm.gm_set_enableAnodePulser(enablePulse)
    dm.gm_set_cathodeMode(dm.GMCathMode_Unipolar)
    dm.gm_set_enableNegData(False)
    dm.gm_set_enableThermalData(False)
    dm.gm_set_pulseCount(pulseCount)
    time.sleep(.2)
    print("GM setting complete ...")
    log.info("GM setting complete ...")

def setASICSettings(testPulse, peakingtime_ms):
    if not dm.asic_set_channelThreshold(dm.ChannelThresholdType_AnodePositiveEnergy, 397.75):
        print("Channel Threshold Positive not set!")
    if not dm.asic_set_channelThreshold(dm.ChannelThresholdType_AnodeNegativeEnergy, 397.75):
        print("Channel Threshold Negative not set")
    dm.asic_set_peakingTime(dm.ChannelType_Anode, peakingtime_ms)
    dm.asic_set_peakingTime(dm.ChannelType_Cathode, peakingTimeInMicroSeconds=0.5)
    dm.asic_set_cathodeTimingChannelsShaperPeakingTime(dm.TimingChannelsShaperPeakingTime_400nS)
    dm.asic_set_channelThreshold(dm.ChannelThresholdType_CathodeEnergy, 1892.55)
    dm.asic_set_channelGain(dm.A_ChannelGain_120mV, dm.C_ChannelGain_60mV)
    dm.asic_set_readoutMode(dm.GMASICReadout_Sparsified)
    dm.asic_set_timeDetectRampLength(dm.ChannelType_Anode, rampLengthInMicroSeconds=1)
    dm.asic_set_peakDetectTimeout(dm.ChannelType_Anode,timeoutInMicroSeconds=1)
    dm.asic_set_anodeInternalLeakageCurrentGenerator(dm.InternalLeakageCurrentGenerator_0A)
    dm.asic_set_multipleFiringSuppressTime(dm.MultipleFiringSuppressionTime_62_5nS)
    dm.asic_set_timingChannelUnipolarGain(dm.TimingChannelUnipolarGain_27mV)
    dm.asic_set_timingChannelBiPolarGain(dm.TimingChannelBipolarGain_21mV)
    dm.asic_set_testPulse(dm.ChannelType_Anode, testPulse)
    dm.asic_set_anodeTestPulseEdge(dm.AnodeTestPulseEdge_InjectNegativeCharge)
    #dm.asic_set_globalOptions(dm.ASICGlobal_SingleEventMode, dm.ASICGlobal_TimingMultipleFiringSuppressor)
    dm.asic_set_globalOptions(dm.ASICGlobal_None)
    if not dm.asic_send_globalData():
        print("Asic Global data not sent")
    time.sleep(.5)
    print("ASIC setting complete ...")
    log.info("ASIC setting complete ...")

def setChannelSettings(testCap):
    dm.channel_set_activeType(dm.ChannelType_Anode)
    dm.channel_set_updateType(dm.ChannelUpdateType_Broadcast)
    dm.channel_set_mask(False)
    dm.channel_set_cpd(False)
    dm.channel_set_anodeSignalMonitored(dm.Signal_Positive)
    dm.channel_set_enableTestCapacitor(testCap)
    dm.channel_set_positivePulseThresholdTrim(-62)
    dm.channel_set_anodeNegativePulseThresholdTrim(-62)
    time.sleep(.2)
    if not dm.asic_send_channelData():
        print("channel data not sent to device")
        log.info("channel data not sent to device")
    time.sleep(2)
    print(f"Channel setting complete ...")
    log.info(f"Channel setting complete ...")

def turnHVOn(goal):
    goalmargin = goal - 10
    dm.sys_set_enableHV(True)
    dm.sys_set_hvCtl(goal)
    volts = 0
    while volts < goalmargin:
        time.sleep(8)
        getvolts = dm.sys_get_hvCtl()
        volts = getvolts.val
        log.info(f"Current volts {volts}")
    log.info("HV on ...")
    log.info(f"Current volts {volts}")
    log.info(f"Current volts set to {volts}")
    
def turnHVOff():
    dm.sys_set_hvCtl(0)
    volts = dm.sys_get_hvCtl()
    volts = volts.val
    log.info("Turning HV off ...")
    while volts > 5:
        time.sleep(8)
        getvolts = dm.sys_get_hvCtl()
        volts = getvolts.val
        log.info(f"Current volts {volts}")
    log.info("HV off ...")
    log.info(f"Current volts {volts}")
    log.info(f"Current volts set to {volts}")

