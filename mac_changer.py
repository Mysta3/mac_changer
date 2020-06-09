#!/usr/bin/env python

# import modules
import subprocess
import optparse
import re


# Read terminal commands
def get_arguments():
    parser = optparse.OptionParser()  # create object class
    # add options to use within cli
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()  # returns options and arguments
    if not options.interface:
        parser.error("[-] Please specify an interface , use --help for more info.")  # code to handle error
    elif not options.new_mac:
        parser.error("[-] Please specify new a MAC , use --help for more info.")         # code for error
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    print("[+] New Mac: " + new_mac)

def get_current_mac(interface):
    # execute & read config - grab current mac address
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac)) # casting any value as a string

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not change.")



