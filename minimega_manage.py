import socket, os
from time import sleep

minimega_binary = "/opt/json2labs/minimega"
miniweb_binary = "/opt/json2labs/miniweb"
web_directory = "/opt/json2labs/web"
minimega_socket_file = "/tmp/minimega/minimega"

#make connection to minimega socket
def minimega_connect():
    os.system("killall minimega")
    os.system("killall miniweb")
    os.system("killall dnsmasq")
    os.system(minimega_binary + " -nostdin &")
    sleep(5)
    os.system(miniweb_binary + " -root " + web_directory + " &")
    sleep(5)
    global minimega_socket
    minimega_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    minimega_socket.connect(minimega_socket_file)

#send commands to minimega
def minimega_cmd(command):
    input = '{"Command":"%s"}'%(command)
    minimega_socket.send(input)
    output = minimega_socket.recv(10000000)
    return output

#enable KSM
def enable_ksm():
    minimega_cmd("optimize ksm true")

#start dhcp
def dhcp(tap, cidr, tapip, startip, endip):
    minimega_cmd("tap create %s ip %s"%(tap, cidr))
    minimega_cmd("dnsmasq start %s %s %s"%(tapip, startip, endip))

#make vm's
def vm_make(vm_name, vm_memory, vm_disk, vm_net):
    minimega_cmd("vm config memory %s"%(vm_memory))
    minimega_cmd("vm config disk %s"%(vm_disk))
    minimega_cmd("vm config net %s"%(vm_net))
    minimega_cmd("vm launch kvm %s"%(vm_name))

#start vm's
def vm_start():
    minimega_cmd("vm start all")

#get vnc_port
def vm_vncport(vm_name):
    return minimega_cmd(".columns vnc_port .filter name=%s vm info"%(vm_name))

#stop minimega and other related processes
def minimega_stop():
    minimega_cmd("vm kill all")
    minimega_cmd("quit")
    os.system("killall miniweb")
    os.system("killall dnsmasq")

#save iptables rules and setup forwarding
def network_setup(cidr, outinterface):
    os.system("iptables-save > /opt/json2labs/iptables_old")
    os.system("echo 1 | tee -a /proc/sys/net/ipv4/ip_forward")
    os.system("sysctl -w net.ipv4.ip_forward=1")
    os.system("iptables -t nat -A POSTROUTING -o %s -s %s -j MASQUERADE"%(outinterface,cidr))
    os.system("iptables -P FORWARD DROP")
    os.system("iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT")
    os.system("iptables -A FORWARD -s %s -j ACCEPT"%(cidr))
    os.system("iptables -A FORWARD -s %s -d %s -j ACCEPT"%(cidr,cidr))

#restore iptables rules
def network_clean():
    os.system("iptables-restore < /opt/json2labs/iptables_old")
    os.system("rm /opt/json2labs/iptables_old")
