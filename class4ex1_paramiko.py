#!/usr/bin/env python

import paramiko
from getpass import getpass
password = getpass(prompt="pyclass password")
username = 'pyclass'
ip = '50.76.53.27'
port = 8022
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip_addr, username=username, password=password, look_for_keys=False, allow_agent=False, port=port)
ssh_connect = ssh.invoke_shell()
ssh.send('terminal length 0\n')
ssh.send('sh version\n')
output = ssh.recv(65535)
print output


