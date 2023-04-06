# this is the wis2box-base-setup script to create the student-vm as used in the wis2box-training
# using base-OS=Ubuntu 20.04 LTS (Focal)

# install the docker engine, python3 and docker-compose
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update
sudo apt-get install -y docker-ce python3.8 python3-pip
sudo pip3 install pip --upgrade
sudo pip3 install pyopenssl --upgrade
sudo pip3 install docker-compose==1.29.2 requests==2.26.0 urllib3==1.26.0

# install eccodes, pymetdecoder, csv2bufr, synop2bufr
ECCODES_VER=2.28.0
ECCODES_DIR=/opt/eccodes
PATH="$PATH;/opt/eccodes/bin"
cd /tmp
sudo apt-get remove -y libeccodes-tools
sudo apt-get install -y build-essential cmake gfortran python3-dev curl unzip
curl https://confluence.ecmwf.int/download/attachments/45757960/eccodes-${ECCODES_VER}-Source.tar.gz --output eccodes-${ECCODES_VER}-Source.tar.gz
tar xzf eccodes-${ECCODES_VER}-Source.tar.gz
mkdir build
cd build 
sudo cmake -DCMAKE_INSTALL_PREFIX=${ECCODES_DIR} -DENABLE_AEC=OFF ../eccodes-${ECCODES_VER}-Source
sudo make
sudo ctest
sudo make install
cd ~/
sudo rm -rf /tmp/build
# update path in .bashrc
echo 'export PATH=$PATH:/opt/eccodes/bin' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/eccodes/lib' >> ~/.bashrc
# update current paths
export PATH="$PATH:/opt/eccodes/bin"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/eccodes/lib"

sudo pip3 install https://github.com/wmo-im/pymetdecoder/archive/refs/tags/v0.1.5.zip
sudo pip3 install https://github.com/wmo-im/csv2bufr/archive/refs/tags/v0.5.1.zip
sudo pip3 install https://github.com/wmo-im/synop2bufr/archive/refs/tags/v0.3.2.zip

# install various
sudo apt-get -y install mosquitto-clients nano vim

# install minio, pywis2-pubsubs, pywwiscat
sudo pip3 install minio==7.1.13
sudo pip3 install pywis-pubsub
sudo pip3 install https://github.com/wmo-im/pywiscat/archive/master.zip

python3 -m eccodes selfcheck
