
# torque tile realtime builder

this app build and serve torque tiles in realtime.

It builds a tiles for time slices so every ``TIME_SLICE`` seconds generates a set of tiles, when a
new time slice is generated the old tiles are discarded.

This app does not use any permanent storage


## quick start

install tornado and run the server

    pip install tornado
    python qdb_server.py 15


start adding points

    curl http://localhost:8888?lat=44.2&lon=-4.3

fetch tiles

    curl http://localhost:8888/t/0/0/0.json

## example run

client log: 

    $curl http://localhost:8888/\?lat\=0\&lon\=0 
    $curl http://localhost:8888/\?lat\=0\&lon\=0
    $curl http://localhost:8888/\?lat\=0\&lon\=0
    $curl http://localhost:8888/\?lat\=0\&lon\=0
    $curl http://localhost:8888/\?lat\=0\&lon\=0
    $curl http://localhost:8888/\?lat\=0\&lon\=0
    $curl http://localhost:8888/\?lat\=0\&lon\=0
    $curl http://localhost:8888/\?lat\=0\&lon\=0
    $curl http://localhost:8888/\?lat\=0\&lon\=0
    $curl http://localhost:8888/t/0/0/0.json
    {"tile": [{"x__uint8": 128, "vals__uint16": [1, 1, 2, 1, 1, 2], "y__uint8": 128, "dates__uint16": [4, 5, 6, 7, 8, 9]}], "time_slice": 140267483}

server log:

    $ python qdb_server.py 10
    INFO:qdb_server:starting thread
    INFO:qdb_server:server listening on 8888
    INFO:qdb_server: - TIME_SLICE: 10 seconds
    INFO:qdb_server:slice change
    DEBUG:qdb_server:adding point, timestamp 4
    DEBUG:qdb_server:adding point, timestamp 5
    DEBUG:qdb_server:adding point, timestamp 6
    DEBUG:qdb_server:adding point, timestamp 6
    DEBUG:qdb_server:adding point, timestamp 7
    DEBUG:qdb_server:adding point, timestamp 8
    DEBUG:qdb_server:adding point, timestamp 9
    DEBUG:qdb_server:adding point, timestamp 9
    INFO:qdb_server:slice change
    DEBUG:qdb_server:adding point, timestamp 1
    INFO:qdb_server:tile 0/0/0

## license 

BSD
