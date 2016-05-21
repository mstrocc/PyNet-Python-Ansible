#!/usr/bin/env python

from getpass import getpass
from netmiko import ConnectHandler
from test_devices import pynet1, pynet2, juniper_srx

def main():
    '''
    Using Netmiko enter into configuation mode on a network device.

    Verify that you are currently in configration mode.
    '''

    ip_addr = raw_input("Enter IP Address: ")
    password = getpass()

    for a_dict in (pynet1, pynet2):
        a_dict['ip'] = ip_addr
        a_dict['password'] = password
    

        net_connect2 = ConnectHandler(**a_dict)
        net_connect2.config_mode()

        print "\n>>>"
        print "Checking {}:{} is in configuration mode.".format(net_connect2.ip, net_connect2.port)
        print "Config mode check: {}".format(net_connect2.check_config_mode())
        print "Current prompt: {}".format(net_connect2.find_prompt())
        print ">>>>\n"

if __name__ == "__main__":
    main()
