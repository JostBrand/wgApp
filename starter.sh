#!/bin/bash

myscript(){
    python3 main.py
}

until myscript; do
    echo "'myscript' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
