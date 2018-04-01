#!/usr/bin/python
import subprocess
import re
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib2 import urlopen
#I found this on stack overflow once, modified 
#it so it shows device name, MAC Address and IP. 

#import requests

# Store Mac address of all nodes HERE, replace but keep in lower case! 
saved = {
    'xx:xx:xx:xx:xx:xx': 'My laptop',
   
}

# Set wireless interface using ifconfig
interface = "wlan0"

mac_regex = re.compile(r'([a-zA-Z0-9]{2}:){5}[a-zA-Z0-9]{2}')


def parse_arp():
    arp_out = subprocess.check_output(f'arp -i {interface}', shell=True).decode('utf-8')
    if 'no match found' in arp_out:
        return None

    result = []
    for lines in arp_out.strip().split('\n'):
        line = lines.split()
        if interface in line and '(incomplete)' not in line:
            for element in line:
                # If its a mac addr
                if mac_regex.match(element):
                    result.append((line[1], element))
    return result



def print_device(device, num=0):
    device_name = saved[device[1]] if device[1] in saved else 'unrecognised !!'

    print('name: ',device_name,'\nMac:', device[1], '\nIP: ',device[0],',')

if __name__ == '__main__':
    print('Retrieving connected devices ..\n')

    devices = parse_arp()

    if not devices:
        print('No devices found!')

    else:
        try:
            num = 0
            for device in devices:
                num += 1
                print_device(device, num)
        except KeyboardInterrupt as e:
            num = 0
            for device in devices:
                num += 1
                print_device(device, num,",")
