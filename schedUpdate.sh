#! /bin/bash

while true; do
    git pull
    python script.py
    git add .
    git commit -m "Updated Database"
    git push
    echo "going to sleep"
    sleep 3600
done
