#!/bin/bash

set -e

for name in GATEWAY_ENDPOINTS INFLUX_DB_HOST INFLUX_DB_DATABASE INFLUX_DB_USER INFLUX_DB_PASSWORD; do
    if [[ -z "${!name}" ]]; then
        echo "Variable $name not set!"
        exit 1
    fi
done

python ruuvigw_json_to_influx.py --influx_db_host $INFLUX_DB_HOST --influx_db_database $INFLUX_DB_DATABASE --influx_db_user $INFLUX_DB_USER --influx_db_password $INFLUX_DB_PASSWORD --gateway_endpoints=$GATEWAY_ENDPOINTS
