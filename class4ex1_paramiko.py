#!/usr/bin/env python

import paramiko
import time

from getpass import getpass
password = getpass(prompt="pyclass password: ")
username = 'pyclass'
ip = '50.76.53.27'
port = 8022
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False, port=port)
ssh_connect = ssh.invoke_shell()
output = ssh_connect.recv(65535)
print output

ssh_connect.send("terminal length 0\n")
time.sleep(1)
ssh_connect.send("\n")
time.sleep(1)

ssh_connect.send('sh version\n')
time.sleep(3)
output = ssh_connect.recv(65535)
print output

# It is very important tomake use of the time.sleep command to give the router enought time to generate the command beforeyou try and print it
