
from math import pi, fmod, log, tan, sin
from collections import defaultdict

EARTH_RADIUS = 6378137 
# from TileStache
def mercator((x, y)):
    ''' Project an (x, y) tuple to spherical mercator.  '''
    y = min(max(y, -89.189), 89.189)
    x, y = x/360.0, pi * y/180.0
    siny = sin(y)
    siny = min(max(siny, -0.9999), 0.9999)
    y = 0.5*log(tan(0.25 * pi + 0.5 * y))/pi
    return x, y


def mercatorPoint((x, y), tileSize):
    t2 = tileSize >> 1
    return (
        t2 + x*tileSize,
        t2 - y*tileSize
    )

class Store(object):
    def __init__(self, tile_size, temporal_res):
        self.tile_size = tile_size
        self.tiles = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    def store_point(self, coord, (x, y), timestamp):
        """ stores a point for tile coord """
        tile_key = self._key(coord)
        idx = x * self.tile_size + y
        self.tiles[tile_key][idx][timestamp] += 1

    def _key(self, coord):
        return "%d-%d-%d" % coord

    def to_torque(self, coord):
        return [{
            'x__uint8':  k//self.tile_size,
            'y__uint8': k%self.tile_size,
            'dates__uint16': x.keys(),
            'vals__uint16': x.values(),
         } for k, x in self.tiles[self._key(coord)].iteritems()
        ]


class QDB(object):
    MAX_ZOOM = 16

    def __init__(self, coord=(0, 0, 0), store=None):
        self.points = []
        self.tile_size = 256;
        # m/px
        self.resolution = [6378137 * 2 * pi / (self.tile_size * (1 << zoom)) for zoom in xrange(QDB.MAX_ZOOM + 1)]
        self.coord = coord
        self.children = {};
        if not store:
            store = Store(self.tile_size, 0)
        self.store = store

    def tile_pos(self, x, y, z):
        """ tile position in pixels given z, x, y quadtree coordinates """
        r = self.tile_size
        return int(x*r), int(y*r)

    def quadrant(self, (x, y)):
        th = self.tile_size >> 1;
        if x <= th:
            if y <= th:
                return 0
            return 2
        if y <= th:
            return 1
        return 3

    def _childCoord(self, quadrant):
        offset = [
            [0, 0],
            [1, 0],
            [0, 1],
            [1, 1]
        ]
        return (
            self.coord[0]*2 + offset[quadrant][0],
            self.coord[1]*2 + offset[quadrant][1],
            self.coord[2] + 1
        )

    def add_lonlat(self, lonlat, timestamp):
        self.add_point(mercatorPoint(mercator(lonlat), self.tile_size), timestamp)

    def add_point(self, (x, y), timestamp):
        zoom = self.coord[2]
        tile_pos_px = self.tile_pos(*self.coord)
        res = 1 << zoom
        px, py = int( x * res - tile_pos_px[0]), int( y*res - tile_pos_px[1])
        #print "zoom", zoom, "tile", tile_pos_px,  "pixel", px,py
        self.store.store_point(self.coord, (px, py), timestamp)
        if zoom < self.MAX_ZOOM:
            q = self.quadrant((px, py))
            if q not in self.children:
                self.children[q] = QDB(self._childCoord(q), self.store)
            self.children[q].add_point((x, y), timestamp)


if __name__ == '__main__':
    from random import uniform
    def test():
        q = QDB()
        for x in xrange(1000):
            point = (uniform(-179.9, 179.9), uniform(-85, 85))
            q.add_point(mercatorPoint(mercator(point), 256), 1)
        print q.store.to_torque((0, 0, 0))
    import timeit
    print timeit.timeit(test, number=1)

    #print (
        #mercatorPoint(
            #mercator((-3, 40.0)), 
            #255
        #))
