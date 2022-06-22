#!/bin/sh

### DEPLOYING THE LOCAL CONTAINERS
echo "DEPLOYING THE LOCAL CONTAINERS..."
echo "Deploying local firestore-emulator container..."
docker-compose up -d firestore-emulator
echo -e "\n"

### VERIFYING THE DEPLOYMENT OF THE LOCAL CONTAINERS
echo "VERIFYING THE DEPLOYMENT OF THE LOCAL CONTAINERS..."
while ! curl http://localhost:8200
do
  echo "local firestore-emulator container is not running..."
  sleep 2
done
echo "local firestore-emulator container is running..."
echo -e "\n"

### EXPORTING VARIABLES
echo "EXPORTING VARIABLES..."
echo "Exporting variables for local firestore container..."
export FIRESTORE_EMULATOR_HOST=localhost:8200
export FIRESTORE_PROJECT_ID=emulator
echo -e "\n"

### RUNNING TESTS
echo "RUNNING TESTS..."
python python-scripts/load_dummy_users_data.py
sleep 5
python python-scripts/delete_users_data.py
echo -e "\n"

### TEARING DOWN
echo "TEARING DOWN..."
unset FIRESTORE_EMULATOR_HOST
unset FIRESTORE_PROJECT_ID
docker-compose down
