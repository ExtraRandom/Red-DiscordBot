#!/bin/bash
until ./red.py; do
    echo "'red.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done