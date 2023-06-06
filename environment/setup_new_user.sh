# this is a  simple script to create a new user on the local training hardware
# and ensure the user has required materials in the home-directory

sudo useradd -p $(openssl passwd -1 "wis2training") "$USERNAME" -m -G docker,sudo --shell /bin/bash
sudo cp -rf exercise-materials/ /home/`echo $USERNAME`/exercise-materials/
sudo cp -rf wis2box-1.0b3/ /home/`echo $USERNAME`/wis2box-1.0b3/

echo WIS2BOX_HOST_DATADIR=/home/`echo $USERNAME`/exercise-materials/wis2box-test-data/ > /tmp/dev.env
echo WIS2BOX_URL=http://`echo $USERNAME`.wis2.training >> /tmp/dev.env
echo WIS2BOX_API_URL=http://`echo $USERNAME`.wis2.training/oapi >> /tmp/dev.env
echo LOG_LEVEL=INFO >> /tmp/dev.env
sudo cp /tmp/dev.env /home/testuser/wis2box-1.0b3/

sudo chown -R `echo $USERNAME`:`echo $USERNAME` /home/`echo $USERNAME`

sudo ls -lh /home/`echo $USERNAME/*`
sudo cat /home/`echo $USERNAME`/wis2box-1.0b3/dev.env

# pre-ingest data 
sudo cp /tmp/dev.env wis2box-1.0b3
cd wis2box-1.0b3
python3 wis2box-ctl.py start
sleep 5
python3 wis2box-ctl.py execute wis2box data add-collection /data/wis2box/metadata/discovery/mwi-surface-weather-observations.yml
python3 wis2box-ctl.py execute wis2box metadata discovery publish /data/wis2box/metadata/discovery/mwi-surface-weather-observations.yml
python3 wis2box-ctl.py execute wis2box data ingest -th mwi.mwi_wmo_demo.data.core.weather.surface-based-observations.synop -p /data/wis2box/observations/malawi-2023-05-29/
sleep 30
python3 wis2box-ctl.py execute wis2box metadata station publish-collection
python3 wis2box-ctl.py stop