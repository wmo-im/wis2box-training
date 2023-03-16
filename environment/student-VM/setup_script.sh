sudo apt-get -y install mosquitto-clients python3.8 python3-pip unzip
sudo pip3 install docker-compose==1.29.0 requests==2.26.0 urllib3==1.26.0
sudo pip3 install minio==7.1.13
sudo pip3 install pywis-pubsub
sudo pip3 install https://github.com/wmo-im/pywiscat/archive/master.zip
ECCODES_VER=2.28.0
ECCODES_DIR=/opt/eccodes
PATH="$PATH;/opt/eccodes/bin"

sudo apt-get install -y build-essential cmake gfortran python3 python3-pip python3-dev curl 
curl https://confluence.ecmwf.int/download/attachments/45757960/eccodes-${ECCODES_VER}-Source.tar.gz --output eccodes-${ECCODES_VER}-Source.tar.gz
tar xzf eccodes-${ECCODES_VER}-Source.tar.gz
mkdir build
cd build 
sudo cmake -DCMAKE_INSTALL_PREFIX=${ECCODES_DIR} -DENABLE_AEC=OFF ../eccodes-${ECCODES_VER}-Source
sudo make
sudo ctest
sudo make install
sudo apt-get -y install python3-eccodes
#sudo pip3 install https://github.com/wmo-im/synop2bufr/archive/refs/tags/v0.2.0.zip
#sudo pip3 install https://github.com/wmo-im/csv2bufr/archive/refs/tags/v0.5.0.zip