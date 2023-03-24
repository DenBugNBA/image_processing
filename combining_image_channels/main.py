from skimage.io import imread
from align import align

if __name__ == "__main__":
    img = imread("00.png")
    coord = (508, 237)

    print(align(img, coord))
