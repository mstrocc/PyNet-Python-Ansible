#!/usr/bin/env python
# This is a test script meant to show how to use "with" and "open" to opena text file.
# The it iterates thorugh each line in the file and enumerates each line as a tuple
# It then prints the tuple
# It then prints the type function each line is at the very end, which is a tuple
# It is a stupid script that is just meant to show useage.
# I must buidl upon it to use the open and with functions to iterate through each line of the file
import readline
with open("/home/mstrocchia/PyNet-Python-Ansible/cisco_ipsec.txt") as cisco:
    for line in enumerate(cisco):
        print line
    print type(line)
        


