
#!/bin/bash

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

"$SCRIPT_DIR/emulator-testing.sh" pubsub
if [ $? -ne 0 ]; then 

    echo "Pub/sub emulator failed to execute."
    exit 1  

fi

"$SCRIPT_DIR/emulator-testing.sh" datastore
if [ $? -ne 0 ]; then 

    echo "Datastore emulator failed to execute."
    exit 1  

fi

"$SCRIPT_DIR/emulator-testing.sh" bigtable
if [ $? -ne 0 ]; then

    echo "Bigtable emulator failed to execute."
    exit 1

fi
