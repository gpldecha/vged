import gdal
import osr


class VGED(object):

    def __init__(self):
        self.ds = None

    def load(self,filename):
        """
            Args:
                filename : str  , path to a .tif dataset
        """
        self.ds      = gdal.Open(filename)
        self.width   = ds.RasterXSize
        self.height  = ds.RasterYSize
        self.gt      = ds.GetGeoTransform()  # maps i,j to x,y

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

    def get_area(self,tl,bl):
        """ Gets an area of the world.
            Args:
                tl : tuple  , top right GPS coordinates of the area
                    - TR = (latitude,longitude)
                bl : tuple  , bottom left GPS coordinates of the area.
                    - BL = (latitude,longitude)
            Returns:
                np.ndarray  : raster values of the square.
        """
        pt_tl = ct.TransformPoint(*tl)  # x,y
        pt_bl = ct.TransformPoint(*bl)  # x,y
        print pt_tl
        print pt_bl
