# pre-ingest data 
sudo cp /tmp/dev.env wis2box-1.0b4
cd wis2box-1.0b4
python3 wis2box-ctl.py start
sleep 30
python3 wis2box-ctl.py execute wis2box data add-collection /data/wis2box/metadata/discovery/mwi-surface-weather-observations.yml
python3 wis2box-ctl.py execute wis2box data add-collection /data/wis2box/metadata/discovery/mwi-surface-weather-observations-reco.yml
python3 wis2box-ctl.py execute wis2box metadata discovery publish /data/wis2box/metadata/discovery/mwi-surface-weather-observations.yml
python3 wis2box-ctl.py execute wis2box metadata discovery publish /data/wis2box/metadata/discovery/mwi-surface-weather-observations-reco.yml
python3 wis2box-ctl.py execute wis2box auth add-token --topic-hierarchy mwi.mwi_wmo_demo.data.recommended.weather.surface-based-observations.synop mysecrettoken -y
python3 wis2box-ctl.py execute wis2box auth add-token -p mwi_wmo_demo:reco mysecrettoken -y
python3 wis2box-ctl.py execute wis2box data ingest -th mwi.mwi_wmo_demo.data.core.weather.surface-based-observations.synop -p /data/wis2box/observations/malawi-preingested-core/
python3 wis2box-ctl.py execute wis2box data ingest -th mwi.mwi_wmo_demo.data.recommended.weather.surface-based-observations.synop -p /data/wis2box/observations/malawi-preingested-reco/
echo "sleep before refresh station links..."
sleep 120
echo "publishing station metadata"
python3 wis2box-ctl.py execute wis2box metadata station publish-collection
echo "done!"
