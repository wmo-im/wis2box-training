import os,sys

import logging
logging.basicConfig(level=logging.ERROR)
logging.getLogger("oscar_lib.oscar_client").setLevel(logging.ERROR)
logging.getLogger("oscar_lib.station").setLevel(logging.ERROR)


#from dotenv import load_dotenv
from oscar_lib import OscarClient, extractSchedules, Station, OscarGUIClient
from oscar_lib import OscarInterfaceDummy

region_map = {
    "africa":"I",
    "asia":"II",
    "southAmerica":"III",
    "northCentralAmericaCaribbean":"IV",
    "southWestPacific":"V",
    "europe":"VI",
    "south america":"III",
    "north america, central america and the caribbean":"IV",
    "south-west pacific":"V"
}

if len(sys.argv) != 2 or len(sys.argv[1].split("-")) != 4:
    print("pass WIGOS ID as parameter")
    sys.exit(1)

wsi = sys.argv[1]

client = OscarClient()
#stations = client.oscar_search(params={"territoryName":"KEN"})
stations = client.oscar_search(params={"wigosId":wsi})

for station in stations["data"]["stationSearchResults"]:
  
    station["WMOIndex"] = ""
    
    for wsi in station["wigosStationIdentifiers"]:
        if "0-2000" in wsi["wigosStationIdentifier"]:
            station["WMOIndex"] = wsi["wigosStationIdentifier"].split("-")[3]
     
    station["region"] = region_map[station["region"].lower()]
     
    keys = ["name","wigosId","WMOIndex","stationTypeName","latitude","longitude","elevation","territory","region"]

    # Keetmanshoop Airport,0-20000-0-68312,68321,Land (fixed),-26.53333,18.1166666,1064,Namibia,I
    line = ",".join( [ (str(station[k]) if k in station else "") for k in keys]) 
 
    print(line)