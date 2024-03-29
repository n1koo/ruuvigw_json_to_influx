# Ruuvi GW to influx

Scrappy script to pull data from Ruuvi gateways and dump it to influx.

Some features:

- Able to map macs to names
- Able to scrape N gateways
- Able to dedupe duplicate sensors if found in multiple gateways
- All data is outputted as fields per sensor



**NOTICE**

I'm yet to upgrade to InfluxDB 2.x - this script is only for 1.x

## How to use

See `run.sh` for now on required envvars to run.

Basic flow is something like `python3 ruuvigw_json_to_influx.py --gateway_endpoints=192.168.20.40,192.168.20.69 --dry-run=true`

### Mappings

The script is able to map MACs to names. Please see `mappings.json` as an example. 

If mapping is found `sensor_name` tag will be that name (eg. `autotalli`) but if not then `mac`

## Example run:

```
‽ LOG_LEVEL=DEBUG python3 ruuvigw_json_to_influx.py --influx_db_host 192.168.2.9 --gateway_endpoints=192.168.20.40,192.168.20.69 --dry-run=true
2021-09-12 19:10:19 n1proi9.home ruuvigw_json_to_influx[58190] INFO Starting ruuvi json to Influx script
2021-09-12 19:10:19 n1proi9.home urllib3.connectionpool[58190] DEBUG Starting new HTTP connection (1): 192.168.20.40:80
2021-09-12 19:10:20 n1proi9.home urllib3.connectionpool[58190] DEBUG http://192.168.20.40:80 "GET /history HTTP/1.1" 200 1371
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG 2021-09-12 19:10:19
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG {'data_format': 5, 'humidity': 62.34, 'temperature': 24.18, 'pressure': 1003.15, 'acceleration': 1018.3830320660296, 'acceleration_x': -780, 'acceleration_y': -652, 'acceleration_z': 60, 'tx_power': 4, 'battery': 3038, 'movement_counter': 70, 'measurement_sequence_number': 165, 'mac': 'd54ea64b61d5'}
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG 2021-09-12 19:10:19
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG {'data_format': 5, 'humidity': 50.52, 'temperature': 22.98, 'pressure': 1003.31, 'acceleration': 1049.3731462163496, 'acceleration_x': 24, 'acceleration_y': -48, 'acceleration_z': 1048, 'tx_power': 4, 'battery': 3080, 'movement_counter': 51, 'measurement_sequence_number': 17851, 'mac': 'd656d4dfd062'}
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG 2021-09-12 19:10:19
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG {'data_format': 5, 'humidity': 31.68, 'temperature': 35.28, 'pressure': 1002.76, 'acceleration': 1044.0689632394979, 'acceleration_x': -4, 'acceleration_y': -92, 'acceleration_z': 1040, 'tx_power': 4, 'battery': 3073, 'movement_counter': 76, 'measurement_sequence_number': 18049, 'mac': 'cf56c510cdb2'}
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG 2021-09-12 19:10:19
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG {'data_format': 5, 'humidity': 50.86, 'temperature': 23.68, 'pressure': 1003.18, 'acceleration': 1056.2045256483234, 'acceleration_x': -92, 'acceleration_y': -20, 'acceleration_z': 1052, 'tx_power': 4, 'battery': 3132, 'movement_counter': 29, 'measurement_sequence_number': 17591, 'mac': 'c71eda631b6e'}
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG 2021-09-12 19:10:19
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG {'data_format': 5, 'humidity': 45.98, 'temperature': 25.82, 'pressure': 1003.4, 'acceleration': 1034.5240451531322, 'acceleration_x': 812, 'acceleration_y': 640, 'acceleration_z': 36, 'tx_power': 4, 'battery': 3009, 'movement_counter': 226, 'measurement_sequence_number': 7291, 'mac': 'e0c9d7fe5650'}
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG 2021-09-12 19:10:19
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG {'data_format': 5, 'humidity': 51.3, 'temperature': 23.5, 'pressure': 1003.64, 'acceleration': 993.0478336918117, 'acceleration_x': -28, 'acceleration_y': 36, 'acceleration_z': 992, 'tx_power': 4, 'battery': 3034, 'movement_counter': 170, 'measurement_sequence_number': 65412, 'mac': 'fe6a53b27039'}
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG 2021-09-12 19:10:18
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG {'data_format': 5, 'humidity': 51.09, 'temperature': 24.41, 'pressure': 1003.4, 'acceleration': 1012.0316200593735, 'acceleration_x': -20, 'acceleration_y': -88, 'acceleration_z': 1008, 'tx_power': 4, 'battery': 3016, 'movement_counter': 0, 'measurement_sequence_number': 6121, 'mac': 'ec356b7e9b06'}
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG 2021-09-12 19:10:12
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG {'data_format': 5, 'humidity': 77.93, 'temperature': 17.7, 'pressure': 1003.94, 'acceleration': 1063.1124117420509, 'acceleration_x': 196, 'acceleration_y': -136, 'acceleration_z': 1036, 'tx_power': 4, 'battery': 3073, 'movement_counter': 100, 'measurement_sequence_number': 17748, 'mac': 'ee64e991f644'}
2021-09-12 19:10:20 n1proi9.home urllib3.connectionpool[58190] DEBUG Starting new HTTP connection (1): 192.168.20.69:80
2021-09-12 19:10:20 n1proi9.home urllib3.connectionpool[58190] DEBUG http://192.168.20.69:80 "GET /history HTTP/1.1" 200 1371
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG 2021-09-12 19:10:19
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG {'data_format': 5, 'humidity': 58.34, 'temperature': 25.14, 'pressure': 1003.37, 'acceleration': 1013.1534928134039, 'acceleration_x': 20, 'acceleration_y': -44, 'acceleration_z': 1012, 'tx_power': 4, 'battery': 3069, 'movement_counter': 42, 'measurement_sequence_number': 64952, 'mac': 'f8a7d0db988f'}
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG 2021-09-12 19:10:19
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] DEBUG {'data_format': 5, 'humidity': 77.72, 'temperature': 21.02, 'pressure': 1004.13, 'acceleration': 1050.0209521719078, 'acceleration_x': 48, 'acceleration_y': -44, 'acceleration_z': 1048, 'tx_power': 4, 'battery': 3027, 'movement_counter': 58, 'measurement_sequence_number': 64760, 'mac': 'c731b038db3f'}
2021-09-12 19:10:20 n1proi9.home ruuvigw_json_to_influx[58190] INFO Would try to output [{'measurement': 'sensor', 'tags': {'sensor_name': 'ylakerta_wc'}, 'time': '2021-09-12 19:10:19', 'fields': {'temperature': 24.18, 'humidity': 62.34, 'pressure': 1003.15, 'accelerationX': -780, 'accelerationY': -652, 'accelerationZ': 60, 'batteryVoltage': 3.038, 'txPower': 4, 'movementCounter': 70, 'measurementSequenceNumber': 165, 'rssi': -75}}, {'measurement': 'sensor', 'tags': {'sensor_name': 'makuuhuone'}, 'time': '2021-09-12 19:10:19', 'fields': {'temperature': 22.98, 'humidity': 50.52, 'pressure': 1003.31, 'accelerationX': 24, 'accelerationY': -48, 'accelerationZ': 1048, 'batteryVoltage': 3.08, 'txPower': 4, 'movementCounter': 51, 'measurementSequenceNumber': 17851, 'rssi': -55}}, {'measurement': 'sensor', 'tags': {'sensor_name': 'laitetila'}, 'time': '2021-09-12 19:10:19', 'fields': {'temperature': 35.28, 'humidity': 31.68, 'pressure': 1002.76, 'accelerationX': -4, 'accelerationY': -92, 'accelerationZ': 1040, 'batteryVoltage': 3.073, 'txPower': 4, 'movementCounter': 76, 'measurementSequenceNumber': 18049, 'rssi': -64}}, {'measurement': 'sensor', 'tags': {'sensor_name': 'aula'}, 'time': '2021-09-12 19:10:19', 'fields': {'temperature': 23.68, 'humidity': 50.86, 'pressure': 1003.18, 'accelerationX': -92, 'accelerationY': -20, 'accelerationZ': 1052, 'batteryVoltage': 3.132, 'txPower': 4, 'movementCounter': 29, 'measurementSequenceNumber': 17591, 'rssi': -47}}, {'measurement': 'sensor', 'tags': {'sensor_name': 'tyohuone'}, 'time': '2021-09-12 19:10:19', 'fields': {'temperature': 25.82, 'humidity': 45.98, 'pressure': 1003.4, 'accelerationX': 812, 'accelerationY': 640, 'accelerationZ': 36, 'batteryVoltage': 3.009, 'txPower': 4, 'movementCounter': 226, 'measurementSequenceNumber': 7291, 'rssi': -57}}, {'measurement': 'sensor', 'tags': {'sensor_name': 'keittio'}, 'time': '2021-09-12 19:10:19', 'fields': {'temperature': 23.5, 'humidity': 51.3, 'pressure': 1003.64, 'accelerationX': -28, 'accelerationY': 36, 'accelerationZ': 992, 'batteryVoltage': 3.034, 'txPower': 4, 'movementCounter': 170, 'measurementSequenceNumber': 65412, 'rssi': -68}}, {'measurement': 'sensor', 'tags': {'sensor_name': 'alakerta_wc'}, 'time': '2021-09-12 19:10:18', 'fields': {'temperature': 24.41, 'humidity': 51.09, 'pressure': 1003.4, 'accelerationX': -20, 'accelerationY': -88, 'accelerationZ': 1008, 'batteryVoltage': 3.016, 'txPower': 4, 'movementCounter': 0, 'measurementSequenceNumber': 6121, 'rssi': -78}}, {'measurement': 'sensor', 'tags': {'sensor_name': 'piha'}, 'time': '2021-09-12 19:10:12', 'fields': {'temperature': 17.7, 'humidity': 77.93, 'pressure': 1003.94, 'accelerationX': 196, 'accelerationY': -136, 'accelerationZ': 1036, 'batteryVoltage': 3.073, 'txPower': 4, 'movementCounter': 100, 'measurementSequenceNumber': 17748, 'rssi': -84}}, {'measurement': 'sensor', 'tags': {'sensor_name': 'talli'}, 'time': '2021-09-12 19:10:19', 'fields': {'temperature': 25.14, 'humidity': 58.34, 'pressure': 1003.37, 'accelerationX': 20, 'accelerationY': -44, 'accelerationZ': 1012, 'batteryVoltage': 3.069, 'txPower': 4, 'movementCounter': 42, 'measurementSequenceNumber': 64952, 'rssi': -48}}, {'measurement': 'sensor', 'tags': {'sensor_name': 'saunatupa'}, 'time': '2021-09-12 19:10:19', 'fields': {'temperature': 21.02, 'humidity': 77.72, 'pressure': 1004.13, 'accelerationX': 48, 'accelerationY': -44, 'accelerationZ': 1048, 'batteryVoltage': 3.027, 'txPower': 4, 'movementCounter': 58, 'measurementSequenceNumber': 64760, 'rssi': -70}}]
```