
from flask import Flask, request, jsonify, render_template
from icecream import ic
from time import sleep
from testing.DMatrix_Commands import Dmatrix
from testing.DMatrix_Util import connectToApi, setSystemSettings, setAmSettings, setGmSettings, setASICSettings, setChannelSettings, maskChannels, initializeDevice
import DMatrix_internal as dm
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import re
import requests
from testing.DMatrix_Redis import getRedisClient

"""
NOTE: Lines containing "43" in this file:
Line 17: logging.basicConfig(handlers=[TimedRotatingFileHandler(f"/media/evfile01/eV common/Production/logging/360_373_unmounted/kev360_373_unmounted_testing_debug_43.log", when="W6", backupCount=5, atTime=rotatetime)],
Line 346: redis_client.delete("process_messages_43")
Line 348: redis_client.rpush("process_messages_43", "Starting Testings")
Line 363: redis_client.rpush("process_messages_43", f"Testing Serial number: {sensor}")
Line 378: redis_client.rpush("process_messages_43", f"Running a {toTest} Test")
Line 395: redis_client.rpush("process_messages_43", "Running a Retest")
Line 409: redis_client.rpush("process_messages_43", "Running a Rework")
Line 423: redis_client.rpush("process_messages_43", "Running a Rework Retest")
Line 437: redis_client.rpush("process_messages_43", "Testing a new Part")
Line 467: redis_client.rpush("process_messages_43", f"Test {toTest} completed")
Line 470: redis_client.rpush("process_messages_43", f"Serial number: {result}")
Line 471: redis_client.rpush("process_messages_43", "All Tests Completed successfully")
Line 472: redis_client.rpush("process_messages_43", f"The new work order number is: {wonumber}")
"""

app = Flask(__name__)
today = datetime.datetime.now().strftime("%Y-%m-%d")
rotatetime = datetime.time(12, 0, 0)
logging.basicConfig(handlers=[TimedRotatingFileHandler(f"/media/evfile01/eV common/Production/logging/360_373_unmounted/kev360_373_unmounted_testing_debug_43.log", when="W6", backupCount=5, atTime=rotatetime)],
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format="{asctime}:{levelname}:{filename}:{message}",
                    style="{")

redis_client = getRedisClient()

def checkForCancel():
    cancel = redis_client.get("cancel")
    cancel = cancel.decode("utf-8")
    print(f"cancel: {cancel}")
    logging.debug(f"cancel: {cancel}")
    if cancel == "True":
        return True
    else:
        return False

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

def checkForVersion(current_serial, model, rework=False, retest=False, reworkretest=False):
    current_serial, partnumber = current_serial.split("-")
    partnumber = "-" + partnumber
    length = len(current_serial)
    foundr = False
    foundt = False
    highest = 0
    if model == "pulser":
        return False
    if reworkretest == True:
        #look for the highest number and add r and t
        status = requests.get(f"http://172.27.2.72:8000/api/v1/dir/serial/kev{model}/{current_serial}")
        if status.status_code == 500:
            return "500"
        versions = requests.get(f"http://172.27.2.72:8000/api/v1/dir/serial/kev{model}/{current_serial}")
        versions = versions.text
        versions = versions.replace("[", "").replace("]", "").replace('"', "")
        versions = versions.split(",")
        logging.info(f"Found versions of workorder number: {versions}")
        if len(versions) > 1:
            for version in versions:
                #look in folder for the exact part number.  if the part number exists then keep that version
                infile = requests.get(f"http://172.27.2.72:8000/api/v1/file/serial/kev{model}/{version}")
                infile = infile.text
                infile = infile.replace("[", "").replace("]", "").replace('"', "").replace(" ", "")
                infile = infile.replace("r", "R").replace("t", "T")
                infile = re.sub(r'R\d+', '', infile)
                infile = re.sub(r'T\d+', '', infile)
                infile = infile.replace("R", "").replace("T", "")
                infile = infile.split(",")
                infile = [x[:length+3] for x in infile]
                logging.info(f"part numbers in file {version}: {infile}")
                if current_serial+partnumber in infile:
                    logging.debug(f"found part number {current_serial+partnumber} in file {version}")
                    if re.search("r", version):
                        foundr = True
                    if re.search("R", version):
                        foundr = True
                    if re.search("t", version):
                        foundt = True
                    if re.search("T", version):
                        foundt = True
                    number = re.search(r'\d+$', version)
                    if number:
                        new_number = int(number.group())
                        if new_number == int(current_serial):
                            continue
                        if new_number > highest:
                            highest = new_number
                else:
                    continue
                
            logging.info(f"hightest version found: {highest}")
            logging.info(f"found an r in workorder number: {foundr}")
            logging.info(f"found a t in workorder number: {foundt}")
            return current_serial+"RT"+str(highest+1)+partnumber
        else:
            return current_serial+"RT"+partnumber
    elif rework == True:
        status = requests.get(f"http://172.27.2.72:8000/api/v1/dir/serial/kev{model}/{current_serial}")
        if status.status_code == 500:
            return "500"
        versions = requests.get(f"http://172.27.2.72:8000/api/v1/dir/serial/kev{model}/{current_serial}")
        versions = versions.text
        versions = versions.replace("[", "").replace("]", "").replace('"', "")
        versions = versions.split(",")
        logging.info(f"Found versions of workorder number: {versions}")
        if len(versions) > 1:
            for version in versions:
                infile = requests.get(f"http://172.27.2.72:8000/api/v1/file/serial/kev{model}/{version}")
                infile = infile.text
                infile = infile.replace("[", "").replace("]", "").replace('"', "").replace(" ", "")
                infile = infile.replace("r", "R").replace("t", "T")
                infile = re.sub(r'R\d+', '', infile)
                infile = re.sub(r'T\d+', '', infile)
                infile = infile.replace("R", "").replace("T", "")
                infile = infile.split(",")
                infile = [x[:length+3] for x in infile]
                logging.info(f"part numbers in file {version}: {infile}")
                if current_serial+partnumber in infile:
                    logging.debug(f"found part number {current_serial+partnumber} in file {version}")
                    if re.search("r", version):
                        foundr = True
                    if re.search("R", version):
                        foundr = True
                    if re.search("t", version):
                        foundt = True
                    if re.search("T", version):
                        foundt = True
                    number = re.search(r'\d+$', version)
                    if number:
                        new_number = int(number.group())
                        if new_number == int(current_serial):
                            continue
                        if new_number > highest:
                            highest = new_number

                else:
                    continue
                
            logging.info(f"hightest version found: {highest}")
            logging.info(f"found an r in workorder number: {foundr}")
            logging.info(f"found a t in workorder number: {foundt}")
            if foundt == True:
                return current_serial+"RT"+str(highest+1)+partnumber
            else:
                return current_serial+"R"+str(highest+1)+partnumber
        else:
            return current_serial+"R"+partnumber

        
    elif retest == True:
        status = requests.get(f"http://172.27.2.72:8000/api/v1/dir/serial/kev{model}/{current_serial}")
        if status.status_code == 500:
            return "500"
        versions = requests.get(f"http://172.27.2.72:8000/api/v1/dir/serial/kev{model}/{current_serial}")
        versions = versions.text
        versions = versions.replace("[", "").replace("]", "").replace('"', "")
        versions = versions.split(",")
        logging.info(f"Found versions of workorder number: {versions}")
        if len(versions) > 1:
            for version in versions:
                infile = requests.get(f"http://172.27.2.72:8000/api/v1/file/serial/kev{model}/{version}")
                infile = infile.text
                infile = infile.replace("[", "").replace("]", "").replace('"', "").replace(" ", "")
                infile = infile.replace("r", "R").replace("t", "T")
                infile = re.sub(r'R\d+', '', infile)
                infile = re.sub(r'T\d+', '', infile)
                infile = infile.replace("R", "").replace("T", "")
                infile = infile.split(",")
                infile = [x[:length+3] for x in infile]
                logging.info(f"part numbers in file {version}: {infile}")
                if current_serial+partnumber in infile:
                    logging.debug(f"found part number {current_serial+partnumber} in file {version}")
                    if re.search("r", version):
                        foundr = True
                    if re.search("R", version):
                        foundr = True
                    if re.search("t", version):
                        foundt = True
                    if re.search("T", version):
                        foundt = True
                    number = re.search(r'\d+$', version)
                    if number:
                        new_number = int(number.group())
                        if new_number == int(current_serial):
                            continue
                        if new_number > highest:
                            highest = new_number

                else:
                    continue
                
            logging.info(f"hightest version found: {highest}")
            logging.info(f"found an r in workorder number: {foundr}")
            logging.info(f"found a t in workorder number: {foundt}")
            if foundr == True:
                return current_serial+"RT"+str(highest+1)+partnumber
            else:
                return current_serial+"T"+str(highest+1)+partnumber
        else:
            return current_serial+"T"+partnumber

    else:
        status = requests.get(f"http://172.27.2.72:8000/api/v1/dir/serial/kev{model}/{current_serial}")
        if status.status_code == 500:
            return "500"
        versions = requests.get(f"http://172.27.2.72:8000/api/v1/dir/serial/kev{model}/{current_serial}")
        versions = versions.text
        versions = versions.replace("[", "").replace("]", "").replace('"', "")
        versions = versions.split(",")
        logging.info(f"Found versions of workorder number: {versions}")
        if len(versions) > 0:
            for version in versions:
                infile = requests.get(f"http://172.27.2.72:8000/api/v1/file/serial/kev{model}/{version}")
                infile = infile.text
                infile = infile.replace("[", "").replace("]", "").replace('"', "").replace(" ", "")
                infile = infile.replace("r", "R").replace("t", "T")
                infile = re.sub(r'R\d+', '', infile)
                infile = re.sub(r'T\d+', '', infile)
                infile = infile.replace("R", "").replace("T", "")
                infile = infile.split(",")
                infile = [x[:length+3] for x in infile]
                logging.info(f"part numbers in file {version}: {infile}")
                if current_serial+partnumber in infile:
                    logging.debug(f"found part number {current_serial+partnumber} in file {version}")
                    if re.search("r", version):
                        foundr = True
                    if re.search("R", version):
                        foundr = True
                    if re.search("t", version):
                        foundt = True
                    if re.search("T", version):
                        foundt = True
                    number = re.search(r'\d+$', version)
                    if number:
                        new_number = int(number.group())
                        if new_number == int(current_serial):
                            continue
                        if new_number > highest:
                            highest = new_number

                else:
                    continue

            logging.info(f"hightest version found: {highest}")
            logging.info(f"found an r in workorder number: {foundr}")
            logging.info(f"found a t in workorder number: {foundt}")
            if foundr == True and foundt == True:
                return current_serial+"RT"+str(highest+1)+partnumber
            elif foundr == True:
                return current_serial+"R"+str(highest+1)+partnumber
            elif foundt == True:
                return current_serial+"T"+str(highest+1)+partnumber
            else:
                return current_serial+partnumber
        else:
            return current_serial+partnumber

def checkSettings(setting_type, pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap):
    connectToApi("192.168.1.148","192.168.1.149")
    logging.debug(f"Checking settings for {setting_type}")
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
        if ispulser == "True" and poweredAMsFlag == "True" and peakingtime == "0.5":
            logging.info("Pulser already set ")
            #settingsflag = sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, Powerflag=True)
            return True
        else:
            logging.info("Pulser setting were not set")
            settingsflag = sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, poweredAMsFlag)
            return settingsflag
    if setting_type == "Source":
        if ispulser == "False" and poweredAMsFlag == "True" and peakingtime == "0.5":
            logging.info("Source settings with peaking time 0.5 already set")
            #settingsflag = sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, Powerflag=True)
            return True
        else:
            logging.info("Source settings with peaking time of 0.5 were not set")
            settingsflag = sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, poweredAMsFlag)
            return settingsflag
    if setting_type == "source_peak_one":
        if ispulser == "False" and poweredAMsFlag == "True" and peakingtime == "1.0":
            logging.info("Source settings with peaking time 1 already set")
            #settingsflag = sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, Powerflag=False)
            return True
        else:
            logging.info("Source settings with peaking time of 1 were not set")
            settingsflag = sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, poweredAMsFlag)
            return settingsflag

def sendSettings(pulse_freq, enable_pulse, pulse_count, test_pulse, peakingtime_ms, enable_test_cap, Powerflag):
    logging.info("Sending settings to device")
    initflag = initializeDevice()
    if initflag == False:
        return initflag
    ssflag = setSystemSettings(Powerflag)
    if ssflag == False:
        return ssflag
    amflag = setAmSettings()
    if amflag == False:
        return amflag
    gmflag = setGmSettings(pulse_freq, enable_pulse, pulse_count) #peakingtime_ms, test_pulse, enable_test_cap
    if gmflag == False:
        return gmflag
    asicflag = setASICSettings(test_pulse, peakingtime_ms)
    if asicflag == False:
        return asicflag 
    channelFlag = setChannelSettings(enable_test_cap)
    if channelFlag == False:
        return channelFlag
    maskflag = maskChannels()
    if maskflag == False:
        return maskflag
    print("All settings complete")
    return True

@app.route('/', methods=['GET', 'POST'])
def submitForm():
    if request.method == 'POST':
        form = request.form
        logging.info("Form recieved")
        print(form)
        logging.info(form)
        if request.form["process"] == "Run":
            headerdata = []
            scanResults = []
            wonumber = form["wonumber"]
            headerdata.append(form["user"])
            headerdata.append(wonumber)
            redis_client.delete("process_messages_43")
            redis_client.set("cancel", "False")
            redis_client.rpush("process_messages_43", "Starting Testings")

            sensors = []
            sensors.append(form["topright"])
            sensors.append(form["topleft"])
            sensors.append(form["bottomright"])
            sensors.append(form["bottomleft"])
            logging.info(f"Original Serial numbers: {sensors}")
            
            for sensor in sensors:
                matchflag = checkForMatch(wonumber, sensor)
                if matchflag == False:
                    return "One or more Serial numbers did not match Work Order #", 400
                else:
                    if sensor != "":
                        redis_client.rpush("process_messages_43", f"Testing Serial number: {sensor}")
                    continue

            if form["scantype"] == "360":
                toTest = "360"
                logging.info("Running a 360 test")
            elif form["scantype"] == "373":
                toTest = "373"
                logging.info("Running a 373 test")
            elif form["scantype"] == "pulser":
                toTest = "pulser"
                logging.info("Running a pulser test")
            else:
                logging.debug("Scan type not found")
                return "Scan type not Found, you must select a scan type", 400
            redis_client.rpush("process_messages_43", f"Running a {toTest} Test")

            #tests = {"360": [form["360"],"360 Test"], 
                     #"373": [form["373"], "373 Test"],
                     #"pulser": [form["pulser"], "Pulser Test"]}
            #if form["360"] == "True":
                #toTest = "360"
            #elif form["373"] == "True":
                #toTest = "373"
            #elif form["pulser"] == "True":
                #toTest = "pulser"
            #else:
                #logging.debug("Scan type not found")
                #errorcode="Scan type NOT Found, you must select a scan type" 
                #return render_template('index.html', headerdata=headerdata, data=errorcode)
            
            if form["testype"] == "retest":
                redis_client.rpush("process_messages_43", "Running a Retest")
                for idx, sensor in  enumerate(sensors):
                    if sensor != "":
                        versionflag = checkForVersion(sensor, toTest, retest=True)
                        if versionflag == False:
                            continue
                        elif versionflag == "500":
                            return "Failed to connect to API", 500
                        else:
                            sensors[idx] = versionflag
                            versionflag = versionflag.split("-")
                            wonumber = versionflag[0]

            elif form["testype"] == "rework":
                redis_client.rpush("process_messages_43", "Running a Rework")
                for idx, sensor in  enumerate(sensors):
                    if sensor != "":
                        versionflag = checkForVersion(sensor, toTest, rework=True)
                        if versionflag == False:
                            continue
                        elif versionflag == "500":
                            return "Failed to connect to API", 500
                        else:
                            sensors[idx] = versionflag
                            versionflag = versionflag.split("-")
                            wonumber = versionflag[0]

            elif form["testype"] == "reworkretest":
                redis_client.rpush("process_messages_43", "Running a Rework Retest")
                for idx, sensor in  enumerate(sensors):
                    if sensor != "":
                        versionflag = checkForVersion(sensor, toTest, reworkretest=True)
                        if versionflag == False:
                            continue
                        elif versionflag == "500":
                            return "Failed to connect to API", 500
                        else:
                            sensors[idx] = versionflag
                            versionflag = versionflag.split("-")
                            wonumber = versionflag[0]

            else:
                redis_client.rpush("process_messages_43", "Testing a new Part")
                for idx, sensor in  enumerate(sensors):
                    if sensor != "":
                        versionflag = checkForVersion(sensor, toTest)
                        if versionflag == False:
                            continue
                        elif versionflag == "failed":
                            errorcode = "This file already exists.  Please select a test type"
                            return errorcode, 400
                        elif versionflag == "500":
                            return "Failed to connect to API", 500
                        else:
                            sensors[idx] = versionflag
                            versionflag = versionflag.split("-")
                            wonumber = versionflag[0]
    
            logging.info(f"Modified serail numbers: {sensors}")
            
            print(f"running {toTest}")
            logging.info(f"running {toTest}")
            stopTest = checkForCancel()
            if stopTest == True:
                logging.info("Test Cancelled")
                return "Test Cancelled", 400

            currentTest = Dmatrix(wonumber, toTest, sensors)
            runtest = Dmatrix.main(currentTest)
        
            if runtest == True:
                print(f"test {toTest} at {sensors} passed")
                redis_client.rpush("process_messages_43", f"Test {toTest} completed")
                results = [i for i in sensors if i != ""]
                for result in results:
                    redis_client.rpush("process_messages_43", f"Serial number: {result}")
                redis_client.rpush("process_messages_43", "All Tests Completed successfully")
                redis_client.rpush("process_messages_43", f"The new work order number is: {wonumber}")
                sleep(1)
            else:
                print(f"test {toTest} failed")
                errorcode = f"tests {toTest} failed or did not complete. {runtest}"
                return errorcode, 400 
        
        elif request.form["process"] == "Clear":
            logging.info("UI cleared")
            return render_template('index.html')

    return render_template('index.html')

@app.route("/connection", methods=['GET','POST'])
def get_connected():
    if request.method == 'POST':
        ifconnected = connectToApi("192.168.1.148","192.168.1.149")
        if ifconnected == True:
            results = {"status": 1 }
            logging.info(results)
            return jsonify(results)
        elif ifconnected == False:
            results = {"status": 0}
            logging.info(results)
            return jsonify(results)

@app.route("/send_settings", methods=['GET','POST'])
def send_device_settings():
    if request.method == 'POST':
        settings = request.form.get('settings')
        print(f"Settings form: {settings}")
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
        

@app.route("/reboot", methods=['GET','POST'])
def reboot_device():
    if request.method == 'POST':
        disconnect = dm.sys_disconnect()
        checkconnect = connectToApi("192.168.1.148","192.168.1.149")
        logging.debug(checkconnect)
        logging.info("Rebooting device")
        dm.sys_set_fanCtl(dm.DMATRIX_FAN1, 0)
        dm.sys_set_fanCtl(dm.DMATRIX_FAN2, 0)
        dm.sys_set_resetAllAm(True)
        dm.sys_set_resetAllAm(False)
        dm.gm_set_active(0)
        dm.gm_set_rebootAsic(True)
        dm.gm_set_active(1)
        dm.gm_set_rebootAsic(True)
        dm.gm_set_active(2)
        dm.gm_set_rebootAsic(True)
        dm.gm_set_active(3)
        dm.gm_set_rebootAsic(True)
        dm.gm_set_reloadAsic(True)
        dm.gm_set_reloadAsic(False)
        sleep(10)
        return jsonify({"reboot": 1})

@app.route("/cancel", methods=['GET','POST'])
def cancel_testing():
    if request.method == 'POST':
        redis_client.set("cancel", "True")
        return jsonify({"cancel": 1})

if __name__ == "__main__":
    app.run(debug=False, threaded=True, host="0.0.0.0", port="5000")
