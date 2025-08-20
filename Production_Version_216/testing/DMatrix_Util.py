
from time import sleep
import DMatrix_internal as dm
import binascii
import logging
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
        sleep(1)
        print(f"Connect to API: {connect}")
        log.info(f"Connect to API: {connect}")
        if connect == True:
            print("Connected on second try")
            return True
        elif connect == False:
            print("Failed to connect to API, Trying again ...")
            log.info("Failed to connect to API, Trying again ...")
            dm.sys_disconnect()
            sleep(2)
            secondconnect = dm.sys_connect(hostip, deviceip)
            print(f"Connect to API: {secondconnect}")
            log.info(f"Connect to API: {secondconnect}")
            if secondconnect == False:
                return False
            else:
                return True

def initializeDevice():
    if dm.sys_isConnected():
        if not dm.sys_set_deviceType(dm.DMatrixDevice_2x2):
            log.debug("Device type not set")
            log.debug(f"last error {dm.api_get_lastErr()}")
            return False 
        dm.sys_set_fanCtl(dm.DMATRIX_FAN1, 255)
        dm.sys_set_fanCtl(dm.DMATRIX_FAN2, 255)
    else:
        log.debug("Not connected to API")
        return False
    log.info(f"Set Decvice type and fans on, last error {dm.api_get_lastErr()}")
    print("System Initialized.....")
    log.info("System Initialized.....")

def setSystemSettings(Powerflag):
    if not dm.sys_set_powerAllAm(True):
        log.debug("AM's not Powered on")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if dm.sys_set_installedAM(0, True):
        print("all AM's installed")
        log.info("all AM's install and powered")
    if Powerflag != "True":
        print("Waiting 10 seconds for AM's to power up")
        log.info("Waiting 10 seconds for AM's to power up")
        sleep(12)
        
    devicetype = dm.sys_set_deviceType(dm.DMatrixDevice_2x2)
    if not devicetype:
        log.debug("Device type not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    log.info(f"device type: {devicetype}")
    if not dm.sys_set_enablePixelMapping(False):
        log.debug("Pixel Mapping not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.sys_set_hvSetType(dm.SetType_Stepped):
        log.debug("Hv type not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.sys_set_hvUpdateStep(25):#changed strp from 10 to 20 for faster ramping
        log.debug("Hv update step not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.sys_set_hvUpdateStepInterval(5):
        log.debug("Hv Step interval not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.sys_set_hvDACSlope(4.802):
        log.debug("HV Dac Slope not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.sys_set_hvDACOffset(0):
        log.debug("HV Dac offset not set")
        return False
    print("System setting complete ...")
    log.info("System setting complete ...")
    
def setAmSettings():
    if not dm.am_set_active(0):
        log.debug("AM Not set active")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.am_set_updateType(dm.AMUpdateType_SingleAM):
        log.debug("AM Update type not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(1)
    print("AM setting complete ...")
    log.info("AM setting complete ...")

def setGmSettings(pulsefreq, enablePulse, pulseCount):
    if not dm.gm_set_updateType(dm.GMUpdateType_Broadcast):
        log.debug("GM Update type not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.gm_set_readoutMode(dm.GMReadout_Sparsified):
        log.debug("GM Readout mode not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.gm_set_cathodeMode(dm.CathodeTimingMode_Undefined):
        log.debug("GM Cathode mode not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.gm_set_powerAsic(True):
        log.debug("GM Set power asic not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.gm_set_delayTime(0):
        log.debug("GM Delay time not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.gm_set_timestampRes(0):
        log.debug("GM Timestamp resolution not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.gm_set_pulserFrequency(pulsefreq):
        log.debug("GM Pulser frequency not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.gm_set_enableAnodePulser(enablePulse):
        log.debug("GM Enable Anode Pulser not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.gm_set_enableNegData(False):
        log.debug("GM Enable Negative Data not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.gm_set_enableThermalData(False):
        log.debug("GM Enable Thermal Data not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.gm_set_pulseCount(pulseCount):
        log.debug("GM Pulse Count not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.gm_set_disablePackets(False):
        log.debug("GM Disable Packets not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(2)
    print("GM setting complete ...")
    log.info("GM setting complete ...")

def setASICSettings(testPulse, peakingtime_ms):
    if not dm.asic_set_peakDetectTimeout(dm.ChannelType_Anode, timeoutInMicroSeconds=1):
        log.debug("Anode Peak Detect Timeout not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_timeDetectRampLength(dm.ChannelType_Anode, rampLengthInMicroSeconds=1):
        log.debug("Anode Time Detect Ramp Length not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_analogOutputMonitored(dm.AnalogOutput_NoFunction):
        log.debug("Analog Output not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_anodeChannelMonitored(0):
        log.debug("Anode Channel Monitored not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_timingChannelUnipolarGain(dm.TimingChannelUnipolarGain_27mV):
        log.debug("Timing Channel Unipolar Gain not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_timingChannelBiPolarGain(dm.TimingChannelBipolarGain_21mV):
        log.debug("Timing Channel Bipolar Gain not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_readoutMode(dm.GMASICReadout_Sparsified):
        log.debug("GM Asic Readout mode not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_peakingTime(dm.ChannelType_Anode, peakingtime_ms):
        log.debug("Anode Peaking time not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_peakDetectTimeout(dm.ChannelType_Anode, timeoutInMicroSeconds=1):
        log.debug("Anode Peak Detect Timeout not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_peakDetectTimeout(dm.ChannelType_Cathode, timeoutInMicroSeconds=1):
        log.debug("Cathode Peak Detect Timeout not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_timeDetectRampLength(dm.ChannelType_Cathode, rampLengthInMicroSeconds=1):
        log.debug("Cathode Time Detect Ramp Length not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.asic_set_cathodeTimingChannelsShaperPeakingTime(dm.TimingChannelsShaperPeakingTime_400nS):
        log.debug("Cathode Timing Channels Shaper Peaking Time not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    #cathode internal leakage current generator maybe 2 channels
    if not dm.asic_set_cathodeChannelInternalLeakageCurrentGenerator(0, dm.CathodeInternalLeakageCurrentGenerator_350pA):
        log.debug("Cathode Channel Internal Leakage Current Generator not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    if not dm.asic_set_cathodeChannelInternalLeakageCurrentGenerator(1, dm.CathodeInternalLeakageCurrentGenerator_350pA):
        log.debug("Cathode Channel Internal Leakage Current Generator not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    #cathode timeing channel secondary multi-threshold maybe
    if not dm.asic_set_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement(-100):
        log.debug("Cathode Timing Channels Secondary Multi Thresholds Displacement not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_multipleFiringSuppressTime(dm.MultipleFiringSuppressionTime_62_5nS):
        log.debug("Multiple Firing Suppress Time not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_anodeInternalLeakageCurrentGenerator(dm.InternalLeakageCurrentGenerator_0A):
        log.debug("Anode Internal Leakage Current Generator not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_testPulse(dm.ChannelType_Anode, testPulse):
        log.debug("Anode Test Pulse not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_channelThreshold(dm.ChannelThresholdType_CathodeTimingPrimaryMultiThresholdBiPolar, 0):
        log.debug("Cathode Timing Primary Multi Threshold BiPolar not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_channelThreshold(dm.ChannelThresholdType_CathodeTimingUnipolar, 0):
        log.debug("Cathode Timing Unipolar not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_channelThreshold(dm.ChannelThresholdType_CathodeEnergy, 1892.55):
        log.debug("Cathode Energy not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_channelThreshold(dm.ChannelThresholdType_AnodeNegativeEnergy, 0):
        log.debug("Channel Threshold Negative not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_channelThreshold(dm.ChannelThresholdType_AnodePositiveEnergy, 397.75):
        log.debug("Channel Threshold Positive not set!")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_anodeTestPulseEdge(dm.AnodeTestPulseEdge_InjectNegativeCharge):
        log.debug("Anode Test Pulse Edge not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_channelGain(dm.A_ChannelGain_120mV, dm.C_ChannelGain_60mV):
        log.debug("Channel Gain not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_cathodeTestSigSrc(dm.CathodeTestSigSrc_SDI):
        log.debug("Cathode Test Signal Source not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_cathodeTestSigType(dm.TestSigType_Step):
        log.debug("Cathode Test Signal Type not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_DACMonitored(dm.DACS_NONE):
        log.debug("DAC Monitored not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_cathodeEnergyTimingMonitored(dm.CathodeEnergyTiming_NONE):
        log.debug("Cathode Energy Timing not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not dm.asic_set_globalOptions(dm.ASICGlobal_None):
        log.debug("Global Options not set")
        log.debug(f"last error {dm.api_get_lastErr()}")
        return False
    sleep(.1)
    if not  dm.asic_send_globalData():
        log.debug("Asic Global data not sent")
        log.debug(f"last error {dm.api_get_lastErr()}")
    sleep(.2)
    if not dm.asic_send_globalData():
        print("Asic Global data not sent")
        log.debug("Asic Global data not sent")
        log.debug(f"last error {dm.api_get_lastErr()}")
    dm.asic_send_globalData()
    sleep(.2)
    print("ASIC setting complete ...")
    log.info("ASIC setting complete ...")

def setChannelSettings(testCap):
    dm.channel_set_activeType(dm.ChannelType_Anode)
    sleep(.3)
    dm.channel_set_updateType(dm.ChannelUpdateType_Broadcast)
    sleep(.3)
    if not dm.channel_set_anodeSignalMonitored(dm.Signal_Positive):
        log.debug("Anode Signal Monitored not set")
        log.debug(dm.api_get_lastErr())    
    sleep(.3)
    if not dm.channel_set_mask(False):
        log.debug("Channel Mask not set")
        log.debug(dm.api_get_lastErr())
    sleep(.3)
    if not dm.channel_set_enableTestCapacitor(testCap):
        log.debug("Enable Test Capacitor not set")
        log.debug(dm.api_get_lastErr())
    sleep(.3)
    if not dm.channel_set_positivePulseThresholdTrim(-62):
        log.debug("Positive Pulse Threshold Trim not set")
        log.debug(dm.api_get_lastErr())
    sleep(.3)
    if not dm.channel_set_anodeNegativePulseThresholdTrim(-62):
        log.debug("Anode Negative Pulse Threshold Trim not set")
        log.debug(dm.api_get_lastErr())
    sleep(.3)
    if not dm.channel_set_cpd(False):
        log.debug("Channel Power Down not set")
        log.debug(dm.api_get_lastErr())
    sleep(.3)
    if not dm.asic_send_channelData():
        print("channel data not sent to device")
        log.info("channel data not sent to device")
    sleep(.5)
    if not dm.asic_send_channelData():
        print("channel data not sent to device")
        log.info("channel data not sent to device")
    sleep(.5)
    if not dm.asic_send_globalData():
        print("Global data not sent to device")
        log.info("Global data not sent to device")
    sleep(.5)
    if not dm.asic_send_channelData():
        print("channel data not sent to device")
        log.info("channel data not sent to device")
    sleep(.5)
    if not dm.asic_send_globalData():
        print("Global data not sent to device")
        log.info("Global data not sent to device")
    sleep(.5)
    if not dm.asic_send_globalData():
        print("Global data not sent to device")
        log.info("Global data not sent to device")
    print(f"Channel setting complete ...")
    log.info(f"Channel setting complete ...")

def maskChannels():
    anodelist = [ 3, 5, 7, 9, 13, 15, 17, 19, 21, 22, 23, 27, 29, 31, 32, 33, 34, 35, 36, 37, 
                 41, 43, 44, 45, 46, 47, 48, 49, 63, 66, 70, 74, 76, 78, 80, 81, 82, 84, 85,
                 86, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 102, 103, 104, 105, 106, 108,
                 110, 114, 115, 116, 117, 118, 120, 126]
    for channel in anodelist:
        dm.channel_set_activeType(dm.ChannelType_Anode)
        sleep(.05)
        dm.channel_set_updateType(dm.ChannelUpdateType_SingleChannel)
        sleep(.05)
        dm.channel_set_active(channel)
        sleep(.05)
        dm.channel_set_mask(True)
        sleep(.05)
    cathodelist = [0, 1]
    for channel in cathodelist:
        dm.channel_set_activeType(dm.ChannelType_Cathode)
        dm.channel_set_active(channel)
        dm.channel_set_mask(True)
    dm.asic_send_channelData()
    sleep(1)
    dm.asic_send_channelData()
    print("Channels masked...")
    log.info("Channels masked...")
#readreg = dm.mm_read_reg(6)
#print(f"Read reg 2: {readreg}")
#gmreadreg = dm.gm_read_reg(12)
#print(f"Read gm reg 6: {gmreadreg}")

def turnHVOn(goal):
    goalmargin = goal - 10
    dm.sys_set_enableHV(True)
    dm.sys_set_hvCtl(goal)
    volts = 0
    while volts < goalmargin:
        sleep(8)
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
        sleep(8)
        getvolts = dm.sys_get_hvCtl()
        volts = getvolts.val
        log.info(f"Current volts {volts}")
    log.info("HV off ...")
    log.info(f"Current volts {volts}")
    log.info(f"Current volts set to {volts}")

def getsettings():
    hardware_settings = {}
    pixelmapping = dm.sys_get_enablePixelMapping()
    pixelmapping = str(pixelmapping)[5:].strip("}")
    hardware_settings["Pixel Mapping"] = pixelmapping
    hvsettype = dm.sys_get_hvSetType()
    hvsettype = str(hvsettype)[15:].strip("}")
    hardware_settings["HV Set Type"] = hvsettype
    hvupdatestep = dm.sys_get_hvUpdateStep()
    hvupdatestep = str(hvupdatestep)[6:].strip("}")
    hardware_settings["HV Update Step"] = hvupdatestep
    hvupdateinterval = dm.sys_get_hvUpdateStepInterval()
    hvupdateinterval = str(hvupdateinterval)[21:].strip("}")
    hardware_settings["HV Update Interval(sec)"] = hvupdateinterval
    syspowerallam = dm.sys_get_powerAllAm()
    syspowerallam = str(syspowerallam)[5:].strip("}")
    hardware_settings["Power All AM's"] = syspowerallam
    hvdacoffset = dm.sys_get_hvDACOffset()
    hvdacoffset = str(hvdacoffset)[11:].strip("}")
    hardware_settings["HV DAC Offset"] = hvdacoffset
    fan1 = dm.sys_get_fanCtl(dm.DMATRIX_FAN1)
    fan1 = str(fan1)[5:].strip("}")
    hardware_settings["Fan 1 speed"] = fan1
    fan2 = dm.sys_get_fanCtl(dm.DMATRIX_FAN2)
    fan2 = str(fan2)[5:].strip("}")
    hardware_settings["Fan 2 speed"] = fan2
    installedam = dm.sys_get_installedAM(0)
    installedam = str(installedam)[5:].strip("}")
    hardware_settings["AM 0 Installed"] = installedam
    activeam = dm.am_get_active()
    hardware_settings["Active AM"] = activeam
    amupdate = dm.am_get_updateType()
    amupdate = str(amupdate)[13:]
    hardware_settings["AM Update Type"] = amupdate
    gmupdate = dm.gm_get_updateType()
    gmupdate = str(gmupdate)[13:]
    hardware_settings["GM Update Type"] = gmupdate
    readoutmode = dm.gm_get_readoutMode()
    readoutmode = str(readoutmode)[20:].strip("}")
    hardware_settings["GM Readout Mode"] = readoutmode
    powerasic = dm.gm_get_powerAsic()
    powerasic = str(powerasic)[5:].strip("}")
    hardware_settings["Power ASIC"] = powerasic
    pulserfreq = dm.gm_get_pulserFrequency()
    pulserfreq = str(pulserfreq)[24:].strip("}")
    hardware_settings["Pulser Frequency"] = pulserfreq
    enableanodepulser = dm.gm_get_enableAnodePulser()
    enableanodepulser = str(enableanodepulser)[5:].strip("}")
    hardware_settings["Enable Anode Pulser"] = enableanodepulser
    cathodemode = dm.gm_get_cathodeMode()
    cathodemode = str(cathodemode)[20:].strip("}")
    hardware_settings["Cathode Mode"] = cathodemode
    enablenegdata = dm.gm_get_enableNegData()
    enablenegdata = str(enablenegdata)[5:].strip("}")
    hardware_settings["Enable Negative Data"] = enablenegdata
    enablethermaldata = dm.gm_get_enableThermalData()
    enablethermaldata = str(enablethermaldata)[5:].strip("}")
    hardware_settings["Enable Thermal Data"] = enablethermaldata
    pulsecount = dm.gm_get_pulseCount()
    pulsecount = str(pulsecount)[10:].strip("}")
    hardware_settings["Pulse Count"] = pulsecount
    posanodechannelthreshold = dm.asic_get_channelThreshold(dm.ChannelThresholdType_AnodePositiveEnergy)
    posanodechannelthreshold = str(posanodechannelthreshold)[15:].strip("}")
    hardware_settings["Positive Anode Channel Threshold(mv)"] = posanodechannelthreshold
    neganodechannelthreshold = dm.asic_get_channelThreshold(dm.ChannelThresholdType_AnodeNegativeEnergy)
    neganodechannelthreshold = str(neganodechannelthreshold)[15:].strip("}")
    hardware_settings["Negative Anode Channel Threshold(mv)"] = neganodechannelthreshold
    anodepeakingtime = dm.asic_get_peakingTime(dm.ChannelType_Anode)
    anodepeakingtime = str(anodepeakingtime)[27:].strip("}")
    hardware_settings["Anode Peaking Time(micro sec)"] = anodepeakingtime
    cathodepeakingtime = dm.asic_get_peakingTime(dm.ChannelType_Cathode)
    cathodepeakingtime = str(cathodepeakingtime)[27:].strip("}")
    hardware_settings["Cathode Peaking Time(micro sec)"] = cathodepeakingtime
    cathodetimingchannels = dm.asic_get_cathodeTimingChannelsShaperPeakingTime()
    cathodetimingchannels = str(cathodetimingchannels)[45:].strip("}")
    hardware_settings["Cathode Timing Channels Shaper Peaking Time"] = cathodetimingchannels
    cathodechannelthreshold = dm.asic_get_channelThreshold(dm.ChannelThresholdType_CathodeEnergy)
    cathodechannelthreshold = str(cathodechannelthreshold)[15:].strip("}")
    hardware_settings["Cathode Channel Threshold(mv)"] = cathodechannelthreshold
    channelgain = dm.asic_get_channelGain()
    anodechannelgain = str(channelgain)[24:43]
    cathodechannelgain = str(channelgain)[70:].strip("}")
    hardware_settings["Anode Channel Gain"] = anodechannelgain
    hardware_settings["Cathode Channel Gain"] = cathodechannelgain
    readoutmode = dm.asic_get_readoutMode()
    readoutmode = str(readoutmode)[24:].strip("}")
    hardware_settings["GM Asic Readout Mode"] = readoutmode
    ramplength = dm.asic_get_timeDetectRampLength(dm.ChannelType_Anode)
    ramplength = str(ramplength)[26:].strip("}")
    hardware_settings["Time Detect Ramp Length(micro sec)"] = ramplength
    peakdetecttimeout = dm.asic_get_peakDetectTimeout(dm.ChannelType_Anode)
    peakdetecttimeout = str(peakdetecttimeout)[23:].strip("}")
    hardware_settings["Peak Detect Timeout(micro sec)"] = peakdetecttimeout
    andodeinternalleakage = dm.asic_get_anodeInternalLeakageCurrentGenerator()
    andodeinternalleakage = str(andodeinternalleakage)[41:].strip("}")
    hardware_settings["Anode Internal Leakage Current Generator"] = andodeinternalleakage
    multifire = dm.asic_get_multipleFiringSuppressTime()
    multifire = str(multifire)[44:].strip("}")
    hardware_settings["Multiple Firing Suppress Time"] = multifire
    unipolargain = dm.asic_get_timingChannelUnipolarGain()
    unipolargain = str(unipolargain)[32:].strip("}")
    hardware_settings["Timing Channel Unipolar Gain"] = unipolargain
    bipolar = dm.asic_get_timingChannelBiPolarGain()
    bipolar = str(bipolar)[31:].strip("}")
    hardware_settings["Timing Channel Bipolar Gain"] = bipolar
    testpulse = dm.asic_get_testPulse(dm.ChannelType_Anode)
    testpulse = str(testpulse)[11:].strip("}")
    hardware_settings["Test Pulse (mV)"] = testpulse
    pulseedge = dm.asic_get_anodeTestPulseEdge()
    pulseedge = str(pulseedge)[20:].strip("}")
    hardware_settings["Anode Test Pulse Edge"] = pulseedge
    globaloptions = dm.asic_get_globalOptions()
    globaloptions = str(globaloptions)[9:].strip("}")
    hardware_settings["Global Options"] = globaloptions
    channelactive = dm.channel_get_activeType()
    channelactive = str(channelactive)[12:].strip("}")
    hardware_settings["Channel Active Type"] = channelactive
    channelupdate = dm.channel_get_updateType()
    channelupdate = str(channelupdate)[37:].strip("}")
    hardware_settings["Channel Update Type"] = channelupdate
    return hardware_settings
    #for key, value in hardware_settings.items():
        #log.info(f"{key} : {value}")

