#!/usr/bin/env python

# This is dictionary file containgn basic login information for devices we want to connect to.  It is then imported into the python scripts we decide to use.  It saves itmeon having to reenter the same informaiton over and over again.

pynet1 = {
    'device_type': 'cisco_ios',
    'username': 'pyclass',
    #'name': 'pynet1',
}

pynet2 = {
    'device_type': 'cisco_ios',
    'username': 'pyclass',
    'secret': '',
    'port': 8022,
    #'name': 'pynet2',
}

juniper_srx = {
    'device_type': 'juniper',
    'username': 'pyclass',
    'port': 9822,
    #'name': 'juniper',
}
    
