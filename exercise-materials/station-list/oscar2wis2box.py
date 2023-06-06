###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

from collections import OrderedDict
import sys

from pyoscar import OSCARClient

REGION_MAP = {
    1: 'I',
    2: 'II',
    3: 'III',
    4: 'IV',
    5: 'V',
    6: 'VI'
}

if len(sys.argv) != 2 or len(sys.argv[1].split('-')) != 4:
    print('Invalid WSI')
    sys.exit(1)

wsi = sys.argv[1]

client = OSCARClient()

station = client.get_station_report(wsi)

results = OrderedDict({
    'station_name': station['name'],
    'wigos_station_identifier': wsi,
    'traditional_station_identifier': None,
    'facility_type': station['typeName'],
    'latitude': station['locations'][0]['latitude'],
    'longitude': station['locations'][0]['longitude'],
    'elevation': station['locations'][0].get('elevation'),
    'territory_name': station['territories'][0]['territoryName'],
    'wmo_region': REGION_MAP[station['wmoRaId']]
})

if '0-2000' in station['wigosIds'][0]['wid']:
    results['traditional_station_identifier'] = station['wigosIds'][0]['wid'].split('-')[-1]  # noqa

line = ','.join([(str(results[k]) if results[k] is not None else '') for k, v in results.items()])  # noqa

print(line)
