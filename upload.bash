#!/bin/bash

# Remove existing data file
rm -rf ./datagen/data/*

# Generate new junk file
python3 ./datagen/datagen.py

# Run connector script
python3 ./connection_test/connector.py $MARIADB_LOCAL_USERNAME $MARIADB_LOCAL_PASSWORD $MARIADB_DEFAULT_HOST $MARIADB_DEFAULT_PORT