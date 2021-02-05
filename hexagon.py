import geopandas as gpd
from shapely.geometry import Polygon
from math import sin, cos, pi

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def get_coor(self):
        return (self.x, self.y)

class Hexagon():
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        
    def get_vertexs(self):
        x = self.center.x
        y = self.center.y
        r = self.radius
        return [Point(x + r * cos(pi*i/3), y + r * sin(pi*i/3)).get_coor() for i in range(6)]
    
class Grid():
    def __init__(self, start, radius, width, height):
        self.start = start
        self.radius = radius
        self.width = width
        self.height = height
        
    def grid_map(self):
        hexagon_l = []
        for h in range(self.height):
            for w in range(self.width):
                if w % 2 == 0:
                    x = self.start[0] + self.radius*(w*1.5)
                    y = self.start[1] - h*2*self.radius*sin(pi*1/3)

                else:
                    x = self.start[0] + self.radius * cos(pi*5/3) + self.radius*((w-1)*1.5+1)
                    y = self.start[1] + self.radius * sin(pi*5/3) - h*2*self.radius*sin(pi*1/3)

                center = Point(x, y)
                hexagon_l.append(Hexagon(center, self.radius))
        return hexagon_l

    def to_gdf(self):
        Polygon_l = [Polygon(hexgon.get_vertexs()) for hexgon in self.grid_map()]
        geometry = gpd.GeoSeries(Polygon_l)
        data = {'id': [i for i in range(len(Polygon_l))]}
        crs = {'init' :'epsg:3826'}
        return gpd.GeoDataFrame(data, crs=crs, geometry=geometry)