#!/bin/bash
until python3 ./red.py; do
    echo "'red.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done