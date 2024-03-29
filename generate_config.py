import json

config = {}

title = raw_input("Title: ")
author = raw_input("Author: ")
comment = raw_input("Comment: ")
config['title'] = title
config['author'] = author
config['comment'] = comment

numb = int(raw_input("Number of VM's do you want: "))

config['vm'] = {}
for vm in range(0,numb):
    name = str(raw_input("Example: ubuntu17 \nVM Name: "))
    disk = str(raw_input("Example: /storage/iso/ubuntu.iso \nFull path to the disk: "))
    ram = str(raw_input("Example: 1024 \nRAM (in MB): "))
    network = str(raw_input("Example: 1 OR 1,00:11:22:33:44:55 \nNetwork: "))
    config['vm'][name] = {}
    config['vm'][name]['disk'] = disk
    config['vm'][name]['ram'] = ram
    config['vm'][name]['network'] = network

option = str(raw_input("Do you want to set up dhcp? (Y/N) "))
if option == "Y":
    config['dhcp'] = {}
    numb = int(raw_input("How many DHCP servers do you want?: "))
    for server in range(0,numb):
        network_id = str(raw_input("Example: 1 \nNetwork: "))
        cidr = str(raw_input("Example: 192.168.1.1/24 \ncidr: "))
        tapip = str(raw_input("Example: 192.168.1.1 \nTap/dhcp server IP: "))
        startip = str(raw_input("Example: 192.168.1.10 \nStart IP: "))
        endip = str(raw_input("Example: 192.168.1.100 \nEnd IP: "))
        config['dhcp'][network_id] = {}
        config['dhcp'][network_id]['cidr'] = cidr
        config['dhcp'][network_id]['tapip'] = tapip
        config['dhcp'][network_id]['startip'] = startip
        config['dhcp'][network_id]['endip'] = endip

option = str(raw_input("Do you want internet connectivity? (Y/N) "))
if option == "Y":
    config['internet'] = {}
    cidr_i = str(raw_input("Example: 192.168.1.1/24 \ncidr: "))
    outinterface = str(raw_input("Example: eth0 \nTraffic out interface: "))
    config['internet']['cidr'] = cidr_i
    config['internet']['outinterface'] = outinterface

print json.dumps(config)
