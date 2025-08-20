from flask import Flask, request, jsonify, render_template
from icecream import ic
from time import sleep
from testing.DMatrix_Commands import Dmatrix
from testing.DMatrix_Util import connectToApi, setSystemSettings, setAmSettings, setGmSettings, setASICSettings, setChannelSettings
import DMatrix_internal as dm
import datetime
import logging
import time
import serial
import yaml

app = Flask(__name__)
today = datetime.datetime.now().strftime("%Y-%m-%d")
logging.basicConfig(format='%(asctime)s %(message)s', filename=f'/storage/eV common/Production/Logging/kev360_373_{today}.log', level=logging.DEBUG)

def setupSerial():
    #serial.tools.list_ports
    comms = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
    comms.flush()
    return comms

def checkForMatch(wonumber, serialnumber):
    if serialnumber == "":
        logging.debug("serial number is empty")
        return True
    lengthWoNumber = len(wonumber)
    if wonumber != serialnumber[:lengthWoNumber]:
        print(f"work order number: {wonumber}, serial number: {serialnumber[:lengthWoNumber]}")
        logging.debug(f"work order number: {wonumber}, serial number: {serialnumber[:lengthWoNumber]}")
        return False
    else:
        logging.debug("Serial and work order number Match!")
        pass

def checkSettings(setting_type, pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap):
    print(f"Checking settings for {setting_type}")
    poweredAMsFlag = dm.sys_get_powerAllAm()
    poweredAMsFlag = str(poweredAMsFlag)[5:].strip("}")
    ispulser = dm.gm_get_enableAnodePulser()
    ispulser = str(ispulser)[5:].strip("}")
    peakingtime = dm.asic_get_peakingTime(dm.ChannelType_Anode)
    peakingtime = str(peakingtime)[27:].strip("}")
    logging.debug(f"pulser on :{ispulser}")
    logging.debug(f"AM's Powered on :{poweredAMsFlag}")
    logging.debug(f"Anode Peaking time: {peakingtime}")
    if setting_type == "Pulser":
        if poweredAMsFlag == "True" and peakingtime == "0.5":
            logging.info("Pulser already set ")
            settingsflag = sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, Powerflag=True)
            return settingsflag
        else:
            logging.info("Pulser setting were not set")
            settingsflag = sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, Powerflag=False)
            return settingsflag
    if setting_type == "Source":
        if ispulser == "False" and poweredAMsFlag == "True" and peakingtime == "0.5":
            logging.info("Source settings with peaking time 0.5 already set")
            settingsflag = sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, Powerflag=True)
            return settingsflag
        else:
            logging.info("Source settings with peaking time of 0.5 were not set")
            settingsflag = sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, Powerflag=False)
            return settingsflag
    if setting_type == "source_peak_one":
        if ispulser == "False" and poweredAMsFlag == "True" and peakingtime == "1.0":
            logging.info("Source settings with peaking time 1 already set")
            settingsflag = sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, Powerflag=False)
            return settingsflag
        else:
            logging.info("Source settings with peaking time of 1 were not set")
            settingsflag = sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, Powerflag=False)
            return settingsflag

def sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, Powerflag):
    logging.info("Sending settings to device")
    ssflag = setSystemSettings(Powerflag)
    if ssflag == False:
        return ssflag
    amflag = setAmSettings()
    if amflag == False:
        return amflag
    gmflag = setGmSettings(pulse_freq, enable_pulse, pulse_count)
    if gmflag == False:
        return gmflag
    asicflag = setASICSettings(test_pulse, peakingtime_ms)
    if asicflag == False:
        return asicflag
    channelflag = setChannelSettings(enable_test_cap)
    if channelflag == False:
        channelflag
    print("All settings complete")
    return True

@app.route('/', methods=['GET', 'POST'])
def submitForm():
    if request.method == 'POST':
        form = request.form
        print("Form recieved")
        print(form)
        logging.info(form)
        if request.form["process"] == "Run":
            headerdata = []
            scanResults = []
            headerdata.append(form["user"])
            headerdata.append(form["wonumber"])
            
            sensors = []
            sensors.append(form["topright"])
            sensors.append(form["topleft"])
            sensors.append(form["bottomright"])
            sensors.append(form["bottomleft"])
            
            for sensor in sensors:
                matchflag = checkForMatch(form["wonumber"], sensor)
                if matchflag == False:
                    return render_template('index.html', headerdata=headerdata, data="One or more Serial numbers did not match WO #")
                else:
                    continue

            tests = {"360": [form["360"],"360 Test"], 
                     "373": [form["373"], "373 Test"]}
                     #"pulser": [form["pulser"], "Pulser Test"]}
            if form["360"] == "True":
                toTest = "360"
            elif form["373"] == "True":
                toTest = "373"
            #elif form["pulser"] == "True":
                #toTest = "pulser"
            else:
                print("test not found")
                return render_template('index.html', headerdata=headerdata, scanResults=scanResults)
            
            print(f"running {toTest}")
            logging.info(f"running {toTest}")

            currentTest = Dmatrix(form["wonumber"], toTest, sensors)
            runtest = Dmatrix.main(currentTest)
            if runtest == True:
                print(f"test {tests[toTest][1]} at {sensors} passed")
                results = [i for i in sensors if i != ""]
                results.insert(0, "All Tests Completed successfully")
                return render_template('index.html', headerdata=headerdata, scanResults=results)
            else:
                print(f"{tests[toTest][1]} failed")
                errorcode = f"{tests[toTest][1]} failed or did not complete. {runtest}"
                return render_template('index.html', headerdata=headerdata, data=errorcode)  

    return render_template('index.html')

@app.route("/connection", methods=['GET','POST'])
def get_connected():
    if request.method == 'POST':
        ifconnected = connectToApi("192.168.1.148","192.168.1.149")
        if ifconnected == True:
            results = {"status": 1 }
            return jsonify(results)
        elif ifconnected == False:
            results = {"status": 0}
            return jsonify(results)

@app.route("/send_settings", methods=['GET','POST'])
def send_device_settings():
    if request.method == 'POST':
        settings = request.form.get('settings')
        if settings == "pulser":
            #def checkSettings(setting_type, pulse_freq, enable_pulse, pulse_count, test_pulse, enable_test_cap):
            pulsercheck = checkSettings("Pulser", dm.GMPulserFreq_100Hz, True, 0, 185, 0.5, True)
            if pulsercheck == True:
                return jsonify({"check_status": 1})
            else:
                return jsonify({"check_status": 0})
        elif settings == "source":
            sourcecheck = checkSettings("Source", dm.GMPulserFreq_100Hz, False, 0, 0, 0.5, False)
            if sourcecheck == True:
                return jsonify({"check_status": 1})
            else:
                return jsonify({"check_status": 0})
        elif settings == "source1":
            sourcecheck = checkSettings("source_peak_one", dm.GMPulserFreq_100Hz, False, 0, 0, 1, False)
            if sourcecheck == True:
                return jsonify({"check_status": 1})
            else:
                return jsonify({"check_status": 0})
        


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0", port="5000")
