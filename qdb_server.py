import tornado.ioloop
import tornado.web

import time
import logging

import threading
from Queue import Queue
from qdb import QDB, mercatorPoint, mercator

logging.basicConfig()
logger = logging.getLogger("qdb_server")
logger.setLevel(logging.DEBUG)

def get_slice():
    return int(time.time()/TIME_SLICE)

TIME_SLICE = 10 # seconds

current_slice = None
current_time_slice = get_slice()

qdb = QDB()
def qdb_process(q):
    global qdb, current_time_slice, current_slice
    logger.info("starting thread")

    while True:
        p = q.get()
        point = p[:2]
        timestamp = int(p[2])
        time_slice = get_slice()
        if current_time_slice != time_slice:
            logger.info("slice change")
            current_slice = qdb;
            current_time_slice = time_slice
            qdb = QDB()
        logger.debug("adding point, timestamp %d", timestamp - current_time_slice*TIME_SLICE)
        # TODO: discard points with timestamp > current_time_slice*TIME_SLICE
        qdb.add_lonlat(point, timestamp - current_time_slice*TIME_SLICE)
        q.task_done()


q = Queue()
threading.Thread(target=qdb_process,args=(q,)).start()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        lat = float(self.get_argument('lat'))
        lon = float(self.get_argument('lon'))
        q.put((lon, lat, time.time()))
        self.write("%d" % q.qsize())

class TilesHandler(tornado.web.RequestHandler):
    def get(self, z, x, y):
        z = int(z)
        x = int(x)
        y = int(y)
        logger.info("tile %d/%d/%d" % (z, x, y))
        if current_slice:
            self.write({
                "time_slice": current_time_slice,
                "tile": current_slice.store.to_torque((x, y, z))
            })
            return
        self.set_status(400, "slice not ready")



application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/t/([0-9]+)/([0-9]+)/([0-9]+).json", TilesHandler)
])

if __name__ == "__main__":
    import sys
    if (len(sys.argv) >= 2):
        TIME_SLICE = int(sys.argv[1])

    application.listen(8888)
    logger.info("server listening on 8888")
    logger.info(" - TIME_SLICE: %d seconds" % TIME_SLICE)
    tornado.ioloop.IOLoop.instance().start()
