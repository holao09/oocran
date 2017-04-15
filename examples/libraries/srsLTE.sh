#!/bin/bash

sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install build-essential -y
sudo apt-get install git -y

#Mandatory dependencies:
#libfftw
sudo apt-get install libfftw3-dev libfftw3-doc -y
#UHD
sudo apt-get install libboost-all-dev libusb-1.0-0-dev python-mako doxygen python-docutils cmake build-essential -y
sudo apt-get install libuhd-dev libuhd003 uhd-host -y
#Optional dependencies:
#BOOST
sudo apt-get install libboost-system-dev libboost-test-dev libboost-thread-dev libqwt-dev libqt4-dev -y
#srsGUI
git clone https://github.com/suttonpd/srsgui.git
cd srsgui
mkdir build
cd build
cmake ../
sudo make install
cd ../..
#VOLK
git clone https://github.com/gnuradio/volk.git
cd volk
mkdir build
cd build
cmake ../
sudo make install
cd ../..
#VBBU
git clone https://github.com/oocran/vbbu.git
cd vbbu
mkdir build
cd build
cmake ../
sudo make install
chmod +x *
path=$(pwd)
ln -s "$path"/* /usr/bin
cd ../..
sudo echo "\nnet.core.rmem_max=50000000" >> /etc/sysctl.conf
sudo echo "\nnet.core.wmem_max=1048576" >> /etc/sysctl.conf
sudo echo "\nroot  -   rtprio    99" >> /etc/security/limits.conf
sudo echo "\nroot    -   memlock   unlimited" >> /etc/security/limits.conf