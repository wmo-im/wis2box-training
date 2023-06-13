# this is the wis2box base setup script to create the student-vm as used in the wis2box-training
# using base OS: Ubuntu 20.04 LTS (Focal)

# install ecCodes, pymetdecoder, csv2bufr, synop2bufr
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

sudo pip3 install https://github.com/wmo-im/pymetdecoder/archive/refs/tags/v0.1.7.zip
sudo pip3 install https://github.com/wmo-im/csv2bufr/archive/refs/tags/v0.6.3.zip
sudo pip3 install https://github.com/wmo-im/synop2bufr/archive/refs/tags/v0.4.1.zip
python3 -m eccodes selfcheck

# install various utilities
sudo apt-get -y install mosquitto-clients nano vim

# install MinIO, pywis-pubsub, pywiscat
sudo pip3 install minio==7.1.13
sudo pip3 install pywis-pubsub
sudo pip3 install https://github.com/wmo-im/pywiscat/archive/master.zip
sudo pip3 install https://github.com/wmo-cop/pyoscar/archive/master.zip

# install the Docker engine, Python 3.8 and Docker Compose
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update
sudo apt-get install -y docker-ce python3.8 python3-pip
sudo pip3 install pip --upgrade
sudo pip3 install pyopenssl --upgrade
sudo pip3 install docker-compose==1.29.2 requests==2.26.0 urllib3==1.26.0

# (re-)download wis2box
cd ~/
rm -rf wis2box-1.0b4/
wget https://github.com/wmo-im/wis2box/releases/download/1.0b3/wis2box-setup-1.0b4.zip
unzip wis2box-setup-1.0b4.zip
rm wis2box-setup-1.0b4.zip

# (re-)download exercise materials
rm -rf exercise-materials/
wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
unzip exercise-materials.zip
rm -rf exercise-materials.zip
