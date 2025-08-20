
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


from c_enum import CEnum
import os
import os.path
import sys

if sys.maxsize <= 2**32:
    print("64 bit python required, stopping")
    quit()

try:
    path = os.path.dirname(os.path.abspath(__file__))
    # Put our folder at the beginning of Path so [in Windows] Qt DLLs are found in our folder FIRST:
    os.environ['PATH'] = path + os.pathsep + os.environ['PATH']
    libfile = "/home/evczt/kev_360_373/lib/libDMatrixSharedLib_Internal.so"
    LIB = CDLL(libfile)
except Exception as e:
    print('exception loading', libfile)
    raise e


# ------------------- BEGIN included file internal_api_boilerplate.py -------------------
# typedef void(*callback_function_str_and_size)(const char*, int);
# callback_function_str_and_size = CFUNCTYPE(None, POINTER(c_char), c_int)
# typedef void(*callback_function_int)(int);
# callback_function_int = CFUNCTYPE(None, c_int)
# typedef void(*void_callback_function)();
# void_callback_function = CFUNCTYPE(None)

# typedef void(*callback_function_op)(OperationType);
callback_function_op = CFUNCTYPE(None, c_int)

# typedef void(*callback_function_op_int)(OperationType, int);
callback_function_op_int = CFUNCTYPE(None, c_int, c_int)

# typedef void(*callback_function_type_str)(CallbackType, const char*) ;
callback_function_type_str = CFUNCTYPE(None, POINTER(c_char))

# typedef void(*data_recvd_function)(DMatrixData*, void*);
data_recvd_function = CFUNCTYPE(None, POINTER(DMatrixData), c_void_p)

# typedef void(*callback_function_val_changed)(ValueChanged, int, void*);
# NOT callback_function_val_changed = CFUNCTYPE(None, ValueChanged, c_int, c_void_p)
# https://lists.archive.carbon60.com/python/python/1269881
# Only ctypes types are supported in callbacks, which unfortunately isn't documented clearly
callback_function_val_changed = CFUNCTYPE(None, c_int, c_int, c_void_p)
# -------------------- END included file internal_api_boilerplate.py --------------------


class CallbackType(CEnum):
    STATUS_COLLECTION = None
    STATUS_CONNECTION = None


class RegisterOp(CEnum):
    RegOp_Write = None
    RegOp_Read = None


class UpdateType(CEnum):
    UpdateType_Single = None
    UpdateType_Broadcast = None


class SetType(CEnum):
    SetType_Undefined = None
    SetType_Direct = None
    SetType_Stepped = None


class UpdateMode(CEnum):
    UpdateMode_Undefined = None
    UpdateMode_Manual = None
    UpdateMode_Auto = None


class Selection(CEnum):
    Selection_Undefined = None
    Selection_Single = None
    Selection_All = None


class PLLClock(CEnum):
    PLLClock_Undefined = None
    PLLClock_20MHz = None
    PLLClock_40MHz = None


class AnodeTestPulseEdge(CEnum):
    AnodeTestPulseEdge_Undefined = None
    AnodeTestPulseEdge_InjectNegativeCharge = None
    AnodeTestPulseEdge_InjectPosAndNegCharge = None


class MonitorSignal(CEnum):
    MonitorSignal_Positive = None
    MonitorSignal_Negative = None


class ChannelType(CEnum):
    ChannelType_Anode = None
    ChannelType_Cathode = None


class TimingChannelUnipolarGain(CEnum):
    TimingChannelUnipolarGain_Undefined = None
    TimingChannelUnipolarGain_27mV = None
    TimingChannelUnipolarGain_81mV = None


class CathodeChannelGain(CEnum):
    C_ChannelGain_Undefined = None
    C_ChannelGain_20mV = None
    C_ChannelGain_60mV = None


class AnodeChannelGain(CEnum):
    A_ChannelGain_Undefined = None
    A_ChannelGain_20mV = None
    A_ChannelGain_40mV = None
    A_ChannelGain_60mV = None
    A_ChannelGain_120mV = None


class TestSigType(CEnum):
    TestSigType_Undefined = None
    TestSigType_Step = None
    TestSigType_Ramp = None


class InternalLeakageCurrentGenerator(CEnum):
    InternalLeakageCurrentGenerator_Undefined = None
    InternalLeakageCurrentGenerator_60pA = None
    InternalLeakageCurrentGenerator_0A = None


class TimingChannelsShaperPeakingTime(CEnum):
    TimingChannelsShaperPeakingTime_Undefined = None
    TimingChannelsShaperPeakingTime_100nS = None
    TimingChannelsShaperPeakingTime_200nS = None
    TimingChannelsShaperPeakingTime_400nS = None
    TimingChannelsShaperPeakingTime_800nS = None


class MultipleFiringSuppressionTime(CEnum):
    MultipleFiringSuppressionTime_Undefined = None
    MultipleFiringSuppressionTime_62_5nS = None
    MultipleFiringSuppressionTime_125nS = None
    MultipleFiringSuppressionTime_250nS = None
    MultipleFiringSuppressionTime_600nS = None


class ChannelThresholdType(CEnum):
    ChannelThresholdType_CathodeTimingPrimaryMultiThresholdBiPolar = None
    ChannelThresholdType_CathodeTimingUnipolar = None
    ChannelThresholdType_CathodeEnergy = None
    ChannelThresholdType_AnodeNegativeEnergy = None
    ChannelThresholdType_AnodePositiveEnergy = None


class CathodeTestSigSrc(CEnum):
    CathodeTestSigSrc_Undefined = None
    CathodeTestSigSrc_AnodeTestSig = None
    CathodeTestSigSrc_SDI = None


class TimingChannelBipolarGain(CEnum):
    TimingChannelBipolarGain_Undefined = None
    TimingChannelBipolarGain_21mV = None
    TimingChannelBipolarGain_55mV = None
    TimingChannelBipolarGain_63mV = None
    TimingChannelBipolarGain_164mV = None


class AnalogOutput(CEnum):
    AnalogOutput_Undefined = None
    AnalogOutput_NoFunction = None
    AnalogOutput_Baseline = None
    AnalogOutput_Temperature = None
    AnalogOutput_DACS = None
    AnalogOutput_CathodeEnergyTiming = None
    AnalogOutput_AnodeEnergy = None


class CathodeEnergyTiming(CEnum):
    CathodeEnergyTiming_Undefined = None
    CathodeEnergyTiming_Channel1Energy = None
    CathodeEnergyTiming_Channel1Timing = None
    CathodeEnergyTiming_Channel2Energy = None
    CathodeEnergyTiming_Channel2Timing = None
    CathodeEnergyTiming_NONE = None


class DACS(CEnum):
    DACS_Undefined = None
    DACS_AnodeEnergyThreshold = None
    DACS_AnodeEnergyTransient = None
    DACS_CathodeEnergyThreshold = None
    DACS_CathodeTimingUnipolarThreshold = None
    DACS_CathodeTimingFirstMultiThreshold = None
    DACS_CathodeTimingSecondMultiThreshold = None
    DACS_CathodeTimingThirdMultiThreshold = None
    DACS_AnodeTestSignal = None
    DACS_CathodeTestSignal = None
    DACS_NONE = None


class Signal(CEnum):
    Signal_Undefined = None
    Signal_Positive = None
    Signal_Negative = None


class ChannelUpdateType(CEnum):
    ChannelUpdateType_SingleChannel = None
    ChannelUpdateType_Broadcast = None


class TestPulseEdge(CEnum):
    TestPulseEdge_Undefined = None
    TestPulseEdge_InjectNegCharge = None
    TestPulseEdge_InjectPosAndNegCharge = None


class CathodeTimingChannelType(CEnum):
    CathodeTimingChannelType_FirstMultiThresholdBiPolar = None
    CathodeTimingChannelType_SecondMultiThreshold = None
    CathodeTimingChannelType_ThirdMultiThreshold = None
    CathodeTimingChannelType_Unipolar = None


class GMASICReadoutMode(CEnum):
    GMASICReadout_Undefined = None
    GMASICReadout_Sparsified = None
    GMASICReadout_EnhancedSparsified = None


class CathodeInternalLeakageCurrentGenerator(CEnum):
    CathodeInternalLeakageCurrentGenerator_Undefined = None
    CathodeInternalLeakageCurrentGenerator_350pA = None
    CathodeInternalLeakageCurrentGenerator_2nA = None


class CathodeShapedTimingSignal(CEnum):
    CathodeShapedTimingSignal_Undefined = None
    CathodeShapedTimingSignal_Unipolar = None
    CathodeShapedTimingSignal_Bipolar = None


class CathodeTimingMode(CEnum):
    CathodeTimingMode_Undefined = None
    CathodeTimingMode_Unipolar = None
    CathodeTimingMode_MultiThreshold_Unipolar = None
    CathodeTimingMode_BiPolar_Unipolar = None


class GMReadoutMode(CEnum):
    GMReadout_ReadAll = None
    GMReadout_Sparsified = None
    GMReadout_EnhancedSparsified = None
    GMReadout_FlagsOnly = None
    GMReadout_Undefined = None


class GMCathodeMode(CEnum):
    GMCathMode_Unipolar = None
    GMCathMode_MultiThreshold = None
    GMCathMode_Bipolar = None
    GMCathMode_Undefined = None


class GMPulserFrequency(CEnum):
    GMPulserFreq_100Hz = None
    GMPulserFreq_1kHz = None
    GMPulserFreq_10kHz = None
    GMPulserFreq_100kHz = None
    GMPulserFreq_Undefined = None


class GMUpdateType(CEnum):
    GMUpdateType_Undefined = None
    GMUpdateType_SingleGM = None
    GMUpdateType_Broadcast = None


class AMUpdateType(CEnum):
    AMUpdateType_Undefined = None
    AMUpdateType_SingleAM = None
    AMUpdateType_Broadcast = None


class SysClockSpeed(CEnum):
    SysClockSpeed_Undefined = None
    SysClockSpeed_10MHZ = None
    SysClockSpeed_20MHZ = None
    SysClockSpeed_40MHZ = None
    SysClockSpeed_80MHZ = None


class PacketData(CEnum):
    PacketData_Undefined = None
    PacketData_AMNo = None
    PacketData_GMNo = None
    PacketData_Timestamp = None
    PacketData_PhotonCount = None


class PhotonData(CEnum):
    PhotonData_Undefined = None
    PhotonData_Pixel = None
    PhotonData_Energy = None
    PhotonData_EnergyPosEvent = None
    PhotonData_TimeDetect = None
    PhotonData_TimeDetectPosEvent = None
    PhotonData_ThresholdFlag = None


class FAN_SELECT(CEnum):
    DMATRIX_FAN_UNDEFINED = None
    DMATRIX_FAN1 = None
    DMATRIX_FAN2 = None


class BRAM_ID(CEnum):
    BRAM_ID_UNDEFINED = None
    BRAM_ID1 = None
    BRAM_ID2 = None
    BRAM_ID3 = None
    BRAM_ID4 = None


class STATUSFLAG(CEnum):
    STATUSFLAG_UNDEFINED = None
    STATUSFLAG_STATUS0 = None
    STATUSFLAG_STATUS1 = None
    STATUSFLAG_EXT_TRG = None
    STATUSFLAG_SYS_ERR = None
    STATUSFLAG_SYS_COMM_ERR = None
    STATUSFLAG_SYS_ILL_CMD = None
    STATUSFLAG_AM_ERR = None
    STATUSFLAG_SYS_LED = None
    STATUSFLAG_HW_SW_STAT = None
    STATUSFLAG_HV_LED = None
    STATUSFLAG_HV_ON = None
    STATUSFLAG_AM0_NOTERR = None
    STATUSFLAG_AM1_NOTERR = None
    STATUSFLAG_AM2_NOTERR = None
    STATUSFLAG_AM3_NOTERR = None


class FPGASTATUSFLAG(CEnum):
    FPGASTATUSFLAG_IDLE = None
    FPGASTATUSFLAG_ASICLOADERR = None
    FPGASTATUSFLAG_FIFOFULL = None


class COMMERR_ID(CEnum):
    COMMERR_NONE = None
    COMMERR_PACKETCRC = None
    COMMERR_NOTUSED = None
    COMMERR_PACKETINCOMPLETE = None
    COMMERR_WRONGCOMMAND = None
    COMMERR_EEPROM = None
    COMMERR_UNDEFINED = None


class COMMERR_OWNER(CEnum):
    COMMERROWNER_GM0 = None
    COMMERROWNER_GM1 = None
    COMMERROWNER_GM2 = None
    COMMERROWNER_GM3 = None
    COMMERROWNER_AMFPGA = None
    COMMERROWNER_UNDEFINED = None


class SYSMODE_ID(CEnum):
    SYSMODE_ASICSOFF = None
    SYSMODE_POWERUP = None
    SYSMODE_IDLE = None
    SYSMODE_COLLECTING = None
    SYSMODE_NOTUSED = None
    SYSMODE_DEBUG = None
    SYSMODE_UNDEFINED = None


class GMCollectionType(CEnum):
    GMCollectionType_All = None
    GMCollectionType_Cycle = None


LIB.mm_write_reg.restype = c_bool
LIB.mm_write_reg.argtypes = [c_int, c_uint]

LIB.mm_read_reg.restype = c_bool
LIB.mm_read_reg.argtypes = [c_int, POINTER(c_uint)]

LIB.gm_write_reg.restype = c_bool
LIB.gm_write_reg.argtypes = [c_int, c_uint]

LIB.gm_read_reg.restype = c_bool
LIB.gm_read_reg.argtypes = [c_int, POINTER(c_uint)]

LIB.am_write_reg.restype = c_bool
LIB.am_write_reg.argtypes = [c_int, c_uint]

LIB.am_read_reg.restype = c_bool
LIB.am_read_reg.argtypes = [c_int, POINTER(c_uint)]

LIB.sys_get_newDeviceIP.restype = c_bool
LIB.sys_get_newDeviceIP.argtypes = [POINTER(c_uint)]

LIB.sys_get_newDeviceGateway.restype = c_bool
LIB.sys_get_newDeviceGateway.argtypes = [POINTER(c_uint)]

LIB.sys_get_newDeviceNetmask.restype = c_bool
LIB.sys_get_newDeviceNetmask.argtypes = [POINTER(c_uint)]

LIB.mm_set_readClockSpeed.restype = c_bool
LIB.mm_set_readClockSpeed.argtypes = [SysClockSpeed]

LIB.mm_get_readClockSpeed.restype = c_bool
LIB.mm_get_readClockSpeed.argtypes = [POINTER(c_int32)]

LIB.sys_set_heaterCtl.restype = c_bool
LIB.sys_set_heaterCtl.argtypes = [c_uint]

LIB.sys_get_heaterCtl.restype = c_bool
LIB.sys_get_heaterCtl.argtypes = [POINTER(c_uint)]

LIB.mm_set_packetTxRate.restype = c_bool
LIB.mm_set_packetTxRate.argtypes = [c_uint]

LIB.mm_get_packetTxRate.restype = c_bool
LIB.mm_get_packetTxRate.argtypes = [POINTER(c_uint)]

LIB.mm_set_enableWebIface.restype = c_bool
LIB.mm_set_enableWebIface.argtypes = [c_bool]

LIB.mm_get_enableWebIface.restype = c_bool
LIB.mm_get_enableWebIface.argtypes = [POINTER(c_bool)]

LIB.mm_set_testPacket.restype = c_bool
LIB.mm_set_testPacket.argtypes = [c_bool]

LIB.mm_get_testPacket.restype = c_bool
LIB.mm_get_testPacket.argtypes = [POINTER(c_bool)]

LIB.mm_set_clearBram.restype = c_bool
LIB.mm_set_clearBram.argtypes = [c_bool]

LIB.mm_get_clearBram.restype = c_bool
LIB.mm_get_clearBram.argtypes = [POINTER(c_bool)]

LIB.mm_set_enableLog.restype = c_bool
LIB.mm_set_enableLog.argtypes = [c_bool]

LIB.mm_get_enableLog.restype = c_bool
LIB.mm_get_enableLog.argtypes = [POINTER(c_bool)]

LIB.mm_set_enableExternalTrigger.restype = c_bool
LIB.mm_set_enableExternalTrigger.argtypes = [c_bool]

LIB.mm_get_enableExternalTrigger.restype = c_bool
LIB.mm_get_enableExternalTrigger.argtypes = [POINTER(c_bool)]

LIB.mm_set_framesRx.restype = c_bool
LIB.mm_set_framesRx.argtypes = [c_uint]

LIB.mm_set_framesTx.restype = c_bool
LIB.mm_set_framesTx.argtypes = [c_uint]

LIB.mm_set_dbgMsg.restype = c_bool
LIB.mm_set_dbgMsg.argtypes = [c_bool]

LIB.mm_get_dbgMsg.restype = c_bool
LIB.mm_get_dbgMsg.argtypes = [POINTER(c_bool)]

LIB.mm_set_dbgCon.restype = c_bool
LIB.mm_set_dbgCon.argtypes = [c_bool]

LIB.mm_get_dbgCon.restype = c_bool
LIB.mm_get_dbgCon.argtypes = [POINTER(c_bool)]

LIB.mm_set_dbgMode.restype = c_bool
LIB.mm_set_dbgMode.argtypes = [c_bool]

LIB.mm_get_dbgMode.restype = c_bool
LIB.mm_get_dbgMode.argtypes = [POINTER(c_bool)]

LIB.mm_get_dumpBram.restype = c_bool
LIB.mm_get_dumpBram.argtypes = [BRAM_ID, POINTER(c_bool)]

LIB.mm_set_dumpBram.restype = c_bool
LIB.mm_set_dumpBram.argtypes = [BRAM_ID, c_bool]

LIB.mm_set_collect.restype = c_bool
LIB.mm_set_collect.argtypes = [c_bool]

LIB.mm_get_collect.restype = c_bool
LIB.mm_get_collect.argtypes = [POINTER(c_bool)]

LIB.sys_set_udpPort.restype = c_bool
LIB.sys_set_udpPort.argtypes = [c_uint]

LIB.sys_set_readNetworkCfg.restype = c_bool
LIB.sys_set_readNetworkCfg.argtypes = [c_bool]

LIB.sys_get_readNetworkCfg.restype = c_bool
LIB.sys_get_readNetworkCfg.argtypes = [POINTER(c_bool)]

LIB.am_get_sysMode.restype = c_bool
LIB.am_get_sysMode.argtypes = [POINTER(c_int32)]

LIB.am_get_readReady.restype = c_bool
LIB.am_get_readReady.argtypes = [POINTER(c_bool)]

LIB.gm_set_enableTimeDetect.restype = c_bool
LIB.gm_set_enableTimeDetect.argtypes = [c_bool]

LIB.gm_get_enableTimeDetect.restype = c_bool
LIB.gm_get_enableTimeDetect.argtypes = [POINTER(c_bool)]

LIB.gm_get_checksumErrors.restype = c_uint
LIB.gm_get_checksumErrors.argtypes = []

LIB.gm_get_numTooLargeEnergies.restype = c_uint
LIB.gm_get_numTooLargeEnergies.argtypes = []

LIB.gm_get_numTooHighChannelNums.restype = c_uint
LIB.gm_get_numTooHighChannelNums.argtypes = []

LIB.gm_get_numTooLargeTimeDetects.restype = c_uint
LIB.gm_get_numTooLargeTimeDetects.argtypes = []

LIB.gm_get_numImpossNonExceededThresholds.restype = c_uint
LIB.gm_get_numImpossNonExceededThresholds.argtypes = []

LIB.gm_get_numImpossEnergyPosEventZeros.restype = c_uint
LIB.gm_get_numImpossEnergyPosEventZeros.argtypes = []

LIB.gm_get_numImpossTimeDetectPosEventZeros.restype = c_uint
LIB.gm_get_numImpossTimeDetectPosEventZeros.argtypes = []

LIB.gm_get_numEnergyPosEventDiffTimeDetectPosEvents.restype = c_uint
LIB.gm_get_numEnergyPosEventDiffTimeDetectPosEvents.argtypes = []

LIB.gm_get_numChK1Chan128.restype = c_uint
LIB.gm_get_numChK1Chan128.argtypes = []

LIB.gm_get_numChK1Chan129.restype = c_uint
LIB.gm_get_numChK1Chan129.argtypes = []

LIB.gm_get_numChK1Chan130.restype = c_uint
LIB.gm_get_numChK1Chan130.argtypes = []

LIB.gm_get_numChK1Chan131.restype = c_uint
LIB.gm_get_numChK1Chan131.argtypes = []

LIB.gm_get_numTempChan132.restype = c_uint
LIB.gm_get_numTempChan132.argtypes = []

LIB.gm_get_numChK2Chan133.restype = c_uint
LIB.gm_get_numChK2Chan133.argtypes = []

LIB.gm_get_numChK2Chan134.restype = c_uint
LIB.gm_get_numChK2Chan134.argtypes = []

LIB.gm_get_numChK2Chan135.restype = c_uint
LIB.gm_get_numChK2Chan135.argtypes = []

LIB.gm_get_numChK2Chan136.restype = c_uint
LIB.gm_get_numChK2Chan136.argtypes = []

LIB.sys_mapPixel.restype = c_bool
LIB.sys_mapPixel.argtypes = [c_int, c_int, c_short, c_short]

LIB.sys_set_loggingPackets.restype = c_bool
LIB.sys_set_loggingPackets.argtypes = [c_bool]

LIB.sys_get_loggingPackets.restype = c_bool
LIB.sys_get_loggingPackets.argtypes = [POINTER(c_bool)]

LIB.api_get_version.restype = None
LIB.api_get_version.argtypes = [POINTER(c_char)]

LIB.api_get_version_size.restype = c_int
LIB.api_get_version_size.argtypes = []

LIB.api_get_lastErr.restype = None
LIB.api_get_lastErr.argtypes = [POINTER(c_char)]

LIB.api_set_lastErr.restype = None
LIB.api_set_lastErr.argtypes = [POINTER(c_char)]

LIB.api_get_lastErr_size.restype = c_int
LIB.api_get_lastErr_size.argtypes = []

LIB.api_close.restype = None
LIB.api_close.argtypes = []

LIB.api_set_opCompleteCallback.restype = None
LIB.api_set_opCompleteCallback.argtypes = [callback_function_op]

LIB.api_set_opProgressCallback.restype = None
LIB.api_set_opProgressCallback.argtypes = [callback_function_op_int]

LIB.api_set_statusCallback.restype = None
LIB.api_set_statusCallback.argtypes = [callback_function_type_str]

LIB.api_set_dataRecvdCallback.restype = None
LIB.api_set_dataRecvdCallback.argtypes = [data_recvd_function, c_void_p]

LIB.api_set_valueChangedCallback.restype = None
LIB.api_set_valueChangedCallback.argtypes = [callback_function_val_changed, c_void_p]

LIB.api_processEvents.restype = c_bool
LIB.api_processEvents.argtypes = []

LIB.sys_connect.restype = c_bool
LIB.sys_connect.argtypes = [POINTER(c_char), POINTER(c_char)]

LIB.sys_isConnected.restype = c_bool
LIB.sys_isConnected.argtypes = []

LIB.sys_disconnect.restype = None
LIB.sys_disconnect.argtypes = []

LIB.sys_set_fanCtl.restype = c_bool
LIB.sys_set_fanCtl.argtypes = [FAN_SELECT, c_ubyte]

LIB.sys_get_fanCtl.restype = c_bool
LIB.sys_get_fanCtl.argtypes = [FAN_SELECT, POINTER(c_ubyte)]

LIB.sys_set_hvSetType.restype = c_bool
LIB.sys_set_hvSetType.argtypes = [SetType]

LIB.sys_get_hvSetType.restype = c_bool
LIB.sys_get_hvSetType.argtypes = [POINTER(c_int32)]

LIB.sys_set_hvUpdateStep.restype = c_bool
LIB.sys_set_hvUpdateStep.argtypes = [c_ubyte]

LIB.sys_get_hvUpdateStep.restype = c_bool
LIB.sys_get_hvUpdateStep.argtypes = [POINTER(c_ubyte)]

LIB.sys_set_hvUpdateStepVolts.restype = c_bool
LIB.sys_set_hvUpdateStepVolts.argtypes = [c_uint]

LIB.sys_get_hvUpdateStepVolts.restype = c_bool
LIB.sys_get_hvUpdateStepVolts.argtypes = [POINTER(c_uint)]

LIB.sys_set_hvUpdateStepInterval.restype = c_bool
LIB.sys_set_hvUpdateStepInterval.argtypes = [c_ubyte]

LIB.sys_get_hvUpdateStepInterval.restype = c_bool
LIB.sys_get_hvUpdateStepInterval.argtypes = [POINTER(c_ubyte)]

LIB.sys_set_hvDACSlope.restype = c_bool
LIB.sys_set_hvDACSlope.argtypes = [c_double]

LIB.sys_get_hvDACSlope.restype = c_bool
LIB.sys_get_hvDACSlope.argtypes = [POINTER(c_double)]

LIB.sys_set_hvDACOffset.restype = c_bool
LIB.sys_set_hvDACOffset.argtypes = [c_double]

LIB.sys_get_hvDACOffset.restype = c_bool
LIB.sys_get_hvDACOffset.argtypes = [POINTER(c_double)]

LIB.sys_set_hvCtl.restype = c_bool
LIB.sys_set_hvCtl.argtypes = [c_ubyte]

LIB.sys_get_hvCtl.restype = c_bool
LIB.sys_get_hvCtl.argtypes = [POINTER(c_ubyte)]

LIB.sys_get_hvTarget.restype = c_bool
LIB.sys_get_hvTarget.argtypes = [POINTER(c_ubyte)]

LIB.sys_set_hvCtlVolts.restype = c_bool
LIB.sys_set_hvCtlVolts.argtypes = [c_uint]

LIB.sys_get_hvCtlVolts.restype = c_bool
LIB.sys_get_hvCtlVolts.argtypes = [POINTER(c_uint)]

LIB.sys_get_hvTargetVolts.restype = c_bool
LIB.sys_get_hvTargetVolts.argtypes = [POINTER(c_uint)]

LIB.sys_stop_hvUpdate.restype = None
LIB.sys_stop_hvUpdate.argtypes = []

LIB.sys_set_enableHV.restype = c_bool
LIB.sys_set_enableHV.argtypes = [c_bool]

LIB.sys_get_enableHV.restype = c_bool
LIB.sys_get_enableHV.argtypes = [POINTER(c_bool)]

LIB.sys_get_statusFlag.restype = c_bool
LIB.sys_get_statusFlag.argtypes = [STATUSFLAG, POINTER(c_bool)]

LIB.sys_set_deviceType.restype = c_bool
LIB.sys_set_deviceType.argtypes = [DMatrixDevice]

LIB.sys_get_deviceType.restype = DMatrixDevice
LIB.sys_get_deviceType.argtypes = []

LIB.sys_set_enablePixelMapping.restype = c_bool
LIB.sys_set_enablePixelMapping.argtypes = [c_bool]

LIB.sys_get_enablePixelMapping.restype = c_bool
LIB.sys_get_enablePixelMapping.argtypes = [POINTER(c_bool)]

LIB.sys_get_hardwareLocationOfPixelCoordinate.restype = c_bool
LIB.sys_get_hardwareLocationOfPixelCoordinate.argtypes = [c_int, c_int, POINTER(PixelHardwareLocation)]

LIB.sys_get_hardwareLocationOfPixel.restype = c_bool
LIB.sys_get_hardwareLocationOfPixel.argtypes = [c_int, POINTER(PixelHardwareLocation)]

LIB.sys_get_pixelCoordinateOfHardwareLocation.restype = c_bool
LIB.sys_get_pixelCoordinateOfHardwareLocation.argtypes = [POINTER(PixelHardwareLocation), POINTER(c_int), POINTER(c_int)]

LIB.sys_get_pixelOfPixelCoordinate.restype = c_bool
LIB.sys_get_pixelOfPixelCoordinate.argtypes = [c_int, c_int, POINTER(c_int)]

LIB.sys_get_noOfPixelRows.restype = c_int
LIB.sys_get_noOfPixelRows.argtypes = []

LIB.sys_get_noOfPixelColumns.restype = c_int
LIB.sys_get_noOfPixelColumns.argtypes = []

LIB.sys_get_noOfPixels.restype = c_int
LIB.sys_get_noOfPixels.argtypes = []

LIB.sys_mask_pixel.restype = c_bool
LIB.sys_mask_pixel.argtypes = [c_int, c_bool]

LIB.sys_mask_pixelCoordinate.restype = c_bool
LIB.sys_mask_pixelCoordinate.argtypes = [c_int, c_int, c_bool]

LIB.sys_get_mask_pixel.restype = c_bool
LIB.sys_get_mask_pixel.argtypes = [c_int, POINTER(c_bool)]

LIB.sys_get_mask_pixelCoordinate.restype = c_bool
LIB.sys_get_mask_pixelCoordinate.argtypes = [c_int, c_int, POINTER(c_bool)]

LIB.sys_reboot.restype = c_bool
LIB.sys_reboot.argtypes = []

LIB.sys_get_udpPort.restype = c_bool
LIB.sys_get_udpPort.argtypes = [POINTER(c_uint)]

LIB.sys_set_newDeviceIP.restype = c_bool
LIB.sys_set_newDeviceIP.argtypes = [c_uint]

LIB.sys_set_newDeviceGateway.restype = c_bool
LIB.sys_set_newDeviceGateway.argtypes = [c_uint]

LIB.sys_set_newDeviceNetmask.restype = c_bool
LIB.sys_set_newDeviceNetmask.argtypes = [c_uint]

LIB.sys_set_writeNetworkCfg.restype = c_bool
LIB.sys_set_writeNetworkCfg.argtypes = [c_bool]

LIB.sys_get_writeNetworkCfg.restype = c_bool
LIB.sys_get_writeNetworkCfg.argtypes = [POINTER(c_bool)]

LIB.sys_set_resetNetworkCfg.restype = c_bool
LIB.sys_set_resetNetworkCfg.argtypes = [c_bool]

LIB.sys_get_resetNetworkCfg.restype = c_bool
LIB.sys_get_resetNetworkCfg.argtypes = [POINTER(c_bool)]

LIB.sys_get_fpgaVersion.restype = c_bool
LIB.sys_get_fpgaVersion.argtypes = [POINTER(c_uint)]

LIB.sys_get_fwVersion.restype = c_bool
LIB.sys_get_fwVersion.argtypes = [POINTER(c_uint)]

LIB.sys_set_enableFtpServer.restype = c_bool
LIB.sys_set_enableFtpServer.argtypes = [c_bool]

LIB.sys_get_enableFtpServer.restype = c_bool
LIB.sys_get_enableFtpServer.argtypes = [POINTER(c_bool)]

LIB.sys_set_installedAM.restype = c_bool
LIB.sys_set_installedAM.argtypes = [c_ubyte, c_bool]

LIB.sys_get_installedAM.restype = c_bool
LIB.sys_get_installedAM.argtypes = [c_ubyte, POINTER(c_bool)]

LIB.sys_set_powerAllAm.restype = c_bool
LIB.sys_set_powerAllAm.argtypes = [c_bool]

LIB.sys_get_powerAllAm.restype = c_bool
LIB.sys_get_powerAllAm.argtypes = [POINTER(c_bool)]

LIB.sys_resetStatusFlagErrors.restype = c_bool
LIB.sys_resetStatusFlagErrors.argtypes = []

LIB.sys_resetFrameCounts.restype = c_bool
LIB.sys_resetFrameCounts.argtypes = []

LIB.sys_set_resetAllAm.restype = c_bool
LIB.sys_set_resetAllAm.argtypes = [c_bool]

LIB.sys_get_resetAllAm.restype = c_bool
LIB.sys_get_resetAllAm.argtypes = [POINTER(c_bool)]

LIB.sys_get_framesTx.restype = c_bool
LIB.sys_get_framesTx.argtypes = [POINTER(c_uint)]

LIB.sys_get_framesRx.restype = c_bool
LIB.sys_get_framesRx.argtypes = [POINTER(c_uint)]

LIB.sys_get_numAM.restype = c_int
LIB.sys_get_numAM.argtypes = []

LIB.sys_reset_GMStats.restype = None
LIB.sys_reset_GMStats.argtypes = []

LIB.am_set_active.restype = c_bool
LIB.am_set_active.argtypes = [c_int]

LIB.am_get_active.restype = c_int
LIB.am_get_active.argtypes = []

LIB.am_set_updateType.restype = c_bool
LIB.am_set_updateType.argtypes = [AMUpdateType]

LIB.am_get_updateType.restype = AMUpdateType
LIB.am_get_updateType.argtypes = []

LIB.am_get_fpgaVersion.restype = c_bool
LIB.am_get_fpgaVersion.argtypes = [POINTER(c_uint)]

LIB.am_get_muxAddr.restype = c_bool
LIB.am_get_muxAddr.argtypes = [POINTER(c_uint)]

LIB.am_set_muxAddr.restype = c_bool
LIB.am_set_muxAddr.argtypes = [c_uint]

LIB.am_get_commErr.restype = c_bool
LIB.am_get_commErr.argtypes = [POINTER(c_int32), POINTER(c_int32)]

LIB.am_get_fpgaStatus.restype = c_bool
LIB.am_get_fpgaStatus.argtypes = [FPGASTATUSFLAG, POINTER(c_bool)]

LIB.am_get_frameErr.restype = c_bool
LIB.am_get_frameErr.argtypes = [POINTER(c_bool)]

LIB.gm_set_active.restype = c_bool
LIB.gm_set_active.argtypes = [c_int]

LIB.gm_get_active.restype = c_int
LIB.gm_get_active.argtypes = []

LIB.gm_set_updateType.restype = c_bool
LIB.gm_set_updateType.argtypes = [GMUpdateType]

LIB.gm_get_updateType.restype = GMUpdateType
LIB.gm_get_updateType.argtypes = []

LIB.gm_set_enableNegData.restype = c_bool
LIB.gm_set_enableNegData.argtypes = [c_bool]

LIB.gm_get_enableNegData.restype = c_bool
LIB.gm_get_enableNegData.argtypes = [POINTER(c_bool)]

LIB.gm_set_enableThermalData.restype = c_bool
LIB.gm_set_enableThermalData.argtypes = [c_bool]

LIB.gm_get_enableThermalData.restype = c_bool
LIB.gm_get_enableThermalData.argtypes = [POINTER(c_bool)]

LIB.gm_get_temperature.restype = c_bool
LIB.gm_get_temperature.argtypes = [POINTER(c_float)]

LIB.gm_set_enableCathodePulser.restype = c_bool
LIB.gm_set_enableCathodePulser.argtypes = [c_bool]

LIB.gm_get_enableCathodePulser.restype = c_bool
LIB.gm_get_enableCathodePulser.argtypes = [POINTER(c_bool)]

LIB.gm_set_enableAnodePulser.restype = c_bool
LIB.gm_set_enableAnodePulser.argtypes = [c_bool]

LIB.gm_get_enableAnodePulser.restype = c_bool
LIB.gm_get_enableAnodePulser.argtypes = [POINTER(c_bool)]

LIB.gm_set_readoutMode.restype = c_bool
LIB.gm_set_readoutMode.argtypes = [GMReadoutMode]

LIB.gm_get_readoutMode.restype = c_bool
LIB.gm_get_readoutMode.argtypes = [POINTER(c_int32)]

LIB.gm_set_cathodeMode.restype = c_bool
LIB.gm_set_cathodeMode.argtypes = [GMCathodeMode]

LIB.gm_get_cathodeMode.restype = c_bool
LIB.gm_get_cathodeMode.argtypes = [POINTER(c_int32)]

LIB.gm_set_pulserFrequency.restype = c_bool
LIB.gm_set_pulserFrequency.argtypes = [GMPulserFrequency]

LIB.gm_get_pulserFrequency.restype = c_bool
LIB.gm_get_pulserFrequency.argtypes = [POINTER(c_int32)]

LIB.gm_set_pulseCount.restype = c_bool
LIB.gm_set_pulseCount.argtypes = [c_uint]

LIB.gm_get_pulseCount.restype = c_bool
LIB.gm_get_pulseCount.argtypes = [POINTER(c_uint)]

LIB.gm_set_delayTime.restype = c_bool
LIB.gm_set_delayTime.argtypes = [c_uint]

LIB.gm_get_delayTime.restype = c_bool
LIB.gm_get_delayTime.argtypes = [POINTER(c_uint)]

LIB.gm_set_timestampRes.restype = c_bool
LIB.gm_set_timestampRes.argtypes = [c_uint]

LIB.gm_get_timestampRes.restype = c_bool
LIB.gm_get_timestampRes.argtypes = [POINTER(c_uint)]

LIB.gm_set_simData.restype = c_bool
LIB.gm_set_simData.argtypes = [c_bool]

LIB.gm_get_simData.restype = c_bool
LIB.gm_get_simData.argtypes = [POINTER(c_bool)]

LIB.gm_get_adcTdo.restype = c_bool
LIB.gm_get_adcTdo.argtypes = [POINTER(c_uint)]

LIB.gm_get_adcPdo.restype = c_bool
LIB.gm_get_adcPdo.argtypes = [POINTER(c_uint)]

LIB.gm_set_disablePackets.restype = c_bool
LIB.gm_set_disablePackets.argtypes = [c_bool]

LIB.gm_get_disablePackets.restype = c_bool
LIB.gm_get_disablePackets.argtypes = [POINTER(c_bool)]

LIB.gm_set_rebootAsic.restype = c_bool
LIB.gm_set_rebootAsic.argtypes = [c_bool]

LIB.gm_get_rebootAsic.restype = c_bool
LIB.gm_get_rebootAsic.argtypes = [POINTER(c_bool)]

LIB.gm_set_reloadAsic.restype = c_bool
LIB.gm_set_reloadAsic.argtypes = [c_bool]

LIB.gm_get_reloadAsic.restype = c_bool
LIB.gm_get_reloadAsic.argtypes = [POINTER(c_bool)]

LIB.gm_set_testAsic.restype = c_bool
LIB.gm_set_testAsic.argtypes = [c_bool]

LIB.gm_get_testAsic.restype = c_bool
LIB.gm_get_testAsic.argtypes = [POINTER(c_bool)]

LIB.gm_set_powerAsic.restype = c_bool
LIB.gm_set_powerAsic.argtypes = [c_bool]

LIB.gm_get_powerAsic.restype = c_bool
LIB.gm_get_powerAsic.argtypes = [POINTER(c_bool)]

LIB.gm_get_numPackets.restype = c_uint
LIB.gm_get_numPackets.argtypes = []

LIB.gm_get_numTriggeredPhotons.restype = c_uint
LIB.gm_get_numTriggeredPhotons.argtypes = []

LIB.gm_get_numTotalPhotons.restype = c_uint
LIB.gm_get_numTotalPhotons.argtypes = []

LIB.asic_send_globalData.restype = c_bool
LIB.asic_send_globalData.argtypes = []

LIB.asic_set_analogOutputMonitored.restype = c_bool
LIB.asic_set_analogOutputMonitored.argtypes = [AnalogOutput]

LIB.asic_get_analogOutputMonitored.restype = c_bool
LIB.asic_get_analogOutputMonitored.argtypes = [POINTER(c_int32)]

LIB.asic_set_globalOptions.restype = c_bool
LIB.asic_set_globalOptions.argtypes = [ASICGlobalOptions]

LIB.asic_get_globalOptions.restype = c_bool
LIB.asic_get_globalOptions.argtypes = [POINTER(ASICGlobalOptions)]

LIB.asic_set_anodeInternalLeakageCurrentGenerator.restype = c_bool
LIB.asic_set_anodeInternalLeakageCurrentGenerator.argtypes = [InternalLeakageCurrentGenerator]

LIB.asic_get_anodeInternalLeakageCurrentGenerator.restype = c_bool
LIB.asic_get_anodeInternalLeakageCurrentGenerator.argtypes = [POINTER(c_int32)]

LIB.asic_set_timingChannelUnipolarGain.restype = c_bool
LIB.asic_set_timingChannelUnipolarGain.argtypes = [TimingChannelUnipolarGain]

LIB.asic_get_timingChannelUnipolarGain.restype = c_bool
LIB.asic_get_timingChannelUnipolarGain.argtypes = [POINTER(c_int32)]

LIB.asic_set_multipleFiringSuppressTime.restype = c_bool
LIB.asic_set_multipleFiringSuppressTime.argtypes = [MultipleFiringSuppressionTime]

LIB.asic_get_multipleFiringSuppressTime.restype = c_bool
LIB.asic_get_multipleFiringSuppressTime.argtypes = [POINTER(c_int32)]

LIB.asic_set_timingChannelBiPolarGain.restype = c_bool
LIB.asic_set_timingChannelBiPolarGain.argtypes = [TimingChannelBipolarGain]

LIB.asic_get_timingChannelBiPolarGain.restype = c_bool
LIB.asic_get_timingChannelBiPolarGain.argtypes = [POINTER(c_int32)]

LIB.asic_set_readoutMode.restype = c_bool
LIB.asic_set_readoutMode.argtypes = [GMASICReadoutMode]

LIB.asic_get_readoutMode.restype = c_bool
LIB.asic_get_readoutMode.argtypes = [POINTER(c_int32)]

LIB.asic_set_channelGain.restype = c_bool
LIB.asic_set_channelGain.argtypes = [AnodeChannelGain, CathodeChannelGain]

LIB.asic_get_channelGain.restype = c_bool
LIB.asic_get_channelGain.argtypes = [POINTER(c_int32), POINTER(c_int32)]

LIB.asic_set_testPulse.restype = c_bool
LIB.asic_set_testPulse.argtypes = [ChannelType, c_float]

LIB.asic_get_testPulse.restype = c_bool
LIB.asic_get_testPulse.argtypes = [ChannelType, POINTER(c_float)]

LIB.asic_set_anodeTestPulseEdge.restype = c_bool
LIB.asic_set_anodeTestPulseEdge.argtypes = [TestPulseEdge]

LIB.asic_get_anodeTestPulseEdge.restype = c_bool
LIB.asic_get_anodeTestPulseEdge.argtypes = [POINTER(c_int32)]

LIB.asic_set_cathodeTestSigSrc.restype = c_bool
LIB.asic_set_cathodeTestSigSrc.argtypes = [CathodeTestSigSrc]

LIB.asic_get_cathodeTestSigSrc.restype = c_bool
LIB.asic_get_cathodeTestSigSrc.argtypes = [POINTER(c_int32)]

LIB.asic_set_cathodeTestSigType.restype = c_bool
LIB.asic_set_cathodeTestSigType.argtypes = [TestSigType]

LIB.asic_get_cathodeTestSigType.restype = c_bool
LIB.asic_get_cathodeTestSigType.argtypes = [POINTER(c_int32)]

LIB.asic_set_peakingTime.restype = c_bool
LIB.asic_set_peakingTime.argtypes = [ChannelType, c_float]

LIB.asic_get_peakingTime.restype = c_bool
LIB.asic_get_peakingTime.argtypes = [ChannelType, POINTER(c_float)]

LIB.asic_set_peakDetectTimeout.restype = c_bool
LIB.asic_set_peakDetectTimeout.argtypes = [ChannelType, c_int]

LIB.asic_get_peakDetectTimeout.restype = c_bool
LIB.asic_get_peakDetectTimeout.argtypes = [ChannelType, POINTER(c_int)]

LIB.asic_set_timeDetectRampLength.restype = c_bool
LIB.asic_set_timeDetectRampLength.argtypes = [ChannelType, c_int]

LIB.asic_get_timeDetectRampLength.restype = c_bool
LIB.asic_get_timeDetectRampLength.argtypes = [ChannelType, POINTER(c_int)]

LIB.asic_set_cathodeTimingChannelsShaperPeakingTime.restype = c_bool
LIB.asic_set_cathodeTimingChannelsShaperPeakingTime.argtypes = [TimingChannelsShaperPeakingTime]

LIB.asic_get_cathodeTimingChannelsShaperPeakingTime.restype = c_bool
LIB.asic_get_cathodeTimingChannelsShaperPeakingTime.argtypes = [POINTER(c_int32)]

LIB.asic_set_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement.restype = c_bool
LIB.asic_set_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement.argtypes = [c_float]

LIB.asic_get_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement.restype = c_bool
LIB.asic_get_cathodeTimingChannelsSecondaryMultiThresholdsDisplacement.argtypes = [POINTER(c_float)]

LIB.asic_set_channelThreshold.restype = c_bool
LIB.asic_set_channelThreshold.argtypes = [ChannelThresholdType, c_float]

LIB.asic_get_channelThreshold.restype = c_bool
LIB.asic_get_channelThreshold.argtypes = [ChannelThresholdType, POINTER(c_float)]

LIB.asic_set_cathodeChannelInternalLeakageCurrentGenerator.restype = c_bool
LIB.asic_set_cathodeChannelInternalLeakageCurrentGenerator.argtypes = [c_int, CathodeInternalLeakageCurrentGenerator]

LIB.asic_get_cathodeChannelInternalLeakageCurrentGenerator.restype = c_bool
LIB.asic_get_cathodeChannelInternalLeakageCurrentGenerator.argtypes = [c_int, POINTER(c_int32)]

LIB.asic_set_anodeChannelMonitored.restype = c_bool
LIB.asic_set_anodeChannelMonitored.argtypes = [c_int]

LIB.asic_get_anodeChannelMonitored.restype = c_bool
LIB.asic_get_anodeChannelMonitored.argtypes = [POINTER(c_int)]

LIB.asic_set_cathodeEnergyTimingMonitored.restype = c_bool
LIB.asic_set_cathodeEnergyTimingMonitored.argtypes = [CathodeEnergyTiming]

LIB.asic_get_cathodeEnergyTimingMonitored.restype = c_bool
LIB.asic_get_cathodeEnergyTimingMonitored.argtypes = [POINTER(c_int32)]

LIB.asic_set_DACMonitored.restype = c_bool
LIB.asic_set_DACMonitored.argtypes = [DACS]

LIB.asic_get_DACMonitored.restype = c_bool
LIB.asic_get_DACMonitored.argtypes = [POINTER(c_int32)]

LIB.asic_send_channelData.restype = c_bool
LIB.asic_send_channelData.argtypes = []

LIB.channel_get_updateType.restype = c_bool
LIB.channel_get_updateType.argtypes = [POINTER(c_int32)]

LIB.channel_set_updateType.restype = None
LIB.channel_set_updateType.argtypes = [ChannelUpdateType]

LIB.channel_get_activeType.restype = ChannelType
LIB.channel_get_activeType.argtypes = []

LIB.channel_set_activeType.restype = None
LIB.channel_set_activeType.argtypes = [ChannelType]

LIB.channel_get_active.restype = c_bool
LIB.channel_get_active.argtypes = [POINTER(c_int)]

LIB.channel_set_active.restype = c_bool
LIB.channel_set_active.argtypes = [c_int]

LIB.channel_set_cpd.restype = c_bool
LIB.channel_set_cpd.argtypes = [c_bool]

LIB.channel_get_cpd.restype = c_bool
LIB.channel_get_cpd.argtypes = [c_int, POINTER(c_bool)]

LIB.channel_set_mask.restype = c_bool
LIB.channel_set_mask.argtypes = [c_bool]

LIB.channel_get_mask.restype = c_bool
LIB.channel_get_mask.argtypes = [ChannelType, c_int, POINTER(c_bool)]

LIB.channel_set_enableTestCapacitor.restype = c_bool
LIB.channel_set_enableTestCapacitor.argtypes = [c_bool]

LIB.channel_get_enableTestCapacitor.restype = c_bool
LIB.channel_get_enableTestCapacitor.argtypes = [ChannelType, c_int, POINTER(c_bool)]

LIB.channel_set_anodeSignalMonitored.restype = c_bool
LIB.channel_set_anodeSignalMonitored.argtypes = [Signal]

LIB.channel_get_anodeSignalMonitored.restype = c_bool
LIB.channel_get_anodeSignalMonitored.argtypes = [c_int, POINTER(c_int32)]

LIB.channel_set_cathodeShapedTimingSignal.restype = c_bool
LIB.channel_set_cathodeShapedTimingSignal.argtypes = [CathodeShapedTimingSignal]

LIB.channel_get_cathodeShapedTimingSignal.restype = c_bool
LIB.channel_get_cathodeShapedTimingSignal.argtypes = [c_int, POINTER(c_int32)]

LIB.channel_set_positivePulseThresholdTrim.restype = c_bool
LIB.channel_set_positivePulseThresholdTrim.argtypes = [c_int]

LIB.channel_get_positivePulseThresholdTrim.restype = c_bool
LIB.channel_get_positivePulseThresholdTrim.argtypes = [ChannelType, c_int, POINTER(c_int)]

LIB.channel_set_anodeNegativePulseThresholdTrim.restype = c_bool
LIB.channel_set_anodeNegativePulseThresholdTrim.argtypes = [c_int]

LIB.channel_get_anodeNegativePulseThresholdTrim.restype = c_bool
LIB.channel_get_anodeNegativePulseThresholdTrim.argtypes = [c_int, POINTER(c_int)]

LIB.channel_set_cathodeTimingMode.restype = c_bool
LIB.channel_set_cathodeTimingMode.argtypes = [CathodeTimingMode]

LIB.channel_get_cathodeTimingMode.restype = c_bool
LIB.channel_get_cathodeTimingMode.argtypes = [c_int, POINTER(c_int32)]

LIB.channel_set_cathodeTimingTrim.restype = c_bool
LIB.channel_set_cathodeTimingTrim.argtypes = [CathodeTimingChannelType, c_double]

LIB.channel_get_cathodeTimingTrim.restype = c_bool
LIB.channel_get_cathodeTimingTrim.argtypes = [c_int, CathodeTimingChannelType, POINTER(c_double)]

LIB.collect_timed_start.restype = c_bool
LIB.collect_timed_start.argtypes = [c_int]

LIB.collect_start.restype = c_bool
LIB.collect_start.argtypes = []

LIB.collect_stop.restype = c_bool
LIB.collect_stop.argtypes = []

LIB.collect_isCollecting.restype = c_bool
LIB.collect_isCollecting.argtypes = [POINTER(c_bool)]

LIB.collect_setCollectionDelay.restype = c_bool
LIB.collect_setCollectionDelay.argtypes = [c_int]

LIB.collect_getCollectionDelay.restype = c_int
LIB.collect_getCollectionDelay.argtypes = []
