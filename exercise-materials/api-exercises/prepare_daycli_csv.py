# the following code shows how to prepare a CSV string
# using data extracted from the wis2box OGC API
# the script requires 2 input parameters: date and station-id

# Configure these parameters in the code below:
# Set WIS2BOX_API_URL to your wis2box OAPI URL
# Set COLLECTION_ID to the collection you want to query
WIS2BOX_API_URL = "http://localhost/oapi"
COLLECTION_ID = "urn:wmo:md:int-wmo-example:synop-dataset"

import requests
from datetime import datetime

# check at least 2 parameters are provided
# if not, print usage and exit
import sys
if len(sys.argv) != 3:
    print("Usage: python3 prepare_daycli_csv.py <date> <WIGOS-station-id>")
    print("Example: python3 prepare_daycli_csv.py 2025-09-21 0-340-0-SRDH3")
    sys.exit(1)

wigos_id = sys.argv[2]
try:
    my_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
except ValueError:
    print("Error: date must be in format YYYY-MM-DD")
    sys.exit(1)
my_date_range_str = f"{sys.argv[1]}T00:00:00Z/{sys.argv[1]}T23:59:59Z",

URL = f"{WIS2BOX_API_URL}/collections/{COLLECTION_ID}/items"
PARAMS = {
    "datetime":  my_date_range_str,
    "name": "air_temperature", # filter on air_temperature parameter, take care unit is CELSIUS
    "wigos_station_identifier": wigos_id,
    "format": "json"
}

try:
    response = requests.get(URL, params=PARAMS)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from {URL}")
    sys.exit(1)

data = response.json()

print(f"Number of features: {len(data['features'])}")

# min_hour in selected range
min_hour = None

# extract min, max, avg temperature
temps = []
for feature in data['features']:
    name = feature['properties'].get('name')
    value = feature['properties'].get('value')
    if name == 'air_temperature' and value is not None:
        # convert from Celsius to Kelvin before appending to list
        temps.append(value + 273.15)
if len(temps) == 0:
    print("No temperature data found")
    exit(1)

# get coordinates from the first feature
coordinates = data['features'][0]['geometry']['coordinates']

# calculate min, max, avg temperature from the list of temperatures
min_temp = min(temps)
max_temp = max(temps)
avg_temp = sum(temps) / len(temps)

# calculate parameters from wigos_id
wsi_series = int(wigos_id.split("-")[0])
wsi_issuer = int(wigos_id.split("-")[1])
wsi_issue_number = int(wigos_id.split("-")[2])
wsi_local = str(wigos_id.split("-")[3])
wmo_block_number = '' if wsi_issuer != 20000 else wsi_local[0:2]
wmo_station_number = '' if wsi_issuer != 20000 else wsi_local[2:5]

my_data = {
    "wsi_series": wsi_series,
    "wsi_issuer": wsi_issuer,
    "wsi_issue_number": wsi_issue_number,
    "wsi_local": wsi_local,
    "wmo_block_number": wmo_block_number,
    "wmo_station_number": wmo_station_number,
    "latitude": coordinates[1], 
    "longitude": coordinates[0],
    "station_height_above_msl": coordinates[2],
    "temperature_siting_classification": 255, # unknown
    "precipitation_siting_classification": 255, # unknown
    "averaging_method": 2, # averaged over 24 hours
    "year": my_date.year,
    "month": my_date.month,
    "day": my_date.day,
    "precipitation_day_offset": None,
    "precipitation_hour": None,
    "precipitation_minute": None,
    "precipitation_second": None,
    "precipitation": None,
    "precipitation_flag": None,
    "fresh_snow_day_offset": None,
    "fresh_snow_hour": None,
    "fresh_snow_minute": None,
    "fresh_snow_second": None,
    "fresh_snow_depth": None,
    "fresh_snow_depth_flag": None,
    "total_snow_day_offset": None,
    "total_snow_hour": None,
    "total_snow_minute": None,
    "total_snow_second": None,
    "total_snow_depth": None,
    "total_snow_depth_flag": None,
    "thermometer_height": 2, # standard height 2m ? CHECK
    "maximum_temperature_day_offset": 0,
    "maximum_temperature_hour": 0,
    "maximum_temperature_minute": 0,
    "maximum_temperature_second": 0,
    "maximum_temperature": max_temp,
    "maximum_temperature_flag": 0,
    "minimum_temperature_day_offset": 0,
    "minimum_temperature_hour": 0,
    "minimum_temperature_minute": 0,
    "minimum_temperature_second": 0,
    "minimum_temperature": min_temp,
    "minimum_temperature_flag": 0,
    "average_temperature_day_offset": 0,
    "average_temperature_hour": 0,
    "average_temperature_minute": 0,
    "average_temperature_second": 0,
    "average_temperature": f"{avg_temp:.2f}",
    "average_temperature_flag": 0
}

# print CSV header
header = ",".join(my_data.keys())
# print CSV data
data = ",".join([str(v) if v is not None else "" for v in my_data.values()])

# write a CSV file
output_file = f"{wigos_id}_{my_date.strftime('%Y%m%d')}_daycli_from_api.csv"
with open(output_file, "w") as f:
    f.write(header + "\n")
    f.write(data + "\n")
print(f"Data written to {output_file}")