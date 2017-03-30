from vged.core import VGed
import matplotlib.pyplot as plt
#http://geoexamples.blogspot.co.uk/2014/02/3d-terrain-visualization-with-python.html

def plot1(array_part):
    fig = plt.figure()
    plt.imshow(array_part,origin='lower')
    plt.show()



def plot2(array_part):
    from mayavi import mlab
    mlab.figure(size=(640, 800), bgcolor=(0.16, 0.28, 0.46))
    mlab.surf(array_part, warp_scale=0.2)
    mlab.show()

def main():

    vged = VGed()

    filename = '/home/guillaume/PythonWorkSpace/geo/N051E000/MEDIAN/N051E000_MED_DSM.tif'
    vged.load(filename)

    ul=(51.55,0) #latitude,longitude
    lr=(51.45,0.2)

    array_part = vged.get_area(ul=ul,lr=lr)

    #plot1(array_part)
    plot2(array_part)



if __name__ == "__main__":
    main()
