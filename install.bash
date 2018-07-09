#!/bin/bash

#This script needs to be ran as root
if [[ $EUID -ne 0 ]]; then
    echo "Run this as root"
    exit
fi

echo "====Installing required packages===="
apt-get update && apt-get install openvswitch-switch qemu-kvm qemu-utils dnsmasq ntfs-3g iproute python -y
echo "====Making /opt/json2labs directory===="
mkdir /opt/json2labs
echo "====Copying json2labs code into /opt/json2labs===="
cp json2labs.py generate_config.py minimega_manage.py /opt/json2labs/
echo "====Setting minimega in /opt/json2labs===="
cd /opt/json2labs
echo "====Downloading minimega binary===="
wget "https://storage.googleapis.com/minimega-files/minimega-2.4.tar.bz2"
tar xjf minimega-2.4.tar.bz2
echo "====Uncompressing and copying minimega files===="
cp minimega-2.4-release/bin/minimega minimega
cp minimega-2.4-release/bin/miniweb miniweb
cp -R minimega-2.4-release/misc/web/ web/
echo "====Downloading noVNC===="
git clone https://github.com/novnc/noVNC
echo "====Updating noVNC===="
rm -rf web/novnc/*
rm web/vnc.html
mv noVNC/app/ web/novnc/
mv noVNC/core/ web/novnc/
mv noVNC/vendor/ web/novnc/
mv noVNC/vnc.html web/vnc.html
sed -i 's/app\//\/novnc\/app\//g' web/vnc.html
sed -i 's/core\//\/novnc\/core\//g' web/vnc.html
sed -i 's/vendor\//\/novnc\/vendor\//g' web/vnc.html
echo "====Removing unused files and folder===="
rm -rf minimega-2.4-release/
rm minimega-2.4.tar.bz2
rm -rf noVNC/
echo -e "====Run the command below to test installation!!====\nsudo python /opt/json2labs/json2labs.py --test"
