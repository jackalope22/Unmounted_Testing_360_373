from DMatrix_Util import connectToApi
import DMatrix_internal as dm

def main():
    connectToApi("192.168.1.148","192.168.1.149")
    udpport = dm.sys_get_udpPort()
    udpport = str(udpport)[10].strip("}")
    print(f"upd port: {udpport}")
    ipaddress = dm.sys_get_newDeviceIP()
    ipaddress = str(ipaddress)[5].strip("}")
    print(f"Device ip address in decimal: {ipaddress}")
    gateway = dm.sys_get_newDeviceGateway()
    gateway = str(gateway)[5].strip("}")
    print(f"Device Gateway: {gateway}")

main()