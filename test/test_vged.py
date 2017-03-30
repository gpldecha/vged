from vged.core import VGed
import matplotlib.pyplot as plt

def main():

    vged = VGed()

    filename = '/home/guillaume/PythonWorkSpace/geo/N051E000/MEDIAN/N051E000_MED_DSM.tif'
    vged.load(filename)

    ul=(51.55,0) #latitude,longitude
    lr=(51.45,0.2)

    array_part = vged.get_area(ul=ul,lr=lr)


    fig = plt.figure()
    plt.imshow(array_part,origin='lower')
    plt.show()




if __name__ == "__main__":
    main()
