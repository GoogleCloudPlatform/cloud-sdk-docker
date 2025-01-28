
#!/bin/bash

./emulator-testing.sh pubsub
if [ $? -ne 0 ]; then 

    echo "Pub/sub emulator failed to execute."
    exit 1  

fi

./emulator-testing.sh datastore
if [ $? -ne 0 ]; then 

    echo "Datastore emulator failed to execute."
    exit 1  

fi

./emulator-testing.sh bigtable
if [ $? -ne 0 ]; then

    echo "Bigtable emulator failed to execute."
    exit 1

fi

