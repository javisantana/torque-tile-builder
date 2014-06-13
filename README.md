
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

## license 

BSD
