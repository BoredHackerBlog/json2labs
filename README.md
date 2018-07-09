# json2labs
A project that generates virtual labs based on a json configuration file.

# About
json2labs utilizes a json configuration file as an input and starts up virtual environment based on it.

The minimega project (minimega.org), created by Sandia National Labs, is used for virtual machine management.

Minimega uses qemu/kvm, dnsmasq, and openvswitch for virtualization and networking. Minimega provides miniweb for VM management and access. 

Virtual machines created by json2labs can be accessed via Web (using noVNC) or VNC connection.

Benefits: Changes made to the VM are not saved to disk. Minimega uses qemu/kvm in snapshot mode. Since it's snapshot mode, you can use one qcow2 or iso file to create multiple VM's as well. KSM is used to keep the total memory usage down.

Limitations/Issues: For VNC connection, the mouse cursor does not behave correctly, depending on the VNC software. Use novnc via web server running on port 9001, since that seems to work fine. For the "internet" option, only one CIDR is supported for now.

Check screenshots directory for screenshots and usage example.

# Use Cases
- Labs for a school class or a workshop
- Malware analysis
- Security training (pentesting, DFIR, etc)

# Installation
This has been tested on Ubuntu 16.04 64-bit.

All the files will be in /opt/json2labs/ after installation
```
git clone https://github.com/BoredHackerBlog/json2labs
cd json2labs
sudo bash install.bash

#Testing your installation
sudo python /opt/json2labs/json2labs.py --test
```

# Files
- generate_config.py - Generates JSON configuration based on provided input.
- json2labs.py - Main code for running json2labs. 
- minimega_manage.py - Code for minimega management. It's imported and used by json2labs.py. Does not run directly.
- minimega - Main minimega executable.
- miniweb - Minimega web management/access executable.
- web/ - Files for miniweb.

# Example Configuration file
```
{
	"comment": "This is an example JSON file. Used for running Kali linux",
	"author": "Nobody",
	"title": "Kali Linux",
	"vm": {
		"Linux1": {
			"disk": "/home/research/kali.iso",
			"ram": "1024",
			"network": "1"
		}
	},
	"dhcp": {
		"1": {
			"startip": "192.168.1.10",
			"tapip": "192.168.1.1",
			"cidr": "192.168.1.1/24",
			"endip": "192.168.1.50"
		}
	},
	"internet": {
		"cidr": "192.168.1.1/24",
		"outinterface": "eth0"
	}
}
```
The configuration file above creates a Kali VM with 1G of RAM, with IP between 192.168.1.10-50.

dhcp and internet parts are optional. Check generate_config.py for more info.

# Creating VM's
You can provide .iso files or you can provide .qcow2 files.

VM's can be made by using VirtualBox and selecting .qcow2 as the virtual disk. VM's can also be made using minimega (make sure to disable snapshot mode) or qemu.

Another option is to convert other virtual disk types (vdi, vmdk, etc) to .qcow2.


License: WTFPL