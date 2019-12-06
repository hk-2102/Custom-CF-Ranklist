#! /bin/bash

while true; do
    python script.py
    git add .
    git commit -m "Updated Database"
    git push
    sleep 3600
done
