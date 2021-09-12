from influxdb import InfluxDBClient
import json
import os
import sys
import argparse
import logging
import coloredlogs
from ruuvitag_sensor.decoder import get_decoder
from ruuvitag_sensor.data_formats import DataFormats
import requests
import datetime

log = logging.getLogger("ruuvigw_json_to_influx")
LOGLEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=LOGLEVEL,
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)])
coloredlogs.install(isatty=True, level=LOGLEVEL)


def _parse_args():
    # parse command line arguments
    parser = argparse.ArgumentParser(
        description='Bridge between Ruuvi GW sensor output json and InfluxDB')
    parser.add_argument(
        '--gateway_endpoints', help='Comma separated list of endpoints to scrape', type=str)
    parser.add_argument(
        '--tag_mappings_file', help='File that includes mac to name pairings', default="mappings.json", type=str)
    parser.add_argument('--influx_db_host', help='influx db host address',
                        default='127.0.0.1', type=str)
    parser.add_argument('--influx_db_port', help='influx db host port',
                        default=8086, type=int)
    parser.add_argument('--influx_db_database', help='influx db database name (eg default)',
                        default="ruuvi", type=str)
    parser.add_argument('--influx_db_user', help='influx db user',
                        default="ruuvi", type=str)
    parser.add_argument('--influx_db_password', help='influx db password',
                        default="ruuvi", type=str)
    parser.add_argument('--dry-run', help='Output to console rather than sending to influx',
                        default=False, type=bool)
    args = parser.parse_args()
    return args


def _get_data(endpoints: list, mappings: dict) -> dict:
    measurements = []
    processed_macs = []

    for endpoint in endpoints:
        try:
            response = requests.get(f"http://{endpoint}/history")
            for tag in response.json()['data']['tags'].items():
                mac = tag[0]
                if mac in processed_macs:
                    continue

                processed_macs.append(mac)
                if mac in mappings:
                    tag_name = mappings[mac]
                else:
                    tag_name = mac.replace(":", "_")

                time = datetime.datetime.utcfromtimestamp(int(tag[1]['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
                log.debug(time)
                tags = {"sensor_name": tag_name}

                # Cut off until FF990405 and keep 05
                sensor_data = get_decoder(5).decode_data(tag[1]['data'][14:])
                log.debug(sensor_data)
                fields = {}
                fields['temperature'] = sensor_data['temperature'] if ('temperature' in sensor_data) else None
                fields['humidity'] = sensor_data['humidity'] if ('humidity' in sensor_data) else None
                fields['pressure'] = sensor_data['pressure'] if ('pressure' in sensor_data) else None
                fields['accelerationX'] = sensor_data['acceleration_x'] if ('acceleration_x' in sensor_data) else None
                fields['accelerationY'] = sensor_data['acceleration_y'] if ('acceleration_y' in sensor_data) else None
                fields['accelerationZ'] = sensor_data['acceleration_z'] if ('acceleration_z' in sensor_data) else None
                fields['batteryVoltage'] = sensor_data['battery']/1000.0 if ('battery' in sensor_data) else None
                fields['txPower'] = sensor_data['tx_power'] if ('tx_power' in sensor_data) else None
                fields['movementCounter'] = sensor_data['movement_counter'] if ('movement_counter' in sensor_data) else None
                fields['measurementSequenceNumber'] = sensor_data['measurement_sequence_number'] if ('measurement_sequence_number' in sensor_data) else None
                fields['rssi'] = tag[1]['rssi'] if ('rssi' in tag[1]) else None

                measurement = {"measurement": 'sensor',
                               "tags": tags,
                               "time": time,
                               "fields": fields}
                measurements.append(measurement)
        # TODO: proper handling of issues
        except requests.exceptions.HTTPError as e:
            log.error(e)
        except requests.exceptions.ConnectionError as e:
            log.error(e)

    _ = json.JSONEncoder().encode(measurements)
    return measurements


def _read_mappings(mappings_file: str) -> dict:
    mappings = {}
    with open(mappings_file, 'r') as input_json:
        mappings = json.load(input_json)
    return mappings


def main():
    log.info("Starting ruuvi json to Influx script")
    args = _parse_args()

    mappings = {}
    if args.tag_mappings_file:
        mappings = _read_mappings(args.tag_mappings_file)

    endpoints = args.gateway_endpoints.split(",")
    data = _get_data(endpoints, mappings)

    influx_client = InfluxDBClient(host=args.influx_db_host, port=args.influx_db_port, database=args.influx_db_database,
                                   username=args.influx_db_user, password=args.influx_db_password, timeout=3)
    if args.dry_run:
        log.info(f"Would try to output {data}")
    else:
        influx_client.write_points(data)


if __name__ == '__main__':
    main()
