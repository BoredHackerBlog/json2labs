import os, sys, signal, json
from time import sleep
from minimega_manage import *

#https://stackoverflow.com/a/1112350
def exit_signal(sig, frame):
    print "Cleaning up and exiting"
    minimega_stop()
    network_clean()
    print "Bye!"
    sys.exit(0)

signal.signal(signal.SIGINT, exit_signal)

minimega_binary = "/opt/json2labs/minimega"
miniweb_binary = "/opt/json2labs/miniweb"
web_directory = "/opt/json2labs/web"

#test installation files and minimega
def test_install():
    print "If there are failures, try running the install script again"
    if os.path.isfile(minimega_binary) == False:
        print "Fail: Minimega binary does not exist"
        quit()
    if os.path.isfile(miniweb_binary) == False:
        print "Fail: Miniweb binary does not exist"
        quit()
    if os.path.isdir(web_directory) == False:
        print "Fail: Web directory does not exist"
        quit()
    print "All of the files seem to be here"
    print "Running minimega"
    minimega_connect()
    check_output = minimega_cmd("check")
    if not json.loads(check_output)["Resp"][0]["Error"]:
        print "Minimega seems to be working"
    else:
        print "Fail: Something went wrong with minimega"
        print check_output
    minimega_stop()

#Entry point
#Check if root
if os.geteuid() != 0:
    print "Run this as root"
    quit()

#Check args
if len(sys.argv) != 2 : #if not two args
    print "Your running options:"
    print "Test installation: python json2labs.py --test"
    print "Running json lab config file: python json2labs.py filename.json"
    print "Make sure you test and verify everything is working before running VM's with a json file!"
    quit()
elif sys.argv[1] == "--test": #if --test, then run testing
    print "====Test installation===="
    test_install()
    quit()
elif os.path.isfile(sys.argv[1]) == False: #if json file does not exist
    print "File you specified does not exist"
    quit()

json_config = json.loads(open(sys.argv[1],"r").read())

print "====JSON Info===="
print "Title: " + json_config['title']
print "Author: " + json_config['author']
print "Comment: " + json_config['comment']

print "====Starting minimega and miniweb===="
minimega_connect()
enable_ksm()

print "====Setting up dhcp===="
if json_config.has_key('dhcp'):
    for tap in json_config['dhcp']:
        dhcp(tap, json_config['dhcp'][tap]['cidr'],json_config['dhcp'][tap]['tapip'],json_config['dhcp'][tap]['startip'],json_config['dhcp'][tap]['endip'])

print "====Setting up VM's===="
if json_config.has_key('vm'):
    for vm in json_config['vm']:
        vm_make(vm, json_config['vm'][vm]['ram'], json_config['vm'][vm]['disk'], json_config['vm'][vm]['network'])

print "====Starting up VM's===="
vm_start()

print "====Setting up networking===="
if json_config.has_key('internet'):
    network_setup(json_config['internet']['cidr'],json_config['internet']['outinterface'])

print "====VNC Access===="
if json_config.has_key('vm'):
    for vm in json_config['vm']:
        port = json.loads(vm_vncport(vm))['Resp'][0]['Tabular'][0][0]
        print "VM Name: %s \t VNC Port: %s"%(vm, port)

print "Web server should be running on port 9001.\nYou can access VM's through your browser\nInternet Explorer seems to work the best..."

print "====Press Control+C to stop and exit===="
signal.pause()
