import os

import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme.misc import *
from supreme.config import ftype,itype
restore_path()

class test_ImageCollection(NumpyTestCase):
    data_path = os.path.dirname(__file__)
    data_glob = os.path.join(data_path,'*.png')
    images = [imread(os.path.join(data_path,'data%d.png' % i))
              for i in range(3)]

    def setUp(self):
        self.c = ImageCollection(self.data_glob)

    def check_len(self):
        assert_equal(len(self.c),3)

    def check_images(self):
        assert_array_equal(self.c[0],self.images[0])
        assert_equal(self.c[0].filename,'data0.png')

        assert_array_equal(self.c[2],self.images[2])
        assert_array_equal(self.c[1],self.images[1])

    def check_iterate(self):
        for i,img in enumerate(self.c):
            assert_array_equal(img,self.c[i])
            assert_array_equal(img,self.images[i])

    def check_tags(self):
        ic = ImageCollection(os.path.join(self.data_path,'exif_tagged.jpg'))
        img = ic[0]
        assert_equal(str(img.EXIF['EXIF ExposureTime']),'1/60')
        assert_equal(img.filename,'exif_tagged.jpg')
        assert_almost_equal(img.exposure,1/60.)

        img.info['x'] = 3
        img2 = (img + N.array([1,2,3]))
        assert_equal(img2.info['x'],3)

    def check_grey(self):
        ic = ImageCollection(self.data_glob,grey=True)
        for img in ic:
            assert_equal(img.ndim,2)

class test_ImageCollection_do_not_conserve_memory(test_ImageCollection):
    def setUp(self):
        self.c = ImageCollection(self.data_glob,conserve_memory=False)

if __name__ == "__main__":
    NumpyTest().run()
