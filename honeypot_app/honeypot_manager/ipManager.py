"""
Configure multiple IPs on single network interface
"""
import sys
import os
import re

def addIp(addr):
    if sys.platform == 'darwin': ## macOS
        add_ip_macos(addr)
    elif 'linux' in sys.platform: ## linux
        add_ip_linux(addr)
    else:
        raise Exception(f"Invalid platform")

def removeIp(addr):
    if sys.platform == 'darwin': ## macOS
        remove_ip_macos(addr)
    elif 'linux' in sys.platform: ## linux
        remove_ip_linux(addr)
    else:
        raise Exception(f"Invalid platform")
        

def add_ip_macos(addr):
    cmd = f"sudo ifconfig en0 alias {addr} netmask 255.255.255.255"
    os.system(cmd)

def remove_ip_macos(addr):
    cmd = f"sudo ifconfig en0 -alias {addr}"
    os.system(cmd)


def add_ip_linux(addr):
    aliasName = re.sub("[^0-9]", "", addr) ## remove non-numeric from addr
    cmd = f'sudo ifconfig eth0:{aliasName} {addr} netmask 255.255.255.0 up'
    os.system(cmd)

def remove_ip_linux(addr):
    aliasName = re.sub("[^0-9]", "", addr) ## remove non-numeric from addr
    cmd = f'sudo ifconfig eth0:{aliasName} {addr} netmask 255.255.255.0 down'
    os.system(cmd)
    return