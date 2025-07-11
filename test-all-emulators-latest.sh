#!/bin/bash

./emulator-testing.sh pubsub
if [ $? -ne 0 ]; then 

    echo "Pub/sub emulator failed to execute."
    exit 1  

fi

# TODO: datastore & firestore emulators are not supported on debian 12 because of Java 21 dependency

# ./emulator-testing.sh datastore
# if [ $? -ne 0 ]; then 

#    echo "Datastore emulator failed to execute."
#    exit 1  

# fi

# ./emulator-testing.sh firestore
# if [ $? -ne 0 ]; then

#    echo "Firestore emulator failed to execute."
#    exit 1

# fi

./emulator-testing.sh spanner
if [ $? -ne 0 ]; then 

    echo "Spanner emulator failed to execute."
    exit 1  

fi

./emulator-testing.sh bigtable
if [ $? -ne 0 ]; then

    echo "Bigtable emulator failed to execute."
    exit 1

fi

