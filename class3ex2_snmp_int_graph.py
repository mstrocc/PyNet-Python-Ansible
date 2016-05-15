#!/usr/bin/env python

from snmp_helper import snmp_get_oid_v3, snmp_extract
import line_graph
import time
from getpass import getpass

def get_interface_stats(snmp_device, snmp_user, stat_type, row_number):
    '''
    stat_type can be 'in_octets, out_octets, in_ucast_pkts, out_ucast_pkts

    returns the counter value as an integer
    '''

    oid_dict = {
        'in_octets': '1.3.6.1.2.1.2.2.1.10',
        'out_octets': '1.3.6.1.2.1.2.2.1.16',
        'in_ucast_pkts': '1.3.6.1.2.1.2.2.1.11',
        'out_ucast_pkts': '1.3.6.1.2.1.2.2.1.17',
    }

    if not stat_type in oid_dict.keys():
        raise ValueError("Invalid value for that stat_type")

    # Make sure row_number can be converted into an integer
    row_number = int(row_number)

    # Append row number to OID
    oid = oid_dict[stat_type]
    oid = oid + '.' + str(row_number)

    snmp_data = snmp_get_oid_v3(snmp_device, snmp_user, oid)
    return int(snmp_extract(snmp_data))

def main():
    '''
    Connect to router via SNMPv3

    Create two graphs in/out octeys and in/out packets
    '''

    debug = False

    # SMPNv3 connection Parameters
    ip_addr = raw_input("Enter router IP: ")
    a_user = 'pysnmp'
    my_key = getpass(prompt="Auth + Encryption Key: ")
    auth_key = my_key
    encrypt_key = my_key

    snmp_user = (a_user, auth_key, encrypt_key)

    pynet_rtr1 = (ip_addr, 7961)
    snmp_device = pynet_rtr1

    # Fa4 is in rownumber5in the MIB-2 interfaces table
    row_number = 5

    graph_stats = {
        "in_octets": [],
        "out_octets": [],
        "in_ucast_pkts": [],
        "out_ucast_pkts": [],
    }
    base_count_dict = {}

    # Enter a loop gathering SNMP date every 5 minutes