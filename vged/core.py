import gdal
import osr
import numpy as np


class VGed(object):

    def __init__(self):
        self.ds = None

    def load(self,filename):
        """
            Args:
                filename : str  , path to a .tif dataset
        """
        self.ds      = gdal.Open(filename)
        self.width   = self.ds.RasterXSize
        self.height  = self.ds.RasterYSize
        self.gt      = self.ds.GetGeoTransform()  # maps i,j to x,y
        self.band    = self.ds.GetRasterBand(1)

        self._get_corners()

        print 'width:  ', self.width
        print 'height: ', self.height
        print ' top left: (0,0) => (', self.gt[0] ,',', self.gt[3] ,')'
        print 'pixel w: ', self.gt[1]
        print 'pixel h: ', self.gt[5]
        print '2: ', self.gt[2]
        print '4: ', self.gt[4]

        try:
            self.inv_gt_success, self.inverse_gt = gdal.InvGeoTransform(self.gt) # maps x,y to i,j
        except:
            self.inverse_gt = gdal.InvGeoTransform(self.gt) # maps x,y to i,j

        self.sr_ds = osr.SpatialReference()  # spatial reference of the dataset
        self.sr_ds.ImportFromWkt(self.ds.GetProjection())

        self.sr_wgs84 = osr.SpatialReference()  # spatial reference of WGS84
        self.sr_wgs84.SetWellKnownGeogCS('WGS84')

        self.ct = osr.CoordinateTransformation(self.sr_wgs84, self.sr_ds)

        # compute corners

    def get_area(self,ul,lr):
        """ Gets an area of the world.
            Args:
                ul : tuple  , upper left GPS coordinates of the area
                    - TR = (latitude,longitude)
                lr : tuple  , lower right GPS coordinates of the area.
                    - BL = (latitude,longitude)
            Returns:
                np.ndarray  : raster values of the square.
        """
        point1 = self._ll2pixel(Lat=ul[0],Long=ul[1])  # x,y
        point2 = self._ll2pixel(Lat=lr[0],Long=lr[1])  # x,y

        dx = np.abs(point1[0] - point2[0])
        dy = np.abs(point1[1] - point2[1])
        print point1
        print point2
        print dx
        print dy
        self._area_array = self.band.ReadAsArray(point1[0],point1[1],dx,dy)
        return self._area_array


    def _get_corners(self):
        minx = self.gt[0]
        miny = self.gt[3] + self.width*self.gt[4] + self.height*self.gt[5]  # from http://gdal.org/gdal_datamodel.html
        maxx = self.gt[0] + self.width*self.gt[1] + self.height*self.gt[2]  # from http://gdal.org/gdal_datamodel.html
        maxy = self.gt[3]
        self.LL = (minx,miny)
        self.UL = (minx,maxy)
        self.UR = (maxx,maxy)
        self.LR = (maxx,miny)

    def _rescale(self,x,min_x,max_x,a,b):
        """ rescales x to be in range [a,b] when in range  [x_min,x_max]"""
        return (b-a) * (x - min_x) / (max_x - min_x) + a

    def _ll2pixel(self,Lat,Long):
        """ Converts latitude and longitude to pixel location
            Ref: [Affine GeoTransform](http://www.gdal.org/gdal_datamodel.html)
        """
        px = self._rescale(Long,self.UL[0],self.UR[0],0,self.width) # east-weast
        py = self._rescale(Lat, self.UL[1],self.LL[1],0,self.height)  # north-south
        return np.array([px,py],dtype=int)
