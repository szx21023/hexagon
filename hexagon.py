import geopandas
from geopandas import GeoSeries
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

# 起始座標(x軸, y軸)(公尺)
# 半徑
# 水平網格數
# 垂直網格數
    
class Grid():
    def __init__(self, start, radius, width, height):
        self.start = start
        self.radius = radius
        self.width = width
        self.height = height
        
    def grid_map(self):
        start = self.start
        radius = self.radius
        width = self.width
        height = self.height

        hexagon_l = []
        for h in range(height):
            for w in range(width):
                if w == 0:
                    x = start[0]
                    y = start[1] - h*2*radius*sin(pi*1/3)

                elif w % 2 == 0:
                    x = start[0] + radius*(w*1.5)
                    y = start[1] - h*2*radius*sin(pi*1/3)

                else:
                    x = start[0] + radius * cos(pi*5/3) + radius*((w-1)*1.5+1)
                    y = start[1] + radius * sin(pi*5/3) - h*2*radius*sin(pi*1/3)

                center = Point(x, y)
                hexagon_l.append(Hexagon(center, radius))
        return hexagon_l

    def to_geopandas(self, file_name):
        Polygon_l = [Polygon(hexgon.get_vertexs()) for hexgon in self.grid_map()]
        geometry = GeoSeries(Polygon_l)
        id_l = [i for i in range(len(Polygon_l))]

        gdf = geopandas.GeoDataFrame(id_l, geometry=geometry).rename(columns={0: 'id'})
        gdf.crs = {'init' :'epsg:3826'}
        gdf = gdf.to_crs({'init': 'epsg:4326'})
        gdf.to_csv(file_name, index=False)

    def to_gdf(self):
        Polygon_l = [Polygon(hexgon.get_vertexs()) for hexgon in self.grid_map()]
        geometry = GeoSeries(Polygon_l)
        id_l = [i for i in range(len(Polygon_l))]

        gdf = geopandas.GeoDataFrame(id_l, geometry=geometry).rename(columns={0: 'id'})
        gdf.crs = {'init' :'epsg:3826'}
        gdf = gdf.to_crs({'init': 'epsg:4326'})
        return gdf
