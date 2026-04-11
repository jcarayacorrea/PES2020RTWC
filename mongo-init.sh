#!/bin/bash
set -e

echo "Initialising MongoDB database: $MONGO_INITDB_DATABASE"

# Run all files in /init-data
# Explicitly list them in order if needed, but the user asked to run EVERY file.
# We'll run Teams, Places, Fixtures first, then any other files, and initDBScript last.

declare -a files=(
    "Teams.json"
    "Places.json"
    "Fixtures.json"
)

# Run known data files first
for f in "${files[@]}"; do
    if [ -f "/init-data/$f" ]; then
        echo "Running script: $f"
        mongosh --username "$MONGO_INITDB_ROOT_USERNAME" \
                --password "$MONGO_INITDB_ROOT_PASSWORD" \
                --authenticationDatabase admin \
                "$MONGO_INITDB_DATABASE" \
                "/init-data/$f"
    fi
done

# Run any other files except the ones already run and initDBScript
for f in /init-data/*; do
    filename=$(basename "$f")
    if [[ ! " ${files[@]} " =~ " ${filename} " ]] && [[ "$filename" != "initDBScript" ]] && [[ -f "$f" ]]; then
        echo "Running script: $filename"
        mongosh --username "$MONGO_INITDB_ROOT_USERNAME" \
                --password "$MONGO_INITDB_ROOT_PASSWORD" \
                --authenticationDatabase admin \
                "$MONGO_INITDB_DATABASE" \
                "$f"
    fi
done

# Run initDBScript last
if [ -f "/init-data/initDBScript" ]; then
    echo "Running script: initDBScript"
    mongosh --username "$MONGO_INITDB_ROOT_USERNAME" \
            --password "$MONGO_INITDB_ROOT_PASSWORD" \
            --authenticationDatabase admin \
            "$MONGO_INITDB_DATABASE" \
            "/init-data/initDBScript"
fi

echo "MongoDB initialisation complete!"
