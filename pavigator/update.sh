#!/bin/bash
rm -rf ./google_transit_dublinbus
rm -rf ./google_transit_dublinbus.zip

curl -LJO https://www.transportforireland.ie/transitData/Deprecated/google_transit_dublinbus.zip

if [ $? -ne 0 ]; then
    echo "Failed download"
    exit 1
fi

unzip -q ./google_transit_dublinbus.zip -d ./google_transit_dublinbus

if [ $? -ne 0 ]; then
    echo "Failed extraction"
    exit 1
fi
echo "Starting update process..."

ls ./google_transit_dublinbus

rm -f ./google_transit_dublinbus.zip

chmod 600 ./update.cnf

mysql --defaults-extra-file=./update.cnf -e 'SET GLOBAL local_infile=1;'

if [ $? -ne 0 ]; then
    echo "Failed to SET GLOBAL local_infile"
    exit 1
fi

mysql --defaults-extra-file=./update.cnf -h localhost pavigator < truncate.sql

if [ $? -ne 0 ]; then
    echo "Failed to drop tables in the database"
    exit 1
fi

mysql --defaults-extra-file=./update.cnf -h localhost pavigator < update.sql

if [ $? -eq 0 ]; then
    rm -rf ./google_transit_dublinbus
else
    echo "Failed database update"
    exit 1
fi

echo "Completed successfully"
