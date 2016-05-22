#!/usr/bin/env python

from getpass import getpass
from netmiko import ConnectHandler
from test_devices import pynet1, pynet2, juniper_srx

def main():
    '''
    Use Netmiko to change the logging buffer size on pynet-rtr2.
    '''

    ip_addr = raw_input("Enter IP address: ")
    password = getpass()

    # Get connection parameters setup correctly
    for a_dict in (pynet1, pynet2):
        a_dict['ip'] = ip_addr
        a_dict['password'] = password
        a_dict['verbose'] = False
    
    # Loop through each router and issue config command via config_file
    for a_device in (pynet1, pynet2):
        
        net_connect = ConnectHandler(**a_device)
        net_connect.send_config_from_file(config_file='config_file.txt')
        output = net_connect.send_command("show run | i logging")
    
        print
        print "Device: {}:{}".format(net_connect.ip, net_connect.port)
        print
        print output
        print

if __name__ == "__main__":
    main()
