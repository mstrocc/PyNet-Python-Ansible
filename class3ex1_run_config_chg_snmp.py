#!/usr/bin/env python

import cPickle as pickle
import os.path
from getpass import getpass

from snmp_helper import snmp_get_oid_v3, snmp_extract
from email_helper import send_mail

from datetime import datetime

# Constants
DEBUG = True

# 300 seconds (converted to hundredths of seconds)
RELOAD_WINDOW = 300 * 100

#Uptime when running config last changed

RUN_LAST_CHANGED = '1.3.6.1.4.1.9.9.43.1.1.1.0'

# Relevant SNMP OIDs
SYS_NAME = '1.3.6.1.2.1.1.5.0'
SYS_UPTIME = '1.3.6.1.2.1.1.3.0'

def obtain_saved_objects(file_name):
    '''
    Read in previoulsy saved objects from a pickle file

    Returns a dict:
    {
        'device_name': device_object,
        'device_name': device_object,
    }

    '''

    # Check that the pickle file exists
    if not os.path.isfile(file_name):
        return{}

    # Read in any saved network devices
    net_devices = {}
    with open(file_name, 'r') as f:
        while True:
            try:
                tmp_device = pickle.load(f)
                net_devices[tmp_device.device_name] = tmp_device
            except EOFError:
                break

    return net_devices

def send_notification(net_device):
    '''
    Send email noticatction regarding modified device
    '''

    current_time = datetime.now()

    sender = 'mstrocc@hotmail.com'
    recipient = 'mstrocc@gmail.com'
    subject = 'Device {0} was modified'.format(net_device.device_name)

    message = '''
The running configuration of {0} ws modified.

This change was detected at: {1}
'''.format(net_device.device_name, current_time)

    if send_mail(recipient, subject, message, sender):
        print 'Email notification sent to {}'.format(recipient)
        return True

class NetworkDevice(object):
    '''
    Simple object to store network device information
    '''

    def __init__(self, device_name, uptime, last_changed, config_changed=False):
        self.device_name = device_name
        self.uptime = uptime

        # The uptime value in hundredths of seconds when running configration
        # was last changed
        self.last_changed = last_changed
        self.run_config_changed = config_changed

def main():
    '''
    Check if the running coinfug has changedm send an email notification when this ocurrs.
    
    Logic for detecting the running config has chagned:
        Normal (non-reboot):

            # Did RUN_LAST_Changed increase
            if RUN_LAST_CHANGED > network_device_object.last_changed

        Reboot case:

            RUN_LAST_CHANGED decreases (i.e < network_device_object.last_cahnged

            Righ after reboot run_last_changed isudated upon load of running-config from startup-config

            Create a grace window (reload_window) for values of RUN_LAST_CHANGED.
            In other words as long as RUN_LAST_CHANGED is <= RELOAD_WINDOW assum no running config changes

            If RUN_LAST_CHANGED is > RELOAD_WINDOW assume running config was changed
    '''

    # Pickle file for storing previous runninglastchanged timestamp
    net_dev_file ='netdev.pkl'

    # SNMPV3 Connection Paramters
    ip_addr = raw_input("Enter IP of Router: ")
    a_user = 'pysnmp'
    my_key = getpass(prompt="Auth + Encryption Key: ")
    auth_key = my_key
    encrypt_key = my_key
    snmp_user = (a_user, auth_key, encrypt_key)
    pynet_rtr1 = (ip_addr, 7961)
    pynet_rtr2 = (ip_addr, 8061)
    
    print '\n***Checking for device changes***'
    
    saved_devices = obtain_saved_objects(net_dev_file)
    print "{0} devices were previoulsly saved\n".format(len(saved_devices))

    # Temporarily store the current devices in a dictionary
    current_devices = {}

    # Connect to each device / retrieve last changed time
    for a_device in (pynet_rtr1, pynet_rtr2):

        snmp_results = []
        for oid in (SYS_NAME, SYS_UPTIME, RUN_LAST_CHANGED):
            try:
                value = snmp_extract(snmp_get_oid_v3(a_device, snmp_user, oid=oid))
                snmp_results.append(int(value))
            except ValueError:
                snmp_results.append(value)

        device_name, uptime, last_changed = snmp_results

        if DEBUG:
            print "\nConnected to device = {0}".format(device_name)
            print "Last changed timestamp = {0}".format(last_changed)
            print "Uptime = {0}".format(uptime)

        # see if this devide has been previously saved
        if device_name in saved_devices:

            saved_device = saved_devices[device_name]
            print "{0} {1}".format(device_name, (35 - len(device_name))*'.'),

            # Check for a reboot (did uptime decrease or last_change decrease?)
            if uptime < saved_device.uptime or last_changed < saved_device.last_changed:
            
                if last_changed <= RELOAD_WINDOW:
                    print "Device Reloaded...not changed"
                    current_devices[device_name] = NetworkDevice(device_name, uptime, last_changed, False)
            
                else:
                    print "Device Relaoded...and changed"
                    current_devices[device_name] = NetworkDevice(device_name, uptime, last_changed, True)
                    send_notification(current_devices[device_name]) 

            # running config last_changed is the same
            elif last_changed == saved_device.last_changed:
                print 'not cahnged'
                current_devices[device_name] = NetworkDevice(device_name, uptime, last_changed, False)
  
            # running conig was modified
            elif last_changed > saved_device.last_changed:
                print "CHANGED"
                current_devices[device_name] = NetworkDevice(device_name, uptime, last_changed, True) 
        
                send_notification(current_devices[device_name])

            else:
                raise ValueError()

        else:
            # New Device, just save it
            print "{0} {1}".format(device_name, (35 - len(device_name))*'.'),
            print "saving new device"
            current_devices[device_name] = NetworkDevice(device_name, uptime, last_changed, False)

    # Write the devices to a pickle file
    with open(net_dev_file, 'w') as f:
        for dev_obj in current_devices.values():
            pickle.dump(dev_obj, f)

    print

if __name__ == "__main__":
    main()
    

    
 



