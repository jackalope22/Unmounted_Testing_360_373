import DMatrix_INTERNALAPI_Aliases as wrap # type: ignore
import threading

# ------------------- BEGIN included file boilerplate.py -------------------
# This file is meant to be included in a generated user or internal API access module, not imported on it's own.

import os.path

from ctypes import (CDLL, CFUNCTYPE, POINTER, Structure, create_string_buffer, sizeof, byref,
                    c_bool, c_ubyte, c_byte, c_char,
                    c_int8, c_int16, c_int32, c_int64,
                    c_uint8, c_uint16, c_uint32, c_uint64,
                    c_void_p, c_float, c_double, c_long, c_int, c_short, c_ushort, c_uint, c_size_t)

my_dir_path = os.path.dirname(os.path.realpath(__file__))

from c_enum import CEnum

versionFileToExec = os.path.join(my_dir_path, "version.py")
exec(open(versionFileToExec).read())

# DMatrixDevice is in ignored_enums so we can special-case them

class DMatrixDevice(CEnum):
    DMatrixDevice_Undefined = None
    DMatrixDevice_2x2 = None
    DMatrixDevice_4x4 = None
    DMatrixDevice_2x8 = None
    QETDevice_2x4 = None
    DMatrixDevice_keV360 = None

DMatrixDevice_Undefined = DMatrixDevice.DMatrixDevice_Undefined
DMatrixDevice_2x2 = DMatrixDevice.DMatrixDevice_2x2
DMatrixDevice_4x4 = DMatrixDevice.DMatrixDevice_4x4
DMatrixDevice_2x8 = DMatrixDevice.DMatrixDevice_2x8
QETDevice_2x4 = DMatrixDevice.QETDevice_2x4
DMatrixDevice_keV360 = DMatrixDevice.DMatrixDevice_keV360

class OperationType(CEnum):
    OperationType_SavePackets = None
    OperationType_Collection = None
    OperationType_HVUpdate = None

class ValueChanged(CEnum):
    ValueChanged_HV = None

# typedef struct
# {
#    uint PixelNumber;
#    uint Counts;
# } DetectorData;

# typedef struct
#{
#    DetectorData BaseInfo;    
#    ushort AMID;
#    ushort Timestamp;
#    ushort Energy;
#    ushort TimeDetect;
#    BYTE Index;
#    BYTE GMID;
#    BYTE EnergyPosEvent;
#    BYTE TimeDetectPosEvent;
#    BYTE ExceededThreshold;
#} DMatrixData;

class DMatrixData(Structure):
    _pack_ = 1
    _fields_ = [ # First 2 are technically inside a DetectorData struct, but we can hopefully just get away with this:
		("PixelNumber", c_uint),
		("Counts", c_uint),
        ("AMID", c_ushort),
        ("Timestamp", c_ushort),
        ("Energy", c_ushort),
        ("TimeDetect", c_ushort),
        ("Index", c_ubyte),
        ("GMID", c_ubyte),
        ("EnergyPosEvent", c_ubyte),
        ("TimeDetectPosEvent", c_ubyte),
        ("ExceededThreshold", c_ubyte)]

# typedef struct
# {
#    short AM;
#    short GM;
#    short Channel;
# } PixelHardwareLocation;

class PixelHardwareLocation(Structure):
    _pack_ = 1
    _fields_ = [
		("AM", c_ushort),
		("GM", c_ushort),
		("Channel", c_ushort)]

# typedef int ASICGlobalOptions;
# Check what I did for eV-3500 similar non-enums in case I dif anything more "useful":
ASICGlobalOptions = c_int

ASICGlobal_None = 0
ASICGlobal_SingleEventMode = 1
ASICGlobal_EnergyMultipleFiringSuppressor = 1 << 1
ASICGlobal_Validation = 1 << 2
ASICGlobal_MonitorOutputs = 1 << 3
ASICGlobal_RouteTempMonitorToAXPK62 = 1 << 4
ASICGlobal_TimingMultipleFiringSuppressor = 1 << 5
ASICGlobal_DisableMultipleResetAcquisitionMode = 1 << 6
ASICGlobal_RouteMonitorToPinTDO = 1 << 7
ASICGlobal_BufferChnl62PreAmplifierMonitorOutput = 1 << 8
ASICGlobal_BufferChnl63PreAmplifierMonitorOutput = 1 << 9
ASICGlobal_BufferPeakAndTimeDetectorOutputs = 1 << 10
ASICGlobal_BufferAuxMonitorOutput = 1 << 11
ASICGlobal_HighGain = 1 << 12
ASICGlobal_NegChanPowerDown = 1 << 13

# This allows us to define functions preceded by
#   @preserve_active_modules_and_updatetypes
# ...which will enforce that current AM/GM "update type" and "active index"
# are recorded when the function is entered and restored on its exit
# (rather than the functions themselves having to preserve and restore state on their own)

import _thread
from contextlib import ContextDecorator
class preserve_active_modules_and_updatetypes(ContextDecorator):
    _lock = _thread.allocate_lock()

    def __init__(self):
        pass

    def __enter__(self):
        self._lock.acquire()

        self._priorActiveAM = am_get_active()
        self._prior_AMUpdateType = am_get_updateType()

        self._priorActiveGM = gm_get_active()
        self._prior_GMUpdateType = gm_get_updateType()

        self._lock.release()

    def __exit__(self, exc_type, exc, exc_tb):
        self._lock.acquire()
        
        am_set_active(self._priorActiveAM)
        am_set_updateType(self._prior_AMUpdateType)

        gm_set_active(self._priorActiveGM)
        gm_set_updateType(self._prior_GMUpdateType)

        self._lock.release()

import os
import os.path
import sys
DMatrixDLLEnvVar = 'DMatrixDLL'
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    #print('{}: running in a PyInstaller bundle'.format(__file__), flush=True)
    pass
else:
    #print('{}: running in a normal Python process'.format(__file__), flush=True)
    pass
os.environ[DMatrixDLLEnvVar] = os.path.join(bundle_dir, "DMatrixSharedLib_Internal.dll" if os.name == 'nt' else "libDMatrixSharedLib_Internal.so")
# -------------------- END included file boilerplate.py --------------------


class ArgsOUT:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        s = '{'
        comma = False
        for (k, v) in self.__dict__.items():
            if comma:
                s += ', '
            s += k + ':' + str(v)
            comma = True
        s += '}'
        return s

    def get(self, arg):
        return getattr(self, arg)

exception_on_error = False
verbose = False
locking = False
apiLock = threading.Lock()

def GetLastErrorValue():
    err = api_get_lastErr()
    if verbose:
        print("error:", err)
    return err.last_err

STATUS_COLLECTION = wrap.CallbackType.STATUS_COLLECTION.value
STATUS_CONNECTION = wrap.CallbackType.STATUS_CONNECTION.value

RegOp_Write = wrap.RegisterOp.RegOp_Write.value
RegOp_Read = wrap.RegisterOp.RegOp_Read.value

UpdateType_Single = wrap.UpdateType.UpdateType_Single.value
UpdateType_Broadcast = wrap.UpdateType.UpdateType_Broadcast.value

SetType_Undefined = wrap.SetType.SetType_Undefined.value
SetType_Direct = wrap.SetType.SetType_Direct.value
SetType_Stepped = wrap.SetType.SetType_Stepped.value

UpdateMode_Undefined = wrap.UpdateMode.UpdateMode_Undefined.value
UpdateMode_Manual = wrap.UpdateMode.UpdateMode_Manual.value
UpdateMode_Auto = wrap.UpdateMode.UpdateMode_Auto.value

Selection_Undefined = wrap.Selection.Selection_Undefined.value
Selection_Single = wrap.Selection.Selection_Single.value
Selection_All = wrap.Selection.Selection_All.value

PLLClock_Undefined = wrap.PLLClock.PLLClock_Undefined.value
PLLClock_20MHz = wrap.PLLClock.PLLClock_20MHz.value
PLLClock_40MHz = wrap.PLLClock.PLLClock_40MHz.value

AnodeTestPulseEdge_Undefined = wrap.AnodeTestPulseEdge.AnodeTestPulseEdge_Undefined.value
AnodeTestPulseEdge_InjectNegativeCharge = wrap.AnodeTestPulseEdge.AnodeTestPulseEdge_InjectNegativeCharge.value
AnodeTestPulseEdge_InjectPosAndNegCharge = wrap.AnodeTestPulseEdge.AnodeTestPulseEdge_InjectPosAndNegCharge.value

MonitorSignal_Positive = wrap.MonitorSignal.MonitorSignal_Positive.value
MonitorSignal_Negative = wrap.MonitorSignal.MonitorSignal_Negative.value

ChannelType_Anode = wrap.ChannelType.ChannelType_Anode.value
ChannelType_Cathode = wrap.ChannelType.ChannelType_Cathode.value

TimingChannelUnipolarGain_Undefined = wrap.TimingChannelUnipolarGain.TimingChannelUnipolarGain_Undefined.value
TimingChannelUnipolarGain_27mV = wrap.TimingChannelUnipolarGain.TimingChannelUnipolarGain_27mV.value
TimingChannelUnipolarGain_81mV = wrap.TimingChannelUnipolarGain.TimingChannelUnipolarGain_81mV.value

C_ChannelGain_Undefined = wrap.CathodeChannelGain.C_ChannelGain_Undefined.value
C_ChannelGain_20mV = wrap.CathodeChannelGain.C_ChannelGain_20mV.value
C_ChannelGain_60mV = wrap.CathodeChannelGain.C_ChannelGain_60mV.value

A_ChannelGain_Undefined = wrap.AnodeChannelGain.A_ChannelGain_Undefined.value
A_ChannelGain_20mV = wrap.AnodeChannelGain.A_ChannelGain_20mV.value
A_ChannelGain_40mV = wrap.AnodeChannelGain.A_ChannelGain_40mV.value
A_ChannelGain_60mV = wrap.AnodeChannelGain.A_ChannelGain_60mV.value
A_ChannelGain_120mV = wrap.AnodeChannelGain.A_ChannelGain_120mV.value

TestSigType_Undefined = wrap.TestSigType.TestSigType_Undefined.value
TestSigType_Step = wrap.TestSigType.TestSigType_Step.value
TestSigType_Ramp = wrap.TestSigType.TestSigType_Ramp.value

InternalLeakageCurrentGenerator_Undefined = wrap.InternalLeakageCurrentGenerator.InternalLeakageCurrentGenerator_Undefined.value
InternalLeakageCurrentGenerator_60pA = wrap.InternalLeakageCurrentGenerator.InternalLeakageCurrentGenerator_60pA.value
InternalLeakageCurrentGenerator_0A = wrap.InternalLeakageCurrentGenerator.InternalLeakageCurrentGenerator_0A.value

TimingChannelsShaperPeakingTime_Undefined = wrap.TimingChannelsShaperPeakingTime.TimingChannelsShaperPeakingTime_Undefined.value
TimingChannelsShaperPeakingTime_100nS = wrap.TimingChannelsShaperPeakingTime.TimingChannelsShaperPeakingTime_100nS.value
TimingChannelsShaperPeakingTime_200nS = wrap.TimingChannelsShaperPeakingTime.TimingChannelsShaperPeakingTime_200nS.value
TimingChannelsShaperPeakingTime_400nS = wrap.TimingChannelsShaperPeakingTime.TimingChannelsShaperPeakingTime_400nS.value
TimingChannelsShaperPeakingTime_800nS = wrap.TimingChannelsShaperPeakingTime.TimingChannelsShaperPeakingTime_800nS.value

MultipleFiringSuppressionTime_Undefined = wrap.MultipleFiringSuppressionTime.MultipleFiringSuppressionTime_Undefined.value
MultipleFiringSuppressionTime_62_5nS = wrap.MultipleFiringSuppressionTime.MultipleFiringSuppressionTime_62_5nS.value
MultipleFiringSuppressionTime_125nS = wrap.MultipleFiringSuppressionTime.MultipleFiringSuppressionTime_125nS.value
MultipleFiringSuppressionTime_250nS = wrap.MultipleFiringSuppressionTime.MultipleFiringSuppressionTime_250nS.value
MultipleFiringSuppressionTime_600nS = wrap.MultipleFiringSuppressionTime.MultipleFiringSuppressionTime_600nS.value

ChannelThresholdType_CathodeTimingPrimaryMultiThresholdBiPolar = wrap.ChannelThresholdType.ChannelThresholdType_CathodeTimingPrimaryMultiThresholdBiPolar.value
ChannelThresholdType_CathodeTimingUnipolar = wrap.ChannelThresholdType.ChannelThresholdType_CathodeTimingUnipolar.value
ChannelThresholdType_CathodeEnergy = wrap.ChannelThresholdType.ChannelThresholdType_CathodeEnergy.value
ChannelThresholdType_AnodeNegativeEnergy = wrap.ChannelThresholdType.ChannelThresholdType_AnodeNegativeEnergy.value
ChannelThresholdType_AnodePositiveEnergy = wrap.ChannelThresholdType.ChannelThresholdType_AnodePositiveEnergy.value

CathodeTestSigSrc_Undefined = wrap.CathodeTestSigSrc.CathodeTestSigSrc_Undefined.value
CathodeTestSigSrc_AnodeTestSig = wrap.CathodeTestSigSrc.CathodeTestSigSrc_AnodeTestSig.value
CathodeTestSigSrc_SDI = wrap.CathodeTestSigSrc.CathodeTestSigSrc_SDI.value

TimingChannelBipolarGain_Undefined = wrap.TimingChannelBipolarGain.TimingChannelBipolarGain_Undefined.value
TimingChannelBipolarGain_21mV = wrap.TimingChannelBipolarGain.TimingChannelBipolarGain_21mV.value
TimingChannelBipolarGain_55mV = wrap.TimingChannelBipolarGain.TimingChannelBipolarGain_55mV.value
TimingChannelBipolarGain_63mV = wrap.TimingChannelBipolarGain.TimingChannelBipolarGain_63mV.value
TimingChannelBipolarGain_164mV = wrap.TimingChannelBipolarGain.TimingChannelBipolarGain_164mV.value

AnalogOutput_Undefined = wrap.AnalogOutput.AnalogOutput_Undefined.value
AnalogOutput_NoFunction = wrap.AnalogOutput.AnalogOutput_NoFunction.value
AnalogOutput_Baseline = wrap.AnalogOutput.AnalogOutput_Baseline.value
AnalogOutput_Temperature = wrap.AnalogOutput.AnalogOutput_Temperature.value
AnalogOutput_DACS = wrap.AnalogOutput.AnalogOutput_DACS.value
AnalogOutput_CathodeEnergyTiming = wrap.AnalogOutput.AnalogOutput_CathodeEnergyTiming.value
AnalogOutput_AnodeEnergy = wrap.AnalogOutput.AnalogOutput_AnodeEnergy.value

CathodeEnergyTiming_Undefined = wrap.CathodeEnergyTiming.CathodeEnergyTiming_Undefined.value
CathodeEnergyTiming_Channel1Energy = wrap.CathodeEnergyTiming.CathodeEnergyTiming_Channel1Energy.value
CathodeEnergyTiming_Channel1Timing = wrap.CathodeEnergyTiming.CathodeEnergyTiming_Channel1Timing.value
CathodeEnergyTiming_Channel2Energy = wrap.CathodeEnergyTiming.CathodeEnergyTiming_Channel2Energy.value
CathodeEnergyTiming_Channel2Timing = wrap.CathodeEnergyTiming.CathodeEnergyTiming_Channel2Timing.value
CathodeEnergyTiming_NONE = wrap.CathodeEnergyTiming.CathodeEnergyTiming_NONE.value

DACS_Undefined = wrap.DACS.DACS_Undefined.value
DACS_AnodeEnergyThreshold = wrap.DACS.DACS_AnodeEnergyThreshold.value
DACS_AnodeEnergyTransient = wrap.DACS.DACS_AnodeEnergyTransient.value
DACS_CathodeEnergyThreshold = wrap.DACS.DACS_CathodeEnergyThreshold.value
DACS_CathodeTimingUnipolarThreshold = wrap.DACS.DACS_CathodeTimingUnipolarThreshold.value
DACS_CathodeTimingFirstMultiThreshold = wrap.DACS.DACS_CathodeTimingFirstMultiThreshold.value
DACS_CathodeTimingSecondMultiThreshold = wrap.DACS.DACS_CathodeTimingSecondMultiThreshold.value
DACS_CathodeTimingThirdMultiThreshold = wrap.DACS.DACS_CathodeTimingThirdMultiThreshold.value
DACS_AnodeTestSignal = wrap.DACS.DACS_AnodeTestSignal.value
DACS_CathodeTestSignal = wrap.DACS.DACS_CathodeTestSignal.value
DACS_NONE = wrap.DACS.DACS_NONE.value

Signal_Undefined = wrap.Signal.Signal_Undefined.value
Signal_Positive = wrap.Signal.Signal_Positive.value
Signal_Negative = wrap.Signal.Signal_Negative.value

ChannelUpdateType_SingleChannel = wrap.ChannelUpdateType.ChannelUpdateType_SingleChannel.value
ChannelUpdateType_Broadcast = wrap.ChannelUpdateType.ChannelUpdateType_Broadcast.value

TestPulseEdge_Undefined = wrap.TestPulseEdge.TestPulseEdge_Undefined.value
TestPulseEdge_InjectNegCharge = wrap.TestPulseEdge.TestPulseEdge_InjectNegCharge.value
TestPulseEdge_InjectPosAndNegCharge = wrap.TestPulseEdge.TestPulseEdge_InjectPosAndNegCharge.value

CathodeTimingChannelType_FirstMultiThresholdBiPolar = wrap.CathodeTimingChannelType.CathodeTimingChannelType_FirstMultiThresholdBiPolar.value
CathodeTimingChannelType_SecondMultiThreshold = wrap.CathodeTimingChannelType.CathodeTimingChannelType_SecondMultiThreshold.value
CathodeTimingChannelType_ThirdMultiThreshold = wrap.CathodeTimingChannelType.CathodeTimingChannelType_ThirdMultiThreshold.value
CathodeTimingChannelType_Unipolar = wrap.CathodeTimingChannelType.CathodeTimingChannelType_Unipolar.value

GMASICReadout_Undefined = wrap.GMASICReadoutMode.GMASICReadout_Undefined.value
GMASICReadout_Sparsified = wrap.GMASICReadoutMode.GMASICReadout_Sparsified.value
GMASICReadout_EnhancedSparsified = wrap.GMASICReadoutMode.GMASICReadout_EnhancedSparsified.value

CathodeInternalLeakageCurrentGenerator_Undefined = wrap.CathodeInternalLeakageCurrentGenerator.CathodeInternalLeakageCurrentGenerator_Undefined.value
CathodeInternalLeakageCurrentGenerator_350pA = wrap.CathodeInternalLeakageCurrentGenerator.CathodeInternalLeakageCurrentGenerator_350pA.value
CathodeInternalLeakageCurrentGenerator_2nA = wrap.CathodeInternalLeakageCurrentGenerator.CathodeInternalLeakageCurrentGenerator_2nA.value

CathodeShapedTimingSignal_Undefined = wrap.CathodeShapedTimingSignal.CathodeShapedTimingSignal_Undefined.value
CathodeShapedTimingSignal_Unipolar = wrap.CathodeShapedTimingSignal.CathodeShapedTimingSignal_Unipolar.value
CathodeShapedTimingSignal_Bipolar = wrap.CathodeShapedTimingSignal.CathodeShapedTimingSignal_Bipolar.value

CathodeTimingMode_Undefined = wrap.CathodeTimingMode.CathodeTimingMode_Undefined.value
CathodeTimingMode_Unipolar = wrap.CathodeTimingMode.CathodeTimingMode_Unipolar.value
CathodeTimingMode_MultiThreshold_Unipolar = wrap.CathodeTimingMode.CathodeTimingMode_MultiThreshold_Unipolar.value
CathodeTimingMode_BiPolar_Unipolar = wrap.CathodeTimingMode.CathodeTimingMode_BiPolar_Unipolar.value

GMReadout_ReadAll = wrap.GMReadoutMode.GMReadout_ReadAll.value
GMReadout_Sparsified = wrap.GMReadoutMode.GMReadout_Sparsified.value
GMReadout_EnhancedSparsified = wrap.GMReadoutMode.GMReadout_EnhancedSparsified.value
GMReadout_FlagsOnly = wrap.GMReadoutMode.GMReadout_FlagsOnly.value
GMReadout_Undefined = wrap.GMReadoutMode.GMReadout_Undefined.value

GMCathMode_Unipolar = wrap.GMCathodeMode.GMCathMode_Unipolar.value
GMCathMode_MultiThreshold = wrap.GMCathodeMode.GMCathMode_MultiThreshold.value
GMCathMode_Bipolar = wrap.GMCathodeMode.GMCathMode_Bipolar.value
GMCathMode_Undefined = wrap.GMCathodeMode.GMCathMode_Undefined.value

GMPulserFreq_100Hz = wrap.GMPulserFrequency.GMPulserFreq_100Hz.value
GMPulserFreq_1kHz = wrap.GMPulserFrequency.GMPulserFreq_1kHz.value
GMPulserFreq_10kHz = wrap.GMPulserFrequency.GMPulserFreq_10kHz.value
GMPulserFreq_100kHz = wrap.GMPulserFrequency.GMPulserFreq_100kHz.value
GMPulserFreq_Undefined = wrap.GMPulserFrequency.GMPulserFreq_Undefined.value

GMUpdateType_Undefined = wrap.GMUpdateType.GMUpdateType_Undefined.value
GMUpdateType_SingleGM = wrap.GMUpdateType.GMUpdateType_SingleGM.value
GMUpdateType_Broadcast = wrap.GMUpdateType.GMUpdateType_Broadcast.value

AMUpdateType_Undefined = wrap.AMUpdateType.AMUpdateType_Undefined.value
AMUpdateType_SingleAM = wrap.AMUpdateType.AMUpdateType_SingleAM.value
AMUpdateType_Broadcast = wrap.AMUpdateType.AMUpdateType_Broadcast.value

SysClockSpeed_Undefined = wrap.SysClockSpeed.SysClockSpeed_Undefined.value
SysClockSpeed_10MHZ = wrap.SysClockSpeed.SysClockSpeed_10MHZ.value
SysClockSpeed_20MHZ = wrap.SysClockSpeed.SysClockSpeed_20MHZ.value
SysClockSpeed_40MHZ = wrap.SysClockSpeed.SysClockSpeed_40MHZ.value
SysClockSpeed_80MHZ = wrap.SysClockSpeed.SysClockSpeed_80MHZ.value

PacketData_Undefined = wrap.PacketData.PacketData_Undefined.value
PacketData_AMNo = wrap.PacketData.PacketData_AMNo.value
PacketData_GMNo = wrap.PacketData.PacketData_GMNo.value
PacketData_Timestamp = wrap.PacketData.PacketData_Timestamp.value
PacketData_PhotonCount = wrap.PacketData.PacketData_PhotonCount.value

PhotonData_Undefined = wrap.PhotonData.PhotonData_Undefined.value
PhotonData_Pixel = wrap.PhotonData.PhotonData_Pixel.value
PhotonData_Energy = wrap.PhotonData.PhotonData_Energy.value
PhotonData_EnergyPosEvent = wrap.PhotonData.PhotonData_EnergyPosEvent.value
PhotonData_TimeDetect = wrap.PhotonData.PhotonData_TimeDetect.value
PhotonData_TimeDetectPosEvent = wrap.PhotonData.PhotonData_TimeDetectPosEvent.value
PhotonData_ThresholdFlag = wrap.PhotonData.PhotonData_ThresholdFlag.value

DMATRIX_FAN_UNDEFINED = wrap.FAN_SELECT.DMATRIX_FAN_UNDEFINED.value
DMATRIX_FAN1 = wrap.FAN_SELECT.DMATRIX_FAN1.value
DMATRIX_FAN2 = wrap.FAN_SELECT.DMATRIX_FAN2.value

BRAM_ID_UNDEFINED = wrap.BRAM_ID.BRAM_ID_UNDEFINED.value
BRAM_ID1 = wrap.BRAM_ID.BRAM_ID1.value
BRAM_ID2 = wrap.BRAM_ID.BRAM_ID2.value
BRAM_ID3 = wrap.BRAM_ID.BRAM_ID3.value
BRAM_ID4 = wrap.BRAM_ID.BRAM_ID4.value

STATUSFLAG_UNDEFINED = wrap.STATUSFLAG.STATUSFLAG_UNDEFINED.value
STATUSFLAG_STATUS0 = wrap.STATUSFLAG.STATUSFLAG_STATUS0.value
STATUSFLAG_STATUS1 = wrap.STATUSFLAG.STATUSFLAG_STATUS1.value
STATUSFLAG_EXT_TRG = wrap.STATUSFLAG.STATUSFLAG_EXT_TRG.value
STATUSFLAG_SYS_ERR = wrap.STATUSFLAG.STATUSFLAG_SYS_ERR.value
STATUSFLAG_SYS_COMM_ERR = wrap.STATUSFLAG.STATUSFLAG_SYS_COMM_ERR.value
STATUSFLAG_SYS_ILL_CMD = wrap.STATUSFLAG.STATUSFLAG_SYS_ILL_CMD.value
STATUSFLAG_AM_ERR = wrap.STATUSFLAG.STATUSFLAG_AM_ERR.value
STATUSFLAG_SYS_LED = wrap.STATUSFLAG.STATUSFLAG_SYS_LED.value
STATUSFLAG_HW_SW_STAT = wrap.STATUSFLAG.STATUSFLAG_HW_SW_STAT.value
STATUSFLAG_HV_LED = wrap.STATUSFLAG.STATUSFLAG_HV_LED.value
STATUSFLAG_HV_ON = wrap.STATUSFLAG.STATUSFLAG_HV_ON.value
STATUSFLAG_AM0_NOTERR = wrap.STATUSFLAG.STATUSFLAG_AM0_NOTERR.value
STATUSFLAG_AM1_NOTERR = wrap.STATUSFLAG.STATUSFLAG_AM1_NOTERR.value
STATUSFLAG_AM2_NOTERR = wrap.STATUSFLAG.STATUSFLAG_AM2_NOTERR.value
STATUSFLAG_AM3_NOTERR = wrap.STATUSFLAG.STATUSFLAG_AM3_NOTERR.value

FPGASTATUSFLAG_IDLE = wrap.FPGASTATUSFLAG.FPGASTATUSFLAG_IDLE.value
FPGASTATUSFLAG_ASICLOADERR = wrap.FPGASTATUSFLAG.FPGASTATUSFLAG_ASICLOADERR.value
FPGASTATUSFLAG_FIFOFULL = wrap.FPGASTATUSFLAG.FPGASTATUSFLAG_FIFOFULL.value

COMMERR_NONE = wrap.COMMERR_ID.COMMERR_NONE.value
COMMERR_PACKETCRC = wrap.COMMERR_ID.COMMERR_PACKETCRC.value
COMMERR_NOTUSED = wrap.COMMERR_ID.COMMERR_NOTUSED.value
COMMERR_PACKETINCOMPLETE = wrap.COMMERR_ID.COMMERR_PACKETINCOMPLETE.value
COMMERR_WRONGCOMMAND = wrap.COMMERR_ID.COMMERR_WRONGCOMMAND.value
COMMERR_EEPROM = wrap.COMMERR_ID.COMMERR_EEPROM.value
COMMERR_UNDEFINED = wrap.COMMERR_ID.COMMERR_UNDEFINED.value

COMMERROWNER_GM0 = wrap.COMMERR_OWNER.COMMERROWNER_GM0.value
COMMERROWNER_GM1 = wrap.COMMERR_OWNER.COMMERROWNER_GM1.value
COMMERROWNER_GM2 = wrap.COMMERR_OWNER.COMMERROWNER_GM2.value
COMMERROWNER_GM3 = wrap.COMMERR_OWNER.COMMERROWNER_GM3.value
COMMERROWNER_AMFPGA = wrap.COMMERR_OWNER.COMMERROWNER_AMFPGA.value
COMMERROWNER_UNDEFINED = wrap.COMMERR_OWNER.COMMERROWNER_UNDEFINED.value

SYSMODE_ASICSOFF = wrap.SYSMODE_ID.SYSMODE_ASICSOFF.value
SYSMODE_POWERUP = wrap.SYSMODE_ID.SYSMODE_POWERUP.value
SYSMODE_IDLE = wrap.SYSMODE_ID.SYSMODE_IDLE.value
SYSMODE_COLLECTING = wrap.SYSMODE_ID.SYSMODE_COLLECTING.value
SYSMODE_NOTUSED = wrap.SYSMODE_ID.SYSMODE_NOTUSED.value
SYSMODE_DEBUG = wrap.SYSMODE_ID.SYSMODE_DEBUG.value
SYSMODE_UNDEFINED = wrap.SYSMODE_ID.SYSMODE_UNDEFINED.value

GMCollectionType_All = wrap.GMCollectionType.GMCollectionType_All.value
GMCollectionType_Cycle = wrap.GMCollectionType.GMCollectionType_Cycle.value



error_code_to_exception_map = {
}


def mm_write_reg(regNum, w_word):
    if verbose:
        print('Called mm_write_reg() with params:')
        print('    regNum:', regNum)
        print('    w_word:', w_word)
    try:
        if locking:
            apiLock.acquire()

        if regNum < -2147483648 or regNum > 2147483647:
            if exception_on_error:
                raise ArgSizeException('mm_write_reg', 'regNum', regNum, 'c_int')
            if verbose:
                print('regNum (', regNum, ') is too large for c_int')
            return False

        if w_word < 0 or w_word > 4294967295:
            if exception_on_error:
                raise ArgSizeException('mm_write_reg', 'w_word', w_word, 'c_uint')
            if verbose:
                print('w_word (', w_word, ') is too large for c_uint')
            return False

        result = wrap.LIB.mm_write_reg(regNum, w_word)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_write_reg')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_read_reg(regNum):
    if verbose:
        print('Called mm_read_reg() with params:')
        print('    regNum:', regNum)
    try:
        if locking:
            apiLock.acquire()

        if regNum < -2147483648 or regNum > 2147483647:
            if exception_on_error:
                raise ArgSizeException('mm_read_reg', 'regNum', regNum, 'c_int')
            if verbose:
                print('regNum (', regNum, ') is too large for c_int')
            return False

        r_word = c_uint()

        result = wrap.LIB.mm_read_reg(regNum, r_word)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_read_reg')
        else:
            args = ArgsOUT()
            args.r_word = r_word.value
            if verbose:
                print('Got:')
                print('    r_word:', r_word.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_write_reg(b_RegNum, data):
    if verbose:
        print('Called gm_write_reg() with params:')
        print('    b_RegNum:', b_RegNum)
        print('    data:', data)
    try:
        if locking:
            apiLock.acquire()

        if b_RegNum < -2147483648 or b_RegNum > 2147483647:
            if exception_on_error:
                raise ArgSizeException('gm_write_reg', 'b_RegNum', b_RegNum, 'c_int')
            if verbose:
                print('b_RegNum (', b_RegNum, ') is too large for c_int')
            return False

        if data < 0 or data > 4294967295:
            if exception_on_error:
                raise ArgSizeException('gm_write_reg', 'data', data, 'c_uint')
            if verbose:
                print('data (', data, ') is too large for c_uint')
            return False

        result = wrap.LIB.gm_write_reg(b_RegNum, data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_write_reg')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_read_reg(b_RegNum):
    if verbose:
        print('Called gm_read_reg() with params:')
        print('    b_RegNum:', b_RegNum)
    try:
        if locking:
            apiLock.acquire()

        if b_RegNum < -2147483648 or b_RegNum > 2147483647:
            if exception_on_error:
                raise ArgSizeException('gm_read_reg', 'b_RegNum', b_RegNum, 'c_int')
            if verbose:
                print('b_RegNum (', b_RegNum, ') is too large for c_int')
            return False

        data = c_uint()

        result = wrap.LIB.gm_read_reg(b_RegNum, data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_read_reg')
        else:
            args = ArgsOUT()
            args.data = data.value
            if verbose:
                print('Got:')
                print('    data:', data.value)
            return args
    finally:
        if locking:
            apiLock.release()


def am_write_reg(b_RegNum, data):
    if verbose:
        print('Called am_write_reg() with params:')
        print('    b_RegNum:', b_RegNum)
        print('    data:', data)
    try:
        if locking:
            apiLock.acquire()

        if b_RegNum < -2147483648 or b_RegNum > 2147483647:
            if exception_on_error:
                raise ArgSizeException('am_write_reg', 'b_RegNum', b_RegNum, 'c_int')
            if verbose:
                print('b_RegNum (', b_RegNum, ') is too large for c_int')
            return False

        if data < 0 or data > 4294967295:
            if exception_on_error:
                raise ArgSizeException('am_write_reg', 'data', data, 'c_uint')
            if verbose:
                print('data (', data, ') is too large for c_uint')
            return False

        result = wrap.LIB.am_write_reg(b_RegNum, data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('am_write_reg')
        return result
    finally:
        if locking:
            apiLock.release()


def am_read_reg(b_RegNum):
    if verbose:
        print('Called am_read_reg() with params:')
        print('    b_RegNum:', b_RegNum)
    try:
        if locking:
            apiLock.acquire()

        if b_RegNum < -2147483648 or b_RegNum > 2147483647:
            if exception_on_error:
                raise ArgSizeException('am_read_reg', 'b_RegNum', b_RegNum, 'c_int')
            if verbose:
                print('b_RegNum (', b_RegNum, ') is too large for c_int')
            return False

        data = c_uint()

        result = wrap.LIB.am_read_reg(b_RegNum, data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('am_read_reg')
        else:
            args = ArgsOUT()
            args.data = data.value
            if verbose:
                print('Got:')
                print('    data:', data.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_newDeviceIP():
    if verbose:
        print('Called sys_get_newDeviceIP()')
    try:
        if locking:
            apiLock.acquire()

        val = c_uint()

        result = wrap.LIB.sys_get_newDeviceIP(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_newDeviceIP')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_newDeviceGateway():
    if verbose:
        print('Called sys_get_newDeviceGateway()')
    try:
        if locking:
            apiLock.acquire()

        val = c_uint()

        result = wrap.LIB.sys_get_newDeviceGateway(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_newDeviceGateway')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_newDeviceNetmask():
    if verbose:
        print('Called sys_get_newDeviceNetmask()')
    try:
        if locking:
            apiLock.acquire()

        val = c_uint()

        result = wrap.LIB.sys_get_newDeviceNetmask(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_newDeviceNetmask')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def mm_set_readClockSpeed(clockSpeed):
    if verbose:
        print('Called mm_set_readClockSpeed() with params:')
        print('    clockSpeed:', clockSpeed)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.mm_set_readClockSpeed(clockSpeed)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_readClockSpeed')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_get_readClockSpeed():
    if verbose:
        print('Called mm_get_readClockSpeed()')
    try:
        if locking:
            apiLock.acquire()

        val = c_int32()

        result = wrap.LIB.mm_get_readClockSpeed(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_get_readClockSpeed')
        else:
            args = ArgsOUT()
            args.val = wrap.SysClockSpeed(val.value)
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_heaterCtl(val):
    if verbose:
        print('Called sys_set_heaterCtl() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 4294967295:
            if exception_on_error:
                raise ArgSizeException('sys_set_heaterCtl', 'val', val, 'c_uint')
            if verbose:
                print('val (', val, ') is too large for c_uint')
            return False

        result = wrap.LIB.sys_set_heaterCtl(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_heaterCtl')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_heaterCtl():
    if verbose:
        print('Called sys_get_heaterCtl()')
    try:
        if locking:
            apiLock.acquire()

        val = c_uint()

        result = wrap.LIB.sys_get_heaterCtl(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_heaterCtl')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def mm_set_packetTxRate(transferRate):
    if verbose:
        print('Called mm_set_packetTxRate() with params:')
        print('    transferRate:', transferRate)
    try:
        if locking:
            apiLock.acquire()

        if transferRate < 0 or transferRate > 4294967295:
            if exception_on_error:
                raise ArgSizeException('mm_set_packetTxRate', 'transferRate', transferRate, 'c_uint')
            if verbose:
                print('transferRate (', transferRate, ') is too large for c_uint')
            return False

        result = wrap.LIB.mm_set_packetTxRate(transferRate)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_packetTxRate')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_get_packetTxRate():
    if verbose:
        print('Called mm_get_packetTxRate()')
    try:
        if locking:
            apiLock.acquire()

        transferRate = c_uint()

        result = wrap.LIB.mm_get_packetTxRate(transferRate)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_get_packetTxRate')
        else:
            args = ArgsOUT()
            args.transferRate = transferRate.value
            if verbose:
                print('Got:')
                print('    transferRate:', transferRate.value)
            return args
    finally:
        if locking:
            apiLock.release()


def mm_set_enableWebIface(val):
    if verbose:
        print('Called mm_set_enableWebIface() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('mm_set_enableWebIface', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.mm_set_enableWebIface(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_enableWebIface')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_get_enableWebIface():
    if verbose:
        print('Called mm_get_enableWebIface()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.mm_get_enableWebIface(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_get_enableWebIface')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def mm_set_testPacket(val):
    if verbose:
        print('Called mm_set_testPacket() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('mm_set_testPacket', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.mm_set_testPacket(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_testPacket')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_get_testPacket():
    if verbose:
        print('Called mm_get_testPacket()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.mm_get_testPacket(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_get_testPacket')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def mm_set_clearBram(val):
    if verbose:
        print('Called mm_set_clearBram() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('mm_set_clearBram', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.mm_set_clearBram(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_clearBram')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_get_clearBram():
    if verbose:
        print('Called mm_get_clearBram()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.mm_get_clearBram(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_get_clearBram')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def mm_set_enableLog(val):
    if verbose:
        print('Called mm_set_enableLog() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('mm_set_enableLog', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.mm_set_enableLog(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_enableLog')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_get_enableLog():
    if verbose:
        print('Called mm_get_enableLog()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.mm_get_enableLog(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_get_enableLog')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def mm_set_enableExternalTrigger(val):
    if verbose:
        print('Called mm_set_enableExternalTrigger() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('mm_set_enableExternalTrigger', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.mm_set_enableExternalTrigger(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_enableExternalTrigger')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_get_enableExternalTrigger():
    if verbose:
        print('Called mm_get_enableExternalTrigger()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.mm_get_enableExternalTrigger(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_get_enableExternalTrigger')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def mm_set_framesRx(val):
    if verbose:
        print('Called mm_set_framesRx() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 4294967295:
            if exception_on_error:
                raise ArgSizeException('mm_set_framesRx', 'val', val, 'c_uint')
            if verbose:
                print('val (', val, ') is too large for c_uint')
            return False

        result = wrap.LIB.mm_set_framesRx(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_framesRx')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_set_framesTx(val):
    if verbose:
        print('Called mm_set_framesTx() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 4294967295:
            if exception_on_error:
                raise ArgSizeException('mm_set_framesTx', 'val', val, 'c_uint')
            if verbose:
                print('val (', val, ') is too large for c_uint')
            return False

        result = wrap.LIB.mm_set_framesTx(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_framesTx')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_set_dbgMsg(val):
    if verbose:
        print('Called mm_set_dbgMsg() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('mm_set_dbgMsg', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.mm_set_dbgMsg(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_dbgMsg')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_get_dbgMsg():
    if verbose:
        print('Called mm_get_dbgMsg()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.mm_get_dbgMsg(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_get_dbgMsg')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def mm_set_dbgCon(val):
    if verbose:
        print('Called mm_set_dbgCon() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('mm_set_dbgCon', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.mm_set_dbgCon(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_dbgCon')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_get_dbgCon():
    if verbose:
        print('Called mm_get_dbgCon()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.mm_get_dbgCon(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_get_dbgCon')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def mm_set_dbgMode(val):
    if verbose:
        print('Called mm_set_dbgMode() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('mm_set_dbgMode', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.mm_set_dbgMode(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_dbgMode')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_get_dbgMode():
    if verbose:
        print('Called mm_get_dbgMode()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.mm_get_dbgMode(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_get_dbgMode')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def mm_get_dumpBram(bramId):
    if verbose:
        print('Called mm_get_dumpBram() with params:')
        print('    bramId:', bramId)
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.mm_get_dumpBram(bramId, val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_get_dumpBram')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def mm_set_dumpBram(bramId, val):
    if verbose:
        print('Called mm_set_dumpBram() with params:')
        print('    bramId:', bramId)
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('mm_set_dumpBram', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.mm_set_dumpBram(bramId, val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_dumpBram')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_set_collect(val):
    if verbose:
        print('Called mm_set_collect() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('mm_set_collect', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.mm_set_collect(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_set_collect')
        return result
    finally:
        if locking:
            apiLock.release()


def mm_get_collect():
    if verbose:
        print('Called mm_get_collect()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.mm_get_collect(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('mm_get_collect')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_udpPort(udp_port):
    if verbose:
        print('Called sys_set_udpPort() with params:')
        print('    udp_port:', udp_port)
    try:
        if locking:
            apiLock.acquire()

        if udp_port < 0 or udp_port > 4294967295:
            if exception_on_error:
                raise ArgSizeException('sys_set_udpPort', 'udp_port', udp_port, 'c_uint')
            if verbose:
                print('udp_port (', udp_port, ') is too large for c_uint')
            return False

        result = wrap.LIB.sys_set_udpPort(udp_port)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_udpPort')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_set_readNetworkCfg(val):
    if verbose:
        print('Called sys_set_readNetworkCfg() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('sys_set_readNetworkCfg', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.sys_set_readNetworkCfg(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_readNetworkCfg')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_readNetworkCfg():
    if verbose:
        print('Called sys_get_readNetworkCfg()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.sys_get_readNetworkCfg(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_readNetworkCfg')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def am_get_sysMode():
    if verbose:
        print('Called am_get_sysMode()')
    try:
        if locking:
            apiLock.acquire()

        sysID = c_int32()

        result = wrap.LIB.am_get_sysMode(sysID)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('am_get_sysMode')
        else:
            args = ArgsOUT()
            args.sysID = wrap.SYSMODE_ID(sysID.value)
            if verbose:
                print('Got:')
                print('    sysID:', sysID.value)
            return args
    finally:
        if locking:
            apiLock.release()


def am_get_readReady():
    if verbose:
        print('Called am_get_readReady()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.am_get_readReady(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('am_get_readReady')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_enableTimeDetect(val):
    if verbose:
        print('Called gm_set_enableTimeDetect() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('gm_set_enableTimeDetect', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.gm_set_enableTimeDetect(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_enableTimeDetect')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_enableTimeDetect():
    if verbose:
        print('Called gm_get_enableTimeDetect()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.gm_get_enableTimeDetect(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_enableTimeDetect')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_get_checksumErrors():
    if verbose:
        print('Called gm_get_checksumErrors()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_checksumErrors()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numTooLargeEnergies():
    if verbose:
        print('Called gm_get_numTooLargeEnergies()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numTooLargeEnergies()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numTooHighChannelNums():
    if verbose:
        print('Called gm_get_numTooHighChannelNums()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numTooHighChannelNums()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numTooLargeTimeDetects():
    if verbose:
        print('Called gm_get_numTooLargeTimeDetects()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numTooLargeTimeDetects()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numImpossNonExceededThresholds():
    if verbose:
        print('Called gm_get_numImpossNonExceededThresholds()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numImpossNonExceededThresholds()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numImpossEnergyPosEventZeros():
    if verbose:
        print('Called gm_get_numImpossEnergyPosEventZeros()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numImpossEnergyPosEventZeros()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numImpossTimeDetectPosEventZeros():
    if verbose:
        print('Called gm_get_numImpossTimeDetectPosEventZeros()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numImpossTimeDetectPosEventZeros()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numEnergyPosEventDiffTimeDetectPosEvents():
    if verbose:
        print('Called gm_get_numEnergyPosEventDiffTimeDetectPosEvents()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numEnergyPosEventDiffTimeDetectPosEvents()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numChK1Chan128():
    if verbose:
        print('Called gm_get_numChK1Chan128()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numChK1Chan128()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numChK1Chan129():
    if verbose:
        print('Called gm_get_numChK1Chan129()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numChK1Chan129()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numChK1Chan130():
    if verbose:
        print('Called gm_get_numChK1Chan130()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numChK1Chan130()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numChK1Chan131():
    if verbose:
        print('Called gm_get_numChK1Chan131()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numChK1Chan131()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numTempChan132():
    if verbose:
        print('Called gm_get_numTempChan132()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numTempChan132()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numChK2Chan133():
    if verbose:
        print('Called gm_get_numChK2Chan133()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numChK2Chan133()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numChK2Chan134():
    if verbose:
        print('Called gm_get_numChK2Chan134()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numChK2Chan134()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numChK2Chan135():
    if verbose:
        print('Called gm_get_numChK2Chan135()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numChK2Chan135()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numChK2Chan136():
    if verbose:
        print('Called gm_get_numChK2Chan136()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numChK2Chan136()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def sys_mapPixel(amID, gmID, channel, pixel):
    if verbose:
        print('Called sys_mapPixel() with params:')
        print('    amID:', amID)
        print('    gmID:', gmID)
        print('    channel:', channel)
        print('    pixel:', pixel)
    try:
        if locking:
            apiLock.acquire()

        if amID < -2147483648 or amID > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_mapPixel', 'amID', amID, 'c_int')
            if verbose:
                print('amID (', amID, ') is too large for c_int')
            return False

        if gmID < -2147483648 or gmID > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_mapPixel', 'gmID', gmID, 'c_int')
            if verbose:
                print('gmID (', gmID, ') is too large for c_int')
            return False

        if channel < -32768 or channel > 32767:
            if exception_on_error:
                raise ArgSizeException('sys_mapPixel', 'channel', channel, 'c_short')
            if verbose:
                print('channel (', channel, ') is too large for c_short')
            return False

        if pixel < -32768 or pixel > 32767:
            if exception_on_error:
                raise ArgSizeException('sys_mapPixel', 'pixel', pixel, 'c_short')
            if verbose:
                print('pixel (', pixel, ') is too large for c_short')
            return False

        result = wrap.LIB.sys_mapPixel(amID, gmID, channel, pixel)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_mapPixel')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_set_loggingPackets(val):
    if verbose:
        print('Called sys_set_loggingPackets() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('sys_set_loggingPackets', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.sys_set_loggingPackets(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_loggingPackets')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_loggingPackets():
    if verbose:
        print('Called sys_get_loggingPackets()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.sys_get_loggingPackets(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_loggingPackets')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def api_get_version():
    if verbose:
        print('Called api_get_version()')
    try:
        if locking:
            apiLock.acquire()

        api_version = create_string_buffer(4096)

        result = wrap.LIB.api_get_version(api_version)
        if verbose:
            print('result:', result)
        args = ArgsOUT()
        args.result = result
        args.api_version = api_version.value.decode()
        if verbose:
            print('Got:')
            print('    api_version:', api_version.value)
        return args
    finally:
        if locking:
            apiLock.release()


def api_get_version_size():
    if verbose:
        print('Called api_get_version_size()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.api_get_version_size()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def api_get_lastErr():
    if verbose:
        print('Called api_get_lastErr()')
    try:
        if locking:
            apiLock.acquire()

        last_err = create_string_buffer(4096)

        result = wrap.LIB.api_get_lastErr(last_err)
        if verbose:
            print('result:', result)
        args = ArgsOUT()
        args.result = result
        args.last_err = last_err.value.decode()
        if verbose:
            print('Got:')
            print('    last_err:', last_err.value)
        return args
    finally:
        if locking:
            apiLock.release()


def api_set_lastErr(last_err):
    if verbose:
        print('Called api_set_lastErr() with params:')
        print('    last_err:', last_err)
    try:
        if locking:
            apiLock.acquire()

        if type(last_err) is str:
            last_err = last_err.encode('utf-8')

        result = wrap.LIB.api_set_lastErr(last_err)
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def api_get_lastErr_size():
    if verbose:
        print('Called api_get_lastErr_size()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.api_get_lastErr_size()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def api_close():
    if verbose:
        print('Called api_close()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.api_close()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def api_set_opCompleteCallback(opCompleteFunction):
    if verbose:
        print('Called api_set_opCompleteCallback() with params:')
        print('    opCompleteFunction:', opCompleteFunction)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.api_set_opCompleteCallback(opCompleteFunction)
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def api_set_opProgressCallback(opProgressFunction):
    if verbose:
        print('Called api_set_opProgressCallback() with params:')
        print('    opProgressFunction:', opProgressFunction)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.api_set_opProgressCallback(opProgressFunction)
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def api_set_statusCallback(sysStatusFunc):
    if verbose:
        print('Called api_set_statusCallback() with params:')
        print('    sysStatusFunc:', sysStatusFunc)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.api_set_statusCallback(sysStatusFunc)
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def api_set_dataRecvdCallback(dataRecvdFunc):
    if verbose:
        print('Called api_set_dataRecvdCallback() with params:')
        print('    dataRecvdFunc:', dataRecvdFunc)
    try:
        if locking:
            apiLock.acquire()

        pData = c_void_p()

        result = wrap.LIB.api_set_dataRecvdCallback(dataRecvdFunc, pData)
        if verbose:
            print('result:', result)
        args = ArgsOUT()
        args.result = result
        args.pData = pData.value
        if verbose:
            print('Got:')
            print('    pData:', pData.value)
        return args
    finally:
        if locking:
            apiLock.release()


def api_set_valueChangedCallback(valChangedFunc):
    if verbose:
        print('Called api_set_valueChangedCallback() with params:')
        print('    valChangedFunc:', valChangedFunc)
    try:
        if locking:
            apiLock.acquire()

        pData = c_void_p()

        result = wrap.LIB.api_set_valueChangedCallback(valChangedFunc, pData)
        if verbose:
            print('result:', result)
        args = ArgsOUT()
        args.result = result
        args.pData = pData.value
        if verbose:
            print('Got:')
            print('    pData:', pData.value)
        return args
    finally:
        if locking:
            apiLock.release()


def api_processEvents():
    if verbose:
        print('Called api_processEvents()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.api_processEvents()
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('api_processEvents')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_connect(hostIP, deviceIP):
    if verbose:
        print('Called sys_connect() with params:')
        print('    hostIP:', hostIP)
        print('    deviceIP:', deviceIP)
    try:
        if locking:
            apiLock.acquire()

        if type(hostIP) is str:
            hostIP = hostIP.encode('utf-8')

        if type(deviceIP) is str:
            deviceIP = deviceIP.encode('utf-8')

        result = wrap.LIB.sys_connect(hostIP, deviceIP)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_connect')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_isConnected():
    if verbose:
        print('Called sys_isConnected()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_isConnected()
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_isConnected')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_disconnect():
    if verbose:
        print('Called sys_disconnect()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_disconnect()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def sys_set_fanCtl(fanNum, val):
    if verbose:
        print('Called sys_set_fanCtl() with params:')
        print('    fanNum:', fanNum)
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 255:
            if exception_on_error:
                raise ArgSizeException('sys_set_fanCtl', 'val', val, 'c_ubyte')
            if verbose:
                print('val (', val, ') is too large for c_ubyte')
            return False

        result = wrap.LIB.sys_set_fanCtl(fanNum, val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_fanCtl')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_fanCtl(fanNum):
    if verbose:
        print('Called sys_get_fanCtl() with params:')
        print('    fanNum:', fanNum)
    try:
        if locking:
            apiLock.acquire()

        val = c_ubyte()

        result = wrap.LIB.sys_get_fanCtl(fanNum, val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_fanCtl')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_hvSetType(sType):
    if verbose:
        print('Called sys_set_hvSetType() with params:')
        print('    sType:', sType)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_set_hvSetType(sType)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_hvSetType')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_hvSetType():
    if verbose:
        print('Called sys_get_hvSetType()')
    try:
        if locking:
            apiLock.acquire()

        sType = c_int32()

        result = wrap.LIB.sys_get_hvSetType(sType)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_hvSetType')
        else:
            args = ArgsOUT()
            args.sType = wrap.SetType(sType.value)
            if verbose:
                print('Got:')
                print('    sType:', sType.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_hvUpdateStep(step):
    if verbose:
        print('Called sys_set_hvUpdateStep() with params:')
        print('    step:', step)
    try:
        if locking:
            apiLock.acquire()

        if step < 0 or step > 255:
            if exception_on_error:
                raise ArgSizeException('sys_set_hvUpdateStep', 'step', step, 'c_ubyte')
            if verbose:
                print('step (', step, ') is too large for c_ubyte')
            return False

        result = wrap.LIB.sys_set_hvUpdateStep(step)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_hvUpdateStep')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_hvUpdateStep():
    if verbose:
        print('Called sys_get_hvUpdateStep()')
    try:
        if locking:
            apiLock.acquire()

        step = c_ubyte()

        result = wrap.LIB.sys_get_hvUpdateStep(step)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_hvUpdateStep')
        else:
            args = ArgsOUT()
            args.step = step.value
            if verbose:
                print('Got:')
                print('    step:', step.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_hvUpdateStepVolts(voltsStep):
    if verbose:
        print('Called sys_set_hvUpdateStepVolts() with params:')
        print('    voltsStep:', voltsStep)
    try:
        if locking:
            apiLock.acquire()

        if voltsStep < 0 or voltsStep > 4294967295:
            if exception_on_error:
                raise ArgSizeException('sys_set_hvUpdateStepVolts', 'voltsStep', voltsStep, 'c_uint')
            if verbose:
                print('voltsStep (', voltsStep, ') is too large for c_uint')
            return False

        result = wrap.LIB.sys_set_hvUpdateStepVolts(voltsStep)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_hvUpdateStepVolts')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_hvUpdateStepVolts():
    if verbose:
        print('Called sys_get_hvUpdateStepVolts()')
    try:
        if locking:
            apiLock.acquire()

        voltsStep = c_uint()

        result = wrap.LIB.sys_get_hvUpdateStepVolts(voltsStep)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_hvUpdateStepVolts')
        else:
            args = ArgsOUT()
            args.voltsStep = voltsStep.value
            if verbose:
                print('Got:')
                print('    voltsStep:', voltsStep.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_hvUpdateStepInterval(stepIntervalSeconds):
    if verbose:
        print('Called sys_set_hvUpdateStepInterval() with params:')
        print('    stepIntervalSeconds:', stepIntervalSeconds)
    try:
        if locking:
            apiLock.acquire()

        if stepIntervalSeconds < 0 or stepIntervalSeconds > 255:
            if exception_on_error:
                raise ArgSizeException('sys_set_hvUpdateStepInterval', 'stepIntervalSeconds', stepIntervalSeconds, 'c_ubyte')
            if verbose:
                print('stepIntervalSeconds (', stepIntervalSeconds, ') is too large for c_ubyte')
            return False

        result = wrap.LIB.sys_set_hvUpdateStepInterval(stepIntervalSeconds)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_hvUpdateStepInterval')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_hvUpdateStepInterval():
    if verbose:
        print('Called sys_get_hvUpdateStepInterval()')
    try:
        if locking:
            apiLock.acquire()

        stepIntervalSeconds = c_ubyte()

        result = wrap.LIB.sys_get_hvUpdateStepInterval(stepIntervalSeconds)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_hvUpdateStepInterval')
        else:
            args = ArgsOUT()
            args.stepIntervalSeconds = stepIntervalSeconds.value
            if verbose:
                print('Got:')
                print('    stepIntervalSeconds:', stepIntervalSeconds.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_hvDACSlope(fDACSlope):
    if verbose:
        print('Called sys_set_hvDACSlope() with params:')
        print('    fDACSlope:', fDACSlope)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_set_hvDACSlope(fDACSlope)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_hvDACSlope')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_hvDACSlope():
    if verbose:
        print('Called sys_get_hvDACSlope()')
    try:
        if locking:
            apiLock.acquire()

        fDACSlope = c_double()

        result = wrap.LIB.sys_get_hvDACSlope(fDACSlope)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_hvDACSlope')
        else:
            args = ArgsOUT()
            args.fDACSlope = fDACSlope.value
            if verbose:
                print('Got:')
                print('    fDACSlope:', fDACSlope.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_hvDACOffset(fDACOffset):
    if verbose:
        print('Called sys_set_hvDACOffset() with params:')
        print('    fDACOffset:', fDACOffset)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_set_hvDACOffset(fDACOffset)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_hvDACOffset')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_hvDACOffset():
    if verbose:
        print('Called sys_get_hvDACOffset()')
    try:
        if locking:
            apiLock.acquire()

        fDACOffset = c_double()

        result = wrap.LIB.sys_get_hvDACOffset(fDACOffset)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_hvDACOffset')
        else:
            args = ArgsOUT()
            args.fDACOffset = fDACOffset.value
            if verbose:
                print('Got:')
                print('    fDACOffset:', fDACOffset.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_hvCtl(val):
    if verbose:
        print('Called sys_set_hvCtl() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 255:
            if exception_on_error:
                raise ArgSizeException('sys_set_hvCtl', 'val', val, 'c_ubyte')
            if verbose:
                print('val (', val, ') is too large for c_ubyte')
            return False

        result = wrap.LIB.sys_set_hvCtl(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_hvCtl')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_hvCtl():
    if verbose:
        print('Called sys_get_hvCtl()')
    try:
        if locking:
            apiLock.acquire()

        val = c_ubyte()

        result = wrap.LIB.sys_get_hvCtl(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_hvCtl')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_hvTarget():
    if verbose:
        print('Called sys_get_hvTarget()')
    try:
        if locking:
            apiLock.acquire()

        val = c_ubyte()

        result = wrap.LIB.sys_get_hvTarget(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_hvTarget')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_hvCtlVolts(val):
    if verbose:
        print('Called sys_set_hvCtlVolts() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 4294967295:
            if exception_on_error:
                raise ArgSizeException('sys_set_hvCtlVolts', 'val', val, 'c_uint')
            if verbose:
                print('val (', val, ') is too large for c_uint')
            return False

        result = wrap.LIB.sys_set_hvCtlVolts(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_hvCtlVolts')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_hvCtlVolts():
    if verbose:
        print('Called sys_get_hvCtlVolts()')
    try:
        if locking:
            apiLock.acquire()

        val = c_uint()

        result = wrap.LIB.sys_get_hvCtlVolts(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_hvCtlVolts')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_hvTargetVolts():
    if verbose:
        print('Called sys_get_hvTargetVolts()')
    try:
        if locking:
            apiLock.acquire()

        val = c_uint()

        result = wrap.LIB.sys_get_hvTargetVolts(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_hvTargetVolts')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_stop_hvUpdate():
    if verbose:
        print('Called sys_stop_hvUpdate()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_stop_hvUpdate()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def sys_set_enableHV(val):
    if verbose:
        print('Called sys_set_enableHV() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('sys_set_enableHV', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.sys_set_enableHV(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_enableHV')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_enableHV():
    if verbose:
        print('Called sys_get_enableHV()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.sys_get_enableHV(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_enableHV')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_statusFlag(sflag):
    if verbose:
        print('Called sys_get_statusFlag() with params:')
        print('    sflag:', sflag)
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.sys_get_statusFlag(sflag, val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_statusFlag')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_deviceType(device):
    if verbose:
        print('Called sys_set_deviceType() with params:')
        print('    device:', device)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_set_deviceType(device)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_deviceType')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_deviceType():
    if verbose:
        print('Called sys_get_deviceType()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_get_deviceType()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def sys_set_enablePixelMapping(val):
    if verbose:
        print('Called sys_set_enablePixelMapping() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('sys_set_enablePixelMapping', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.sys_set_enablePixelMapping(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_enablePixelMapping')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_enablePixelMapping():
    if verbose:
        print('Called sys_get_enablePixelMapping()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.sys_get_enablePixelMapping(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_enablePixelMapping')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_hardwareLocationOfPixelCoordinate(pixelRow, pixelColumn):
    if verbose:
        print('Called sys_get_hardwareLocationOfPixelCoordinate() with params:')
        print('    pixelRow:', pixelRow)
        print('    pixelColumn:', pixelColumn)
    try:
        if locking:
            apiLock.acquire()

        if pixelRow < -2147483648 or pixelRow > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_get_hardwareLocationOfPixelCoordinate', 'pixelRow', pixelRow, 'c_int')
            if verbose:
                print('pixelRow (', pixelRow, ') is too large for c_int')
            return False

        if pixelColumn < -2147483648 or pixelColumn > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_get_hardwareLocationOfPixelCoordinate', 'pixelColumn', pixelColumn, 'c_int')
            if verbose:
                print('pixelColumn (', pixelColumn, ') is too large for c_int')
            return False

        pixHWLoc = wrap.PixelHardwareLocation()

        result = wrap.LIB.sys_get_hardwareLocationOfPixelCoordinate(pixelRow, pixelColumn, pixHWLoc)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_hardwareLocationOfPixelCoordinate')
        else:
            args = ArgsOUT()
            args.pixHWLoc = pixHWLoc.value
            if verbose:
                print('Got:')
                print('    pixHWLoc:', pixHWLoc.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_hardwareLocationOfPixel(pixel):
    if verbose:
        print('Called sys_get_hardwareLocationOfPixel() with params:')
        print('    pixel:', pixel)
    try:
        if locking:
            apiLock.acquire()

        if pixel < -2147483648 or pixel > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_get_hardwareLocationOfPixel', 'pixel', pixel, 'c_int')
            if verbose:
                print('pixel (', pixel, ') is too large for c_int')
            return False

        pixHWLoc = wrap.PixelHardwareLocation()

        result = wrap.LIB.sys_get_hardwareLocationOfPixel(pixel, pixHWLoc)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_hardwareLocationOfPixel')
        else:
            args = ArgsOUT()
            args.pixHWLoc = pixHWLoc.value
            if verbose:
                print('Got:')
                print('    pixHWLoc:', pixHWLoc.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_pixelCoordinateOfHardwareLocation():
    if verbose:
        print('Called sys_get_pixelCoordinateOfHardwareLocation()')
    try:
        if locking:
            apiLock.acquire()

        pixHWLoc = wrap.PixelHardwareLocation()
        pixelRow = c_int()
        pixelColumn = c_int()

        result = wrap.LIB.sys_get_pixelCoordinateOfHardwareLocation(pixHWLoc, pixelRow, pixelColumn)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_pixelCoordinateOfHardwareLocation')
        else:
            args = ArgsOUT()
            args.pixHWLoc = pixHWLoc.value
            args.pixelRow = pixelRow.value
            args.pixelColumn = pixelColumn.value
            if verbose:
                print('Got:')
                print('    pixHWLoc:', pixHWLoc.value)
                print('    pixelRow:', pixelRow.value)
                print('    pixelColumn:', pixelColumn.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_pixelOfPixelCoordinate(pixelRow, pixelColumn):
    if verbose:
        print('Called sys_get_pixelOfPixelCoordinate() with params:')
        print('    pixelRow:', pixelRow)
        print('    pixelColumn:', pixelColumn)
    try:
        if locking:
            apiLock.acquire()

        if pixelRow < -2147483648 or pixelRow > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_get_pixelOfPixelCoordinate', 'pixelRow', pixelRow, 'c_int')
            if verbose:
                print('pixelRow (', pixelRow, ') is too large for c_int')
            return False

        if pixelColumn < -2147483648 or pixelColumn > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_get_pixelOfPixelCoordinate', 'pixelColumn', pixelColumn, 'c_int')
            if verbose:
                print('pixelColumn (', pixelColumn, ') is too large for c_int')
            return False

        pixel = c_int()

        result = wrap.LIB.sys_get_pixelOfPixelCoordinate(pixelRow, pixelColumn, pixel)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_pixelOfPixelCoordinate')
        else:
            args = ArgsOUT()
            args.pixel = pixel.value
            if verbose:
                print('Got:')
                print('    pixel:', pixel.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_noOfPixelRows():
    if verbose:
        print('Called sys_get_noOfPixelRows()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_get_noOfPixelRows()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_noOfPixelColumns():
    if verbose:
        print('Called sys_get_noOfPixelColumns()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_get_noOfPixelColumns()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_noOfPixels():
    if verbose:
        print('Called sys_get_noOfPixels()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_get_noOfPixels()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def sys_mask_pixel(pixel, mask):
    if verbose:
        print('Called sys_mask_pixel() with params:')
        print('    pixel:', pixel)
        print('    mask:', mask)
    try:
        if locking:
            apiLock.acquire()

        if pixel < -2147483648 or pixel > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_mask_pixel', 'pixel', pixel, 'c_int')
            if verbose:
                print('pixel (', pixel, ') is too large for c_int')
            return False

        if mask < 0 or mask > 1:
            if exception_on_error:
                raise ArgSizeException('sys_mask_pixel', 'mask', mask, 'c_bool')
            if verbose:
                print('mask (', mask, ') is too large for c_bool')
            return False

        result = wrap.LIB.sys_mask_pixel(pixel, mask)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_mask_pixel')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_mask_pixelCoordinate(pixelRow, pixelCol, mask):
    if verbose:
        print('Called sys_mask_pixelCoordinate() with params:')
        print('    pixelRow:', pixelRow)
        print('    pixelCol:', pixelCol)
        print('    mask:', mask)
    try:
        if locking:
            apiLock.acquire()

        if pixelRow < -2147483648 or pixelRow > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_mask_pixelCoordinate', 'pixelRow', pixelRow, 'c_int')
            if verbose:
                print('pixelRow (', pixelRow, ') is too large for c_int')
            return False

        if pixelCol < -2147483648 or pixelCol > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_mask_pixelCoordinate', 'pixelCol', pixelCol, 'c_int')
            if verbose:
                print('pixelCol (', pixelCol, ') is too large for c_int')
            return False

        if mask < 0 or mask > 1:
            if exception_on_error:
                raise ArgSizeException('sys_mask_pixelCoordinate', 'mask', mask, 'c_bool')
            if verbose:
                print('mask (', mask, ') is too large for c_bool')
            return False

        result = wrap.LIB.sys_mask_pixelCoordinate(pixelRow, pixelCol, mask)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_mask_pixelCoordinate')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_mask_pixel(pixel):
    if verbose:
        print('Called sys_get_mask_pixel() with params:')
        print('    pixel:', pixel)
    try:
        if locking:
            apiLock.acquire()

        if pixel < -2147483648 or pixel > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_get_mask_pixel', 'pixel', pixel, 'c_int')
            if verbose:
                print('pixel (', pixel, ') is too large for c_int')
            return False

        mask = c_bool()

        result = wrap.LIB.sys_get_mask_pixel(pixel, mask)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_mask_pixel')
        else:
            args = ArgsOUT()
            args.mask = mask.value
            if verbose:
                print('Got:')
                print('    mask:', mask.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_mask_pixelCoordinate(pixelRow, pixelCol):
    if verbose:
        print('Called sys_get_mask_pixelCoordinate() with params:')
        print('    pixelRow:', pixelRow)
        print('    pixelCol:', pixelCol)
    try:
        if locking:
            apiLock.acquire()

        if pixelRow < -2147483648 or pixelRow > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_get_mask_pixelCoordinate', 'pixelRow', pixelRow, 'c_int')
            if verbose:
                print('pixelRow (', pixelRow, ') is too large for c_int')
            return False

        if pixelCol < -2147483648 or pixelCol > 2147483647:
            if exception_on_error:
                raise ArgSizeException('sys_get_mask_pixelCoordinate', 'pixelCol', pixelCol, 'c_int')
            if verbose:
                print('pixelCol (', pixelCol, ') is too large for c_int')
            return False

        mask = c_bool()

        result = wrap.LIB.sys_get_mask_pixelCoordinate(pixelRow, pixelCol, mask)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_mask_pixelCoordinate')
        else:
            args = ArgsOUT()
            args.mask = mask.value
            if verbose:
                print('Got:')
                print('    mask:', mask.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_reboot():
    if verbose:
        print('Called sys_reboot()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_reboot()
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_reboot')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_udpPort():
    if verbose:
        print('Called sys_get_udpPort()')
    try:
        if locking:
            apiLock.acquire()

        udp_port = c_uint()

        result = wrap.LIB.sys_get_udpPort(udp_port)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_udpPort')
        else:
            args = ArgsOUT()
            args.udp_port = udp_port.value
            if verbose:
                print('Got:')
                print('    udp_port:', udp_port.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_newDeviceIP(val):
    if verbose:
        print('Called sys_set_newDeviceIP() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 4294967295:
            if exception_on_error:
                raise ArgSizeException('sys_set_newDeviceIP', 'val', val, 'c_uint')
            if verbose:
                print('val (', val, ') is too large for c_uint')
            return False

        result = wrap.LIB.sys_set_newDeviceIP(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_newDeviceIP')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_set_newDeviceGateway(val):
    if verbose:
        print('Called sys_set_newDeviceGateway() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 4294967295:
            if exception_on_error:
                raise ArgSizeException('sys_set_newDeviceGateway', 'val', val, 'c_uint')
            if verbose:
                print('val (', val, ') is too large for c_uint')
            return False

        result = wrap.LIB.sys_set_newDeviceGateway(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_newDeviceGateway')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_set_newDeviceNetmask(val):
    if verbose:
        print('Called sys_set_newDeviceNetmask() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 4294967295:
            if exception_on_error:
                raise ArgSizeException('sys_set_newDeviceNetmask', 'val', val, 'c_uint')
            if verbose:
                print('val (', val, ') is too large for c_uint')
            return False

        result = wrap.LIB.sys_set_newDeviceNetmask(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_newDeviceNetmask')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_set_writeNetworkCfg(val):
    if verbose:
        print('Called sys_set_writeNetworkCfg() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('sys_set_writeNetworkCfg', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.sys_set_writeNetworkCfg(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_writeNetworkCfg')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_writeNetworkCfg():
    if verbose:
        print('Called sys_get_writeNetworkCfg()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.sys_get_writeNetworkCfg(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_writeNetworkCfg')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_resetNetworkCfg(val):
    if verbose:
        print('Called sys_set_resetNetworkCfg() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('sys_set_resetNetworkCfg', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.sys_set_resetNetworkCfg(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_resetNetworkCfg')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_resetNetworkCfg():
    if verbose:
        print('Called sys_get_resetNetworkCfg()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.sys_get_resetNetworkCfg(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_resetNetworkCfg')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_fpgaVersion():
    if verbose:
        print('Called sys_get_fpgaVersion()')
    try:
        if locking:
            apiLock.acquire()

        r_word = c_uint()

        result = wrap.LIB.sys_get_fpgaVersion(r_word)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_fpgaVersion')
        else:
            args = ArgsOUT()
            args.r_word = r_word.value
            if verbose:
                print('Got:')
                print('    r_word:', r_word.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_fwVersion():
    if verbose:
        print('Called sys_get_fwVersion()')
    try:
        if locking:
            apiLock.acquire()

        r_word = c_uint()

        result = wrap.LIB.sys_get_fwVersion(r_word)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_fwVersion')
        else:
            args = ArgsOUT()
            args.r_word = r_word.value
            if verbose:
                print('Got:')
                print('    r_word:', r_word.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_enableFtpServer(val):
    if verbose:
        print('Called sys_set_enableFtpServer() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('sys_set_enableFtpServer', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.sys_set_enableFtpServer(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_enableFtpServer')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_enableFtpServer():
    if verbose:
        print('Called sys_get_enableFtpServer()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.sys_get_enableFtpServer(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_enableFtpServer')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_installedAM(amNum, val):
    if verbose:
        print('Called sys_set_installedAM() with params:')
        print('    amNum:', amNum)
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if amNum < 0 or amNum > 255:
            if exception_on_error:
                raise ArgSizeException('sys_set_installedAM', 'amNum', amNum, 'c_ubyte')
            if verbose:
                print('amNum (', amNum, ') is too large for c_ubyte')
            return False

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('sys_set_installedAM', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.sys_set_installedAM(amNum, val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_installedAM')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_installedAM(amNum):
    if verbose:
        print('Called sys_get_installedAM() with params:')
        print('    amNum:', amNum)
    try:
        if locking:
            apiLock.acquire()

        if amNum < 0 or amNum > 255:
            if exception_on_error:
                raise ArgSizeException('sys_get_installedAM', 'amNum', amNum, 'c_ubyte')
            if verbose:
                print('amNum (', amNum, ') is too large for c_ubyte')
            return False

        val = c_bool()

        result = wrap.LIB.sys_get_installedAM(amNum, val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_installedAM')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_set_powerAllAm(val):
    if verbose:
        print('Called sys_set_powerAllAm() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('sys_set_powerAllAm', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.sys_set_powerAllAm(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_powerAllAm')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_powerAllAm():
    if verbose:
        print('Called sys_get_powerAllAm()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.sys_get_powerAllAm(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_powerAllAm')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_resetStatusFlagErrors():
    if verbose:
        print('Called sys_resetStatusFlagErrors()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_resetStatusFlagErrors()
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_resetStatusFlagErrors')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_resetFrameCounts():
    if verbose:
        print('Called sys_resetFrameCounts()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_resetFrameCounts()
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_resetFrameCounts')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_set_resetAllAm(val):
    if verbose:
        print('Called sys_set_resetAllAm() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('sys_set_resetAllAm', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.sys_set_resetAllAm(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_set_resetAllAm')
        return result
    finally:
        if locking:
            apiLock.release()


def sys_get_resetAllAm():
    if verbose:
        print('Called sys_get_resetAllAm()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.sys_get_resetAllAm(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_resetAllAm')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_framesTx():
    if verbose:
        print('Called sys_get_framesTx()')
    try:
        if locking:
            apiLock.acquire()

        val = c_uint()

        result = wrap.LIB.sys_get_framesTx(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_framesTx')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_framesRx():
    if verbose:
        print('Called sys_get_framesRx()')
    try:
        if locking:
            apiLock.acquire()

        val = c_uint()

        result = wrap.LIB.sys_get_framesRx(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('sys_get_framesRx')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def sys_get_numAM():
    if verbose:
        print('Called sys_get_numAM()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_get_numAM()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def sys_reset_GMStats():
    if verbose:
        print('Called sys_reset_GMStats()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.sys_reset_GMStats()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def am_set_active(AM_ID):
    if verbose:
        print('Called am_set_active() with params:')
        print('    AM_ID:', AM_ID)
    try:
        if locking:
            apiLock.acquire()

        if AM_ID < -2147483648 or AM_ID > 2147483647:
            if exception_on_error:
                raise ArgSizeException('am_set_active', 'AM_ID', AM_ID, 'c_int')
            if verbose:
                print('AM_ID (', AM_ID, ') is too large for c_int')
            return False

        result = wrap.LIB.am_set_active(AM_ID)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('am_set_active')
        return result
    finally:
        if locking:
            apiLock.release()


def am_get_active():
    if verbose:
        print('Called am_get_active()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.am_get_active()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def am_set_updateType(AMUpdateType):
    if verbose:
        print('Called am_set_updateType() with params:')
        print('    AMUpdateType:', AMUpdateType)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.am_set_updateType(AMUpdateType)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('am_set_updateType')
        return result
    finally:
        if locking:
            apiLock.release()


def am_get_updateType():
    if verbose:
        print('Called am_get_updateType()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.am_get_updateType()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def am_get_fpgaVersion():
    if verbose:
        print('Called am_get_fpgaVersion()')
    try:
        if locking:
            apiLock.acquire()

        data = c_uint()

        result = wrap.LIB.am_get_fpgaVersion(data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('am_get_fpgaVersion')
        else:
            args = ArgsOUT()
            args.data = data.value
            if verbose:
                print('Got:')
                print('    data:', data.value)
            return args
    finally:
        if locking:
            apiLock.release()


def am_get_muxAddr():
    if verbose:
        print('Called am_get_muxAddr()')
    try:
        if locking:
            apiLock.acquire()

        data = c_uint()

        result = wrap.LIB.am_get_muxAddr(data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('am_get_muxAddr')
        else:
            args = ArgsOUT()
            args.data = data.value
            if verbose:
                print('Got:')
                print('    data:', data.value)
            return args
    finally:
        if locking:
            apiLock.release()


def am_set_muxAddr(data):
    if verbose:
        print('Called am_set_muxAddr() with params:')
        print('    data:', data)
    try:
        if locking:
            apiLock.acquire()

        if data < 0 or data > 4294967295:
            if exception_on_error:
                raise ArgSizeException('am_set_muxAddr', 'data', data, 'c_uint')
            if verbose:
                print('data (', data, ') is too large for c_uint')
            return False

        result = wrap.LIB.am_set_muxAddr(data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('am_set_muxAddr')
        return result
    finally:
        if locking:
            apiLock.release()


def am_get_commErr():
    if verbose:
        print('Called am_get_commErr()')
    try:
        if locking:
            apiLock.acquire()

        errID = c_int32()
        errOwner = c_int32()

        result = wrap.LIB.am_get_commErr(errID, errOwner)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('am_get_commErr')
        else:
            args = ArgsOUT()
            args.errID = wrap.COMMERR_ID(errID.value)
            args.errOwner = wrap.COMMERR_OWNER(errOwner.value)
            if verbose:
                print('Got:')
                print('    errID:', errID.value)
                print('    errOwner:', errOwner.value)
            return args
    finally:
        if locking:
            apiLock.release()


def am_get_fpgaStatus(fpgaStatus):
    if verbose:
        print('Called am_get_fpgaStatus() with params:')
        print('    fpgaStatus:', fpgaStatus)
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.am_get_fpgaStatus(fpgaStatus, val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('am_get_fpgaStatus')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def am_get_frameErr():
    if verbose:
        print('Called am_get_frameErr()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.am_get_frameErr(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('am_get_frameErr')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_active(GM_ID):
    if verbose:
        print('Called gm_set_active() with params:')
        print('    GM_ID:', GM_ID)
    try:
        if locking:
            apiLock.acquire()

        if GM_ID < -2147483648 or GM_ID > 2147483647:
            if exception_on_error:
                raise ArgSizeException('gm_set_active', 'GM_ID', GM_ID, 'c_int')
            if verbose:
                print('GM_ID (', GM_ID, ') is too large for c_int')
            return False

        result = wrap.LIB.gm_set_active(GM_ID)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_active')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_active():
    if verbose:
        print('Called gm_get_active()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_active()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_set_updateType(GMUpdateType):
    if verbose:
        print('Called gm_set_updateType() with params:')
        print('    GMUpdateType:', GMUpdateType)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_set_updateType(GMUpdateType)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_updateType')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_updateType():
    if verbose:
        print('Called gm_get_updateType()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_updateType()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_set_enableNegData(val):
    if verbose:
        print('Called gm_set_enableNegData() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('gm_set_enableNegData', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.gm_set_enableNegData(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_enableNegData')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_enableNegData():
    if verbose:
        print('Called gm_get_enableNegData()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.gm_get_enableNegData(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_enableNegData')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_enableThermalData(val):
    if verbose:
        print('Called gm_set_enableThermalData() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('gm_set_enableThermalData', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.gm_set_enableThermalData(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_enableThermalData')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_enableThermalData():
    if verbose:
        print('Called gm_get_enableThermalData()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.gm_get_enableThermalData(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_enableThermalData')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_get_temperature():
    if verbose:
        print('Called gm_get_temperature()')
    try:
        if locking:
            apiLock.acquire()

        val = c_float()

        result = wrap.LIB.gm_get_temperature(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_temperature')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_enableCathodePulser(val):
    if verbose:
        print('Called gm_set_enableCathodePulser() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('gm_set_enableCathodePulser', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.gm_set_enableCathodePulser(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_enableCathodePulser')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_enableCathodePulser():
    if verbose:
        print('Called gm_get_enableCathodePulser()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.gm_get_enableCathodePulser(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_enableCathodePulser')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_enableAnodePulser(val):
    if verbose:
        print('Called gm_set_enableAnodePulser() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('gm_set_enableAnodePulser', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.gm_set_enableAnodePulser(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_enableAnodePulser')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_enableAnodePulser():
    if verbose:
        print('Called gm_get_enableAnodePulser()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.gm_get_enableAnodePulser(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_enableAnodePulser')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_readoutMode(mode):
    if verbose:
        print('Called gm_set_readoutMode() with params:')
        print('    mode:', mode)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_set_readoutMode(mode)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_readoutMode')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_readoutMode():
    if verbose:
        print('Called gm_get_readoutMode()')
    try:
        if locking:
            apiLock.acquire()

        mode = c_int32()

        result = wrap.LIB.gm_get_readoutMode(mode)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_readoutMode')
        else:
            args = ArgsOUT()
            args.mode = wrap.GMReadoutMode(mode.value)
            if verbose:
                print('Got:')
                print('    mode:', mode.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_cathodeMode(mode):
    if verbose:
        print('Called gm_set_cathodeMode() with params:')
        print('    mode:', mode)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_set_cathodeMode(mode)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_cathodeMode')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_cathodeMode():
    if verbose:
        print('Called gm_get_cathodeMode()')
    try:
        if locking:
            apiLock.acquire()

        mode = c_int32()

        result = wrap.LIB.gm_get_cathodeMode(mode)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_cathodeMode')
        else:
            args = ArgsOUT()
            args.mode = wrap.GMCathodeMode(mode.value)
            if verbose:
                print('Got:')
                print('    mode:', mode.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_pulserFrequency(freq):
    if verbose:
        print('Called gm_set_pulserFrequency() with params:')
        print('    freq:', freq)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_set_pulserFrequency(freq)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_pulserFrequency')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_pulserFrequency():
    if verbose:
        print('Called gm_get_pulserFrequency()')
    try:
        if locking:
            apiLock.acquire()

        freq = c_int32()

        result = wrap.LIB.gm_get_pulserFrequency(freq)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_pulserFrequency')
        else:
            args = ArgsOUT()
            args.freq = wrap.GMPulserFrequency(freq.value)
            if verbose:
                print('Got:')
                print('    freq:', freq.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_pulseCount(pulseCnt):
    if verbose:
        print('Called gm_set_pulseCount() with params:')
        print('    pulseCnt:', pulseCnt)
    try:
        if locking:
            apiLock.acquire()

        if pulseCnt < 0 or pulseCnt > 4294967295:
            if exception_on_error:
                raise ArgSizeException('gm_set_pulseCount', 'pulseCnt', pulseCnt, 'c_uint')
            if verbose:
                print('pulseCnt (', pulseCnt, ') is too large for c_uint')
            return False

        result = wrap.LIB.gm_set_pulseCount(pulseCnt)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_pulseCount')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_pulseCount():
    if verbose:
        print('Called gm_get_pulseCount()')
    try:
        if locking:
            apiLock.acquire()

        pulseCnt = c_uint()

        result = wrap.LIB.gm_get_pulseCount(pulseCnt)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_pulseCount')
        else:
            args = ArgsOUT()
            args.pulseCnt = pulseCnt.value
            if verbose:
                print('Got:')
                print('    pulseCnt:', pulseCnt.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_delayTime(data):
    if verbose:
        print('Called gm_set_delayTime() with params:')
        print('    data:', data)
    try:
        if locking:
            apiLock.acquire()

        if data < 0 or data > 4294967295:
            if exception_on_error:
                raise ArgSizeException('gm_set_delayTime', 'data', data, 'c_uint')
            if verbose:
                print('data (', data, ') is too large for c_uint')
            return False

        result = wrap.LIB.gm_set_delayTime(data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_delayTime')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_delayTime():
    if verbose:
        print('Called gm_get_delayTime()')
    try:
        if locking:
            apiLock.acquire()

        data = c_uint()

        result = wrap.LIB.gm_get_delayTime(data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_delayTime')
        else:
            args = ArgsOUT()
            args.data = data.value
            if verbose:
                print('Got:')
                print('    data:', data.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_timestampRes(data):
    if verbose:
        print('Called gm_set_timestampRes() with params:')
        print('    data:', data)
    try:
        if locking:
            apiLock.acquire()

        if data < 0 or data > 4294967295:
            if exception_on_error:
                raise ArgSizeException('gm_set_timestampRes', 'data', data, 'c_uint')
            if verbose:
                print('data (', data, ') is too large for c_uint')
            return False

        result = wrap.LIB.gm_set_timestampRes(data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_timestampRes')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_timestampRes():
    if verbose:
        print('Called gm_get_timestampRes()')
    try:
        if locking:
            apiLock.acquire()

        data = c_uint()

        result = wrap.LIB.gm_get_timestampRes(data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_timestampRes')
        else:
            args = ArgsOUT()
            args.data = data.value
            if verbose:
                print('Got:')
                print('    data:', data.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_simData(val):
    if verbose:
        print('Called gm_set_simData() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('gm_set_simData', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.gm_set_simData(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_simData')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_simData():
    if verbose:
        print('Called gm_get_simData()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.gm_get_simData(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_simData')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_get_adcTdo():
    if verbose:
        print('Called gm_get_adcTdo()')
    try:
        if locking:
            apiLock.acquire()

        data = c_uint()

        result = wrap.LIB.gm_get_adcTdo(data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_adcTdo')
        else:
            args = ArgsOUT()
            args.data = data.value
            if verbose:
                print('Got:')
                print('    data:', data.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_get_adcPdo():
    if verbose:
        print('Called gm_get_adcPdo()')
    try:
        if locking:
            apiLock.acquire()

        data = c_uint()

        result = wrap.LIB.gm_get_adcPdo(data)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_adcPdo')
        else:
            args = ArgsOUT()
            args.data = data.value
            if verbose:
                print('Got:')
                print('    data:', data.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_disablePackets(val):
    if verbose:
        print('Called gm_set_disablePackets() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('gm_set_disablePackets', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.gm_set_disablePackets(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_disablePackets')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_disablePackets():
    if verbose:
        print('Called gm_get_disablePackets()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.gm_get_disablePackets(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_disablePackets')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_rebootAsic(val):
    if verbose:
        print('Called gm_set_rebootAsic() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('gm_set_rebootAsic', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.gm_set_rebootAsic(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_rebootAsic')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_rebootAsic():
    if verbose:
        print('Called gm_get_rebootAsic()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.gm_get_rebootAsic(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_rebootAsic')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_reloadAsic(val):
    if verbose:
        print('Called gm_set_reloadAsic() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('gm_set_reloadAsic', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.gm_set_reloadAsic(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_reloadAsic')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_reloadAsic():
    if verbose:
        print('Called gm_get_reloadAsic()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.gm_get_reloadAsic(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_reloadAsic')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_testAsic(val):
    if verbose:
        print('Called gm_set_testAsic() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('gm_set_testAsic', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.gm_set_testAsic(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_testAsic')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_testAsic():
    if verbose:
        print('Called gm_get_testAsic()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.gm_get_testAsic(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_testAsic')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_set_powerAsic(val):
    if verbose:
        print('Called gm_set_powerAsic() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('gm_set_powerAsic', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.gm_set_powerAsic(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_set_powerAsic')
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_powerAsic():
    if verbose:
        print('Called gm_get_powerAsic()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.gm_get_powerAsic(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('gm_get_powerAsic')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def gm_get_numPackets():
    if verbose:
        print('Called gm_get_numPackets()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numPackets()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numTriggeredPhotons():
    if verbose:
        print('Called gm_get_numTriggeredPhotons()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numTriggeredPhotons()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def gm_get_numTotalPhotons():
    if verbose:
        print('Called gm_get_numTotalPhotons()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.gm_get_numTotalPhotons()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def asic_send_globalData():
    if verbose:
        print('Called asic_send_globalData()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_send_globalData()
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_send_globalData')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_set_analogOutputMonitored(output):
    if verbose:
        print('Called asic_set_analogOutputMonitored() with params:')
        print('    output:', output)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_analogOutputMonitored(output)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_analogOutputMonitored')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_analogOutputMonitored():
    if verbose:
        print('Called asic_get_analogOutputMonitored()')
    try:
        if locking:
            apiLock.acquire()

        output = c_int32()

        result = wrap.LIB.asic_get_analogOutputMonitored(output)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_analogOutputMonitored')
        else:
            args = ArgsOUT()
            args.output = wrap.AnalogOutput(output.value)
            if verbose:
                print('Got:')
                print('    output:', output.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_globalOptions(options):
    if verbose:
        print('Called asic_set_globalOptions() with params:')
        print('    options:', options)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_globalOptions(options)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_globalOptions')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_globalOptions():
    if verbose:
        print('Called asic_get_globalOptions()')
    try:
        if locking:
            apiLock.acquire()

        options = wrap.ASICGlobalOptions()

        result = wrap.LIB.asic_get_globalOptions(options)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_globalOptions')
        else:
            args = ArgsOUT()
            args.options = options.value
            if verbose:
                print('Got:')
                print('    options:', options.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_anodeInternalLeakageCurrentGenerator(currGen):
    if verbose:
        print('Called asic_set_anodeInternalLeakageCurrentGenerator() with params:')
        print('    currGen:', currGen)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_anodeInternalLeakageCurrentGenerator(currGen)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_anodeInternalLeakageCurrentGenerator')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_anodeInternalLeakageCurrentGenerator():
    if verbose:
        print('Called asic_get_anodeInternalLeakageCurrentGenerator()')
    try:
        if locking:
            apiLock.acquire()

        currGen = c_int32()

        result = wrap.LIB.asic_get_anodeInternalLeakageCurrentGenerator(currGen)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_anodeInternalLeakageCurrentGenerator')
        else:
            args = ArgsOUT()
            args.currGen = wrap.InternalLeakageCurrentGenerator(currGen.value)
            if verbose:
                print('Got:')
                print('    currGen:', currGen.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_timingChannelUnipolarGain(gain):
    if verbose:
        print('Called asic_set_timingChannelUnipolarGain() with params:')
        print('    gain:', gain)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_timingChannelUnipolarGain(gain)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_timingChannelUnipolarGain')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_timingChannelUnipolarGain():
    if verbose:
        print('Called asic_get_timingChannelUnipolarGain()')
    try:
        if locking:
            apiLock.acquire()

        gain = c_int32()

        result = wrap.LIB.asic_get_timingChannelUnipolarGain(gain)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_timingChannelUnipolarGain')
        else:
            args = ArgsOUT()
            args.gain = wrap.TimingChannelUnipolarGain(gain.value)
            if verbose:
                print('Got:')
                print('    gain:', gain.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_multipleFiringSuppressTime(suppressTime):
    if verbose:
        print('Called asic_set_multipleFiringSuppressTime() with params:')
        print('    suppressTime:', suppressTime)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_multipleFiringSuppressTime(suppressTime)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_multipleFiringSuppressTime')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_multipleFiringSuppressTime():
    if verbose:
        print('Called asic_get_multipleFiringSuppressTime()')
    try:
        if locking:
            apiLock.acquire()

        suppressTime = c_int32()

        result = wrap.LIB.asic_get_multipleFiringSuppressTime(suppressTime)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_multipleFiringSuppressTime')
        else:
            args = ArgsOUT()
            args.suppressTime = wrap.MultipleFiringSuppressionTime(suppressTime.value)
            if verbose:
                print('Got:')
                print('    suppressTime:', suppressTime.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_timingChannelBiPolarGain(gain):
    if verbose:
        print('Called asic_set_timingChannelBiPolarGain() with params:')
        print('    gain:', gain)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_timingChannelBiPolarGain(gain)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_timingChannelBiPolarGain')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_timingChannelBiPolarGain():
    if verbose:
        print('Called asic_get_timingChannelBiPolarGain()')
    try:
        if locking:
            apiLock.acquire()

        gain = c_int32()

        result = wrap.LIB.asic_get_timingChannelBiPolarGain(gain)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_timingChannelBiPolarGain')
        else:
            args = ArgsOUT()
            args.gain = wrap.TimingChannelBipolarGain(gain.value)
            if verbose:
                print('Got:')
                print('    gain:', gain.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_readoutMode(mode):
    if verbose:
        print('Called asic_set_readoutMode() with params:')
        print('    mode:', mode)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_readoutMode(mode)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_readoutMode')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_readoutMode():
    if verbose:
        print('Called asic_get_readoutMode()')
    try:
        if locking:
            apiLock.acquire()

        mode = c_int32()

        result = wrap.LIB.asic_get_readoutMode(mode)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_readoutMode')
        else:
            args = ArgsOUT()
            args.mode = wrap.GMASICReadoutMode(mode.value)
            if verbose:
                print('Got:')
                print('    mode:', mode.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_channelGain(again, cgain):
    if verbose:
        print('Called asic_set_channelGain() with params:')
        print('    again:', again)
        print('    cgain:', cgain)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_channelGain(again, cgain)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_channelGain')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_channelGain():
    if verbose:
        print('Called asic_get_channelGain()')
    try:
        if locking:
            apiLock.acquire()

        again = c_int32()
        cgain = c_int32()

        result = wrap.LIB.asic_get_channelGain(again, cgain)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_channelGain')
        else:
            args = ArgsOUT()
            args.again = wrap.AnodeChannelGain(again.value)
            args.cgain = wrap.CathodeChannelGain(cgain.value)
            if verbose:
                print('Got:')
                print('    again:', again.value)
                print('    cgain:', cgain.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_testPulse(xx_type, pulseInmV):
    if verbose:
        print('Called asic_set_testPulse() with params:')
        print('    xx_type:', xx_type)
        print('    pulseInmV:', pulseInmV)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_testPulse(xx_type, pulseInmV)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_testPulse')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_testPulse(xx_type):
    if verbose:
        print('Called asic_get_testPulse() with params:')
        print('    xx_type:', xx_type)
    try:
        if locking:
            apiLock.acquire()

        pulseInmV = c_float()

        result = wrap.LIB.asic_get_testPulse(xx_type, pulseInmV)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_testPulse')
        else:
            args = ArgsOUT()
            args.pulseInmV = pulseInmV.value
            if verbose:
                print('Got:')
                print('    pulseInmV:', pulseInmV.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_anodeTestPulseEdge(edge):
    if verbose:
        print('Called asic_set_anodeTestPulseEdge() with params:')
        print('    edge:', edge)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_anodeTestPulseEdge(edge)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_anodeTestPulseEdge')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_anodeTestPulseEdge():
    if verbose:
        print('Called asic_get_anodeTestPulseEdge()')
    try:
        if locking:
            apiLock.acquire()

        edge = c_int32()

        result = wrap.LIB.asic_get_anodeTestPulseEdge(edge)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_anodeTestPulseEdge')
        else:
            args = ArgsOUT()
            args.edge = wrap.TestPulseEdge(edge.value)
            if verbose:
                print('Got:')
                print('    edge:', edge.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_cathodeTestSigSrc(sigSrc):
    if verbose:
        print('Called asic_set_cathodeTestSigSrc() with params:')
        print('    sigSrc:', sigSrc)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_cathodeTestSigSrc(sigSrc)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_cathodeTestSigSrc')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_cathodeTestSigSrc():
    if verbose:
        print('Called asic_get_cathodeTestSigSrc()')
    try:
        if locking:
            apiLock.acquire()

        sigSrc = c_int32()

        result = wrap.LIB.asic_get_cathodeTestSigSrc(sigSrc)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_cathodeTestSigSrc')
        else:
            args = ArgsOUT()
            args.sigSrc = wrap.CathodeTestSigSrc(sigSrc.value)
            if verbose:
                print('Got:')
                print('    sigSrc:', sigSrc.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_cathodeTestSigType(sigType):
    if verbose:
        print('Called asic_set_cathodeTestSigType() with params:')
        print('    sigType:', sigType)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_cathodeTestSigType(sigType)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_cathodeTestSigType')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_cathodeTestSigType():
    if verbose:
        print('Called asic_get_cathodeTestSigType()')
    try:
        if locking:
            apiLock.acquire()

        sigType = c_int32()

        result = wrap.LIB.asic_get_cathodeTestSigType(sigType)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_cathodeTestSigType')
        else:
            args = ArgsOUT()
            args.sigType = wrap.TestSigType(sigType.value)
            if verbose:
                print('Got:')
                print('    sigType:', sigType.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_peakingTime(xx_type, peakingTimeInMicroSeconds):
    if verbose:
        print('Called asic_set_peakingTime() with params:')
        print('    xx_type:', xx_type)
        print('    peakingTimeInMicroSeconds:', peakingTimeInMicroSeconds)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_peakingTime(xx_type, peakingTimeInMicroSeconds)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_peakingTime')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_peakingTime(xx_type):
    if verbose:
        print('Called asic_get_peakingTime() with params:')
        print('    xx_type:', xx_type)
    try:
        if locking:
            apiLock.acquire()

        peakingTimeInMicroSeconds = c_float()

        result = wrap.LIB.asic_get_peakingTime(xx_type, peakingTimeInMicroSeconds)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_peakingTime')
        else:
            args = ArgsOUT()
            args.peakingTimeInMicroSeconds = peakingTimeInMicroSeconds.value
            if verbose:
                print('Got:')
                print('    peakingTimeInMicroSeconds:', peakingTimeInMicroSeconds.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_peakDetectTimeout(xx_type, timeoutInMicroSeconds):
    if verbose:
        print('Called asic_set_peakDetectTimeout() with params:')
        print('    xx_type:', xx_type)
        print('    timeoutInMicroSeconds:', timeoutInMicroSeconds)
    try:
        if locking:
            apiLock.acquire()

        if timeoutInMicroSeconds < -2147483648 or timeoutInMicroSeconds > 2147483647:
            if exception_on_error:
                raise ArgSizeException('asic_set_peakDetectTimeout', 'timeoutInMicroSeconds', timeoutInMicroSeconds, 'c_int')
            if verbose:
                print('timeoutInMicroSeconds (', timeoutInMicroSeconds, ') is too large for c_int')
            return False

        result = wrap.LIB.asic_set_peakDetectTimeout(xx_type, timeoutInMicroSeconds)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_peakDetectTimeout')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_peakDetectTimeout(xx_type):
    if verbose:
        print('Called asic_get_peakDetectTimeout() with params:')
        print('    xx_type:', xx_type)
    try:
        if locking:
            apiLock.acquire()

        timeoutInMicroSeconds = c_int()

        result = wrap.LIB.asic_get_peakDetectTimeout(xx_type, timeoutInMicroSeconds)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_peakDetectTimeout')
        else:
            args = ArgsOUT()
            args.timeoutInMicroSeconds = timeoutInMicroSeconds.value
            if verbose:
                print('Got:')
                print('    timeoutInMicroSeconds:', timeoutInMicroSeconds.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_timeDetectRampLength(xx_type, rampLengthInMicroSeconds):
    if verbose:
        print('Called asic_set_timeDetectRampLength() with params:')
        print('    xx_type:', xx_type)
        print('    rampLengthInMicroSeconds:', rampLengthInMicroSeconds)
    try:
        if locking:
            apiLock.acquire()

        if rampLengthInMicroSeconds < -2147483648 or rampLengthInMicroSeconds > 2147483647:
            if exception_on_error:
                raise ArgSizeException('asic_set_timeDetectRampLength', 'rampLengthInMicroSeconds', rampLengthInMicroSeconds, 'c_int')
            if verbose:
                print('rampLengthInMicroSeconds (', rampLengthInMicroSeconds, ') is too large for c_int')
            return False

        result = wrap.LIB.asic_set_timeDetectRampLength(xx_type, rampLengthInMicroSeconds)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_timeDetectRampLength')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_timeDetectRampLength(xx_type):
    if verbose:
        print('Called asic_get_timeDetectRampLength() with params:')
        print('    xx_type:', xx_type)
    try:
        if locking:
            apiLock.acquire()

        rampLengthInMicroSeconds = c_int()

        result = wrap.LIB.asic_get_timeDetectRampLength(xx_type, rampLengthInMicroSeconds)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_timeDetectRampLength')
        else:
            args = ArgsOUT()
            args.rampLengthInMicroSeconds = rampLengthInMicroSeconds.value
            if verbose:
                print('Got:')
                print('    rampLengthInMicroSeconds:', rampLengthInMicroSeconds.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_cathodeTimingChannelsShaperPeakingTime(peakingTime):
    if verbose:
        print('Called asic_set_cathodeTimingChannelsShaperPeakingTime() with params:')
        print('    peakingTime:', peakingTime)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_cathodeTimingChannelsShaperPeakingTime(peakingTime)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_cathodeTimingChannelsShaperPeakingTime')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_cathodeTimingChannelsShaperPeakingTime():
    if verbose:
        print('Called asic_get_cathodeTimingChannelsShaperPeakingTime()')
    try:
        if locking:
            apiLock.acquire()

        peakingTime = c_int32()

        result = wrap.LIB.asic_get_cathodeTimingChannelsShaperPeakingTime(peakingTime)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_cathodeTimingChannelsShaperPeakingTime')
        else:
            args = ArgsOUT()
            args.peakingTime = wrap.TimingChannelsShaperPeakingTime(peakingTime.value)
            if verbose:
                print('Got:')
                print('    peakingTime:', peakingTime.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement(displacementInmV):
    if verbose:
        print('Called asic_set_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement() with params:')
        print('    displacementInmV:', displacementInmV)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement(displacementInmV)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement():
    if verbose:
        print('Called asic_get_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement()')
    try:
        if locking:
            apiLock.acquire()

        displacementInmV = c_float()

        result = wrap.LIB.asic_get_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement(displacementInmV)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement')
        else:
            args = ArgsOUT()
            args.displacementInmV = displacementInmV.value
            if verbose:
                print('Got:')
                print('    displacementInmV:', displacementInmV.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_channelThreshold(xx_type, thresholdInmV):
    if verbose:
        print('Called asic_set_channelThreshold() with params:')
        print('    xx_type:', xx_type)
        print('    thresholdInmV:', thresholdInmV)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_channelThreshold(xx_type, thresholdInmV)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_channelThreshold')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_channelThreshold(xx_type):
    if verbose:
        print('Called asic_get_channelThreshold() with params:')
        print('    xx_type:', xx_type)
    try:
        if locking:
            apiLock.acquire()

        thresholdInmV = c_float()

        result = wrap.LIB.asic_get_channelThreshold(xx_type, thresholdInmV)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_channelThreshold')
        else:
            args = ArgsOUT()
            args.thresholdInmV = thresholdInmV.value
            if verbose:
                print('Got:')
                print('    thresholdInmV:', thresholdInmV.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_cathodeChannelInternalLeakageCurrentGenerator(channelNumber, currGen):
    if verbose:
        print('Called asic_set_cathodeChannelInternalLeakageCurrentGenerator() with params:')
        print('    channelNumber:', channelNumber)
        print('    currGen:', currGen)
    try:
        if locking:
            apiLock.acquire()

        if channelNumber < -2147483648 or channelNumber > 2147483647:
            if exception_on_error:
                raise ArgSizeException('asic_set_cathodeChannelInternalLeakageCurrentGenerator', 'channelNumber', channelNumber, 'c_int')
            if verbose:
                print('channelNumber (', channelNumber, ') is too large for c_int')
            return False

        result = wrap.LIB.asic_set_cathodeChannelInternalLeakageCurrentGenerator(channelNumber, currGen)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_cathodeChannelInternalLeakageCurrentGenerator')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_cathodeChannelInternalLeakageCurrentGenerator(channelNumber):
    if verbose:
        print('Called asic_get_cathodeChannelInternalLeakageCurrentGenerator() with params:')
        print('    channelNumber:', channelNumber)
    try:
        if locking:
            apiLock.acquire()

        if channelNumber < -2147483648 or channelNumber > 2147483647:
            if exception_on_error:
                raise ArgSizeException('asic_get_cathodeChannelInternalLeakageCurrentGenerator', 'channelNumber', channelNumber, 'c_int')
            if verbose:
                print('channelNumber (', channelNumber, ') is too large for c_int')
            return False

        currGen = c_int32()

        result = wrap.LIB.asic_get_cathodeChannelInternalLeakageCurrentGenerator(channelNumber, currGen)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_cathodeChannelInternalLeakageCurrentGenerator')
        else:
            args = ArgsOUT()
            args.currGen = wrap.CathodeInternalLeakageCurrentGenerator(currGen.value)
            if verbose:
                print('Got:')
                print('    currGen:', currGen.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_anodeChannelMonitored(channel):
    if verbose:
        print('Called asic_set_anodeChannelMonitored() with params:')
        print('    channel:', channel)
    try:
        if locking:
            apiLock.acquire()

        if channel < -2147483648 or channel > 2147483647:
            if exception_on_error:
                raise ArgSizeException('asic_set_anodeChannelMonitored', 'channel', channel, 'c_int')
            if verbose:
                print('channel (', channel, ') is too large for c_int')
            return False

        result = wrap.LIB.asic_set_anodeChannelMonitored(channel)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_anodeChannelMonitored')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_anodeChannelMonitored():
    if verbose:
        print('Called asic_get_anodeChannelMonitored()')
    try:
        if locking:
            apiLock.acquire()

        channel = c_int()

        result = wrap.LIB.asic_get_anodeChannelMonitored(channel)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_anodeChannelMonitored')
        else:
            args = ArgsOUT()
            args.channel = channel.value
            if verbose:
                print('Got:')
                print('    channel:', channel.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_cathodeEnergyTimingMonitored(energyTiming):
    if verbose:
        print('Called asic_set_cathodeEnergyTimingMonitored() with params:')
        print('    energyTiming:', energyTiming)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_cathodeEnergyTimingMonitored(energyTiming)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_cathodeEnergyTimingMonitored')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_cathodeEnergyTimingMonitored():
    if verbose:
        print('Called asic_get_cathodeEnergyTimingMonitored()')
    try:
        if locking:
            apiLock.acquire()

        energyTiming = c_int32()

        result = wrap.LIB.asic_get_cathodeEnergyTimingMonitored(energyTiming)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_cathodeEnergyTimingMonitored')
        else:
            args = ArgsOUT()
            args.energyTiming = wrap.CathodeEnergyTiming(energyTiming.value)
            if verbose:
                print('Got:')
                print('    energyTiming:', energyTiming.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_set_DACMonitored(dac):
    if verbose:
        print('Called asic_set_DACMonitored() with params:')
        print('    dac:', dac)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_set_DACMonitored(dac)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_set_DACMonitored')
        return result
    finally:
        if locking:
            apiLock.release()


def asic_get_DACMonitored():
    if verbose:
        print('Called asic_get_DACMonitored()')
    try:
        if locking:
            apiLock.acquire()

        dac = c_int32()

        result = wrap.LIB.asic_get_DACMonitored(dac)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_get_DACMonitored')
        else:
            args = ArgsOUT()
            args.dac = wrap.DACS(dac.value)
            if verbose:
                print('Got:')
                print('    dac:', dac.value)
            return args
    finally:
        if locking:
            apiLock.release()


def asic_send_channelData():
    if verbose:
        print('Called asic_send_channelData()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.asic_send_channelData()
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('asic_send_channelData')
        return result
    finally:
        if locking:
            apiLock.release()


def channel_get_updateType():
    if verbose:
        print('Called channel_get_updateType()')
    try:
        if locking:
            apiLock.acquire()

        channelUpdateType = c_int32()

        result = wrap.LIB.channel_get_updateType(channelUpdateType)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_get_updateType')
        else:
            args = ArgsOUT()
            args.channelUpdateType = wrap.ChannelUpdateType(channelUpdateType.value)
            if verbose:
                print('Got:')
                print('    channelUpdateType:', channelUpdateType.value)
            return args
    finally:
        if locking:
            apiLock.release()


def channel_set_updateType(channelUpdateType):
    if verbose:
        print('Called channel_set_updateType() with params:')
        print('    channelUpdateType:', channelUpdateType)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.channel_set_updateType(channelUpdateType)
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def channel_get_activeType():
    if verbose:
        print('Called channel_get_activeType()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.channel_get_activeType()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def channel_set_activeType(channelType):
    if verbose:
        print('Called channel_set_activeType() with params:')
        print('    channelType:', channelType)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.channel_set_activeType(channelType)
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()


def channel_get_active():
    if verbose:
        print('Called channel_get_active()')
    try:
        if locking:
            apiLock.acquire()

        channel = c_int()

        result = wrap.LIB.channel_get_active(channel)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_get_active')
        else:
            args = ArgsOUT()
            args.channel = channel.value
            if verbose:
                print('Got:')
                print('    channel:', channel.value)
            return args
    finally:
        if locking:
            apiLock.release()


def channel_set_active(channel):
    if verbose:
        print('Called channel_set_active() with params:')
        print('    channel:', channel)
    try:
        if locking:
            apiLock.acquire()

        if channel < -2147483648 or channel > 2147483647:
            if exception_on_error:
                raise ArgSizeException('channel_set_active', 'channel', channel, 'c_int')
            if verbose:
                print('channel (', channel, ') is too large for c_int')
            return False

        result = wrap.LIB.channel_set_active(channel)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_set_active')
        return result
    finally:
        if locking:
            apiLock.release()


def channel_set_cpd(val):
    if verbose:
        print('Called channel_set_cpd() with params:')
        print('    val:', val)
    try:
        if locking:
            apiLock.acquire()

        if val < 0 or val > 1:
            if exception_on_error:
                raise ArgSizeException('channel_set_cpd', 'val', val, 'c_bool')
            if verbose:
                print('val (', val, ') is too large for c_bool')
            return False

        result = wrap.LIB.channel_set_cpd(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_set_cpd')
        return result
    finally:
        if locking:
            apiLock.release()


def channel_get_cpd(channelNumber):
    if verbose:
        print('Called channel_get_cpd() with params:')
        print('    channelNumber:', channelNumber)
    try:
        if locking:
            apiLock.acquire()

        if channelNumber < -2147483648 or channelNumber > 2147483647:
            if exception_on_error:
                raise ArgSizeException('channel_get_cpd', 'channelNumber', channelNumber, 'c_int')
            if verbose:
                print('channelNumber (', channelNumber, ') is too large for c_int')
            return False

        val = c_bool()

        result = wrap.LIB.channel_get_cpd(channelNumber, val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_get_cpd')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def channel_set_mask(mask):
    if verbose:
        print('Called channel_set_mask() with params:')
        print('    mask:', mask)
    try:
        if locking:
            apiLock.acquire()

        if mask < 0 or mask > 1:
            if exception_on_error:
                raise ArgSizeException('channel_set_mask', 'mask', mask, 'c_bool')
            if verbose:
                print('mask (', mask, ') is too large for c_bool')
            return False

        result = wrap.LIB.channel_set_mask(mask)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_set_mask')
        return result
    finally:
        if locking:
            apiLock.release()


def channel_get_mask(xx_type, channelNumber):
    if verbose:
        print('Called channel_get_mask() with params:')
        print('    xx_type:', xx_type)
        print('    channelNumber:', channelNumber)
    try:
        if locking:
            apiLock.acquire()

        if channelNumber < -2147483648 or channelNumber > 2147483647:
            if exception_on_error:
                raise ArgSizeException('channel_get_mask', 'channelNumber', channelNumber, 'c_int')
            if verbose:
                print('channelNumber (', channelNumber, ') is too large for c_int')
            return False

        mask = c_bool()

        result = wrap.LIB.channel_get_mask(xx_type, channelNumber, mask)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_get_mask')
        else:
            args = ArgsOUT()
            args.mask = mask.value
            if verbose:
                print('Got:')
                print('    mask:', mask.value)
            return args
    finally:
        if locking:
            apiLock.release()


def channel_set_enableTestCapacitor(enable):
    if verbose:
        print('Called channel_set_enableTestCapacitor() with params:')
        print('    enable:', enable)
    try:
        if locking:
            apiLock.acquire()

        if enable < 0 or enable > 1:
            if exception_on_error:
                raise ArgSizeException('channel_set_enableTestCapacitor', 'enable', enable, 'c_bool')
            if verbose:
                print('enable (', enable, ') is too large for c_bool')
            return False

        result = wrap.LIB.channel_set_enableTestCapacitor(enable)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_set_enableTestCapacitor')
        return result
    finally:
        if locking:
            apiLock.release()


def channel_get_enableTestCapacitor(xx_type, channelNumber):
    if verbose:
        print('Called channel_get_enableTestCapacitor() with params:')
        print('    xx_type:', xx_type)
        print('    channelNumber:', channelNumber)
    try:
        if locking:
            apiLock.acquire()

        if channelNumber < -2147483648 or channelNumber > 2147483647:
            if exception_on_error:
                raise ArgSizeException('channel_get_enableTestCapacitor', 'channelNumber', channelNumber, 'c_int')
            if verbose:
                print('channelNumber (', channelNumber, ') is too large for c_int')
            return False

        enabled = c_bool()

        result = wrap.LIB.channel_get_enableTestCapacitor(xx_type, channelNumber, enabled)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_get_enableTestCapacitor')
        else:
            args = ArgsOUT()
            args.enabled = enabled.value
            if verbose:
                print('Got:')
                print('    enabled:', enabled.value)
            return args
    finally:
        if locking:
            apiLock.release()


def channel_set_anodeSignalMonitored(signal):
    if verbose:
        print('Called channel_set_anodeSignalMonitored() with params:')
        print('    signal:', signal)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.channel_set_anodeSignalMonitored(signal)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_set_anodeSignalMonitored')
        return result
    finally:
        if locking:
            apiLock.release()


def channel_get_anodeSignalMonitored(channelNumber):
    if verbose:
        print('Called channel_get_anodeSignalMonitored() with params:')
        print('    channelNumber:', channelNumber)
    try:
        if locking:
            apiLock.acquire()

        if channelNumber < -2147483648 or channelNumber > 2147483647:
            if exception_on_error:
                raise ArgSizeException('channel_get_anodeSignalMonitored', 'channelNumber', channelNumber, 'c_int')
            if verbose:
                print('channelNumber (', channelNumber, ') is too large for c_int')
            return False

        signal = c_int32()

        result = wrap.LIB.channel_get_anodeSignalMonitored(channelNumber, signal)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_get_anodeSignalMonitored')
        else:
            args = ArgsOUT()
            args.signal = wrap.Signal(signal.value)
            if verbose:
                print('Got:')
                print('    signal:', signal.value)
            return args
    finally:
        if locking:
            apiLock.release()


def channel_set_cathodeShapedTimingSignal(signal):
    if verbose:
        print('Called channel_set_cathodeShapedTimingSignal() with params:')
        print('    signal:', signal)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.channel_set_cathodeShapedTimingSignal(signal)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_set_cathodeShapedTimingSignal')
        return result
    finally:
        if locking:
            apiLock.release()


def channel_get_cathodeShapedTimingSignal(channelNumber):
    if verbose:
        print('Called channel_get_cathodeShapedTimingSignal() with params:')
        print('    channelNumber:', channelNumber)
    try:
        if locking:
            apiLock.acquire()

        if channelNumber < -2147483648 or channelNumber > 2147483647:
            if exception_on_error:
                raise ArgSizeException('channel_get_cathodeShapedTimingSignal', 'channelNumber', channelNumber, 'c_int')
            if verbose:
                print('channelNumber (', channelNumber, ') is too large for c_int')
            return False

        signal = c_int32()

        result = wrap.LIB.channel_get_cathodeShapedTimingSignal(channelNumber, signal)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_get_cathodeShapedTimingSignal')
        else:
            args = ArgsOUT()
            args.signal = wrap.CathodeShapedTimingSignal(signal.value)
            if verbose:
                print('Got:')
                print('    signal:', signal.value)
            return args
    finally:
        if locking:
            apiLock.release()


def channel_set_positivePulseThresholdTrim(trimInmV):
    if verbose:
        print('Called channel_set_positivePulseThresholdTrim() with params:')
        print('    trimInmV:', trimInmV)
    try:
        if locking:
            apiLock.acquire()

        if trimInmV < -2147483648 or trimInmV > 2147483647:
            if exception_on_error:
                raise ArgSizeException('channel_set_positivePulseThresholdTrim', 'trimInmV', trimInmV, 'c_int')
            if verbose:
                print('trimInmV (', trimInmV, ') is too large for c_int')
            return False

        result = wrap.LIB.channel_set_positivePulseThresholdTrim(trimInmV)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_set_positivePulseThresholdTrim')
        return result
    finally:
        if locking:
            apiLock.release()


def channel_get_positivePulseThresholdTrim(channelType, channelNumber):
    if verbose:
        print('Called channel_get_positivePulseThresholdTrim() with params:')
        print('    channelType:', channelType)
        print('    channelNumber:', channelNumber)
    try:
        if locking:
            apiLock.acquire()

        if channelNumber < -2147483648 or channelNumber > 2147483647:
            if exception_on_error:
                raise ArgSizeException('channel_get_positivePulseThresholdTrim', 'channelNumber', channelNumber, 'c_int')
            if verbose:
                print('channelNumber (', channelNumber, ') is too large for c_int')
            return False

        trimInmV = c_int()

        result = wrap.LIB.channel_get_positivePulseThresholdTrim(channelType, channelNumber, trimInmV)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_get_positivePulseThresholdTrim')
        else:
            args = ArgsOUT()
            args.trimInmV = trimInmV.value
            if verbose:
                print('Got:')
                print('    trimInmV:', trimInmV.value)
            return args
    finally:
        if locking:
            apiLock.release()


def channel_set_anodeNegativePulseThresholdTrim(trimInmV):
    if verbose:
        print('Called channel_set_anodeNegativePulseThresholdTrim() with params:')
        print('    trimInmV:', trimInmV)
    try:
        if locking:
            apiLock.acquire()

        if trimInmV < -2147483648 or trimInmV > 2147483647:
            if exception_on_error:
                raise ArgSizeException('channel_set_anodeNegativePulseThresholdTrim', 'trimInmV', trimInmV, 'c_int')
            if verbose:
                print('trimInmV (', trimInmV, ') is too large for c_int')
            return False

        result = wrap.LIB.channel_set_anodeNegativePulseThresholdTrim(trimInmV)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_set_anodeNegativePulseThresholdTrim')
        return result
    finally:
        if locking:
            apiLock.release()


def channel_get_anodeNegativePulseThresholdTrim(channelNumber):
    if verbose:
        print('Called channel_get_anodeNegativePulseThresholdTrim() with params:')
        print('    channelNumber:', channelNumber)
    try:
        if locking:
            apiLock.acquire()

        if channelNumber < -2147483648 or channelNumber > 2147483647:
            if exception_on_error:
                raise ArgSizeException('channel_get_anodeNegativePulseThresholdTrim', 'channelNumber', channelNumber, 'c_int')
            if verbose:
                print('channelNumber (', channelNumber, ') is too large for c_int')
            return False

        trimInmV = c_int()

        result = wrap.LIB.channel_get_anodeNegativePulseThresholdTrim(channelNumber, trimInmV)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_get_anodeNegativePulseThresholdTrim')
        else:
            args = ArgsOUT()
            args.trimInmV = trimInmV.value
            if verbose:
                print('Got:')
                print('    trimInmV:', trimInmV.value)
            return args
    finally:
        if locking:
            apiLock.release()


def channel_set_cathodeTimingMode(mode):
    if verbose:
        print('Called channel_set_cathodeTimingMode() with params:')
        print('    mode:', mode)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.channel_set_cathodeTimingMode(mode)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_set_cathodeTimingMode')
        return result
    finally:
        if locking:
            apiLock.release()


def channel_get_cathodeTimingMode(channelNumber):
    if verbose:
        print('Called channel_get_cathodeTimingMode() with params:')
        print('    channelNumber:', channelNumber)
    try:
        if locking:
            apiLock.acquire()

        if channelNumber < -2147483648 or channelNumber > 2147483647:
            if exception_on_error:
                raise ArgSizeException('channel_get_cathodeTimingMode', 'channelNumber', channelNumber, 'c_int')
            if verbose:
                print('channelNumber (', channelNumber, ') is too large for c_int')
            return False

        mode = c_int32()

        result = wrap.LIB.channel_get_cathodeTimingMode(channelNumber, mode)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_get_cathodeTimingMode')
        else:
            args = ArgsOUT()
            args.mode = wrap.CathodeTimingMode(mode.value)
            if verbose:
                print('Got:')
                print('    mode:', mode.value)
            return args
    finally:
        if locking:
            apiLock.release()


def channel_set_cathodeTimingTrim(channelType, trimInmV):
    if verbose:
        print('Called channel_set_cathodeTimingTrim() with params:')
        print('    channelType:', channelType)
        print('    trimInmV:', trimInmV)
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.channel_set_cathodeTimingTrim(channelType, trimInmV)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_set_cathodeTimingTrim')
        return result
    finally:
        if locking:
            apiLock.release()


def channel_get_cathodeTimingTrim(channelNumber, channelType):
    if verbose:
        print('Called channel_get_cathodeTimingTrim() with params:')
        print('    channelNumber:', channelNumber)
        print('    channelType:', channelType)
    try:
        if locking:
            apiLock.acquire()

        if channelNumber < -2147483648 or channelNumber > 2147483647:
            if exception_on_error:
                raise ArgSizeException('channel_get_cathodeTimingTrim', 'channelNumber', channelNumber, 'c_int')
            if verbose:
                print('channelNumber (', channelNumber, ') is too large for c_int')
            return False

        trimInmV = c_double()

        result = wrap.LIB.channel_get_cathodeTimingTrim(channelNumber, channelType, trimInmV)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('channel_get_cathodeTimingTrim')
        else:
            args = ArgsOUT()
            args.trimInmV = trimInmV.value
            if verbose:
                print('Got:')
                print('    trimInmV:', trimInmV.value)
            return args
    finally:
        if locking:
            apiLock.release()


def collect_timed_start(collectionTimeInSeconds):
    if verbose:
        print('Called collect_timed_start() with params:')
        print('    collectionTimeInSeconds:', collectionTimeInSeconds)
    try:
        if locking:
            apiLock.acquire()

        if collectionTimeInSeconds < -2147483648 or collectionTimeInSeconds > 2147483647:
            if exception_on_error:
                raise ArgSizeException('collect_timed_start', 'collectionTimeInSeconds', collectionTimeInSeconds, 'c_int')
            if verbose:
                print('collectionTimeInSeconds (', collectionTimeInSeconds, ') is too large for c_int')
            return False

        result = wrap.LIB.collect_timed_start(collectionTimeInSeconds)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('collect_timed_start')
        return result
    finally:
        if locking:
            apiLock.release()


def collect_start():
    if verbose:
        print('Called collect_start()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.collect_start()
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('collect_start')
        return result
    finally:
        if locking:
            apiLock.release()


def collect_stop():
    if verbose:
        print('Called collect_stop()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.collect_stop()
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('collect_stop')
        return result
    finally:
        if locking:
            apiLock.release()


def collect_isCollecting():
    if verbose:
        print('Called collect_isCollecting()')
    try:
        if locking:
            apiLock.acquire()

        val = c_bool()

        result = wrap.LIB.collect_isCollecting(val)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('collect_isCollecting')
        else:
            args = ArgsOUT()
            args.val = val.value
            if verbose:
                print('Got:')
                print('    val:', val.value)
            return args
    finally:
        if locking:
            apiLock.release()


def collect_setCollectionDelay(collectionDelayMS):
    if verbose:
        print('Called collect_setCollectionDelay() with params:')
        print('    collectionDelayMS:', collectionDelayMS)
    try:
        if locking:
            apiLock.acquire()

        if collectionDelayMS < -2147483648 or collectionDelayMS > 2147483647:
            if exception_on_error:
                raise ArgSizeException('collect_setCollectionDelay', 'collectionDelayMS', collectionDelayMS, 'c_int')
            if verbose:
                print('collectionDelayMS (', collectionDelayMS, ') is too large for c_int')
            return False

        result = wrap.LIB.collect_setCollectionDelay(collectionDelayMS)
        if not result:
            errval = GetLastErrorValue()
            if errval and exception_on_error:
                raise error_code_to_exception_map[errval]('collect_setCollectionDelay')
        return result
    finally:
        if locking:
            apiLock.release()


def collect_getCollectionDelay():
    if verbose:
        print('Called collect_getCollectionDelay()')
    try:
        if locking:
            apiLock.acquire()

        result = wrap.LIB.collect_getCollectionDelay()
        if verbose:
            print('result:', result)
        return result
    finally:
        if locking:
            apiLock.release()
