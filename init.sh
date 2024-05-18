#!/bin/bash

torpy_socks -p 1050 --hops 3 &

python app.py &

wait -n

exit $?