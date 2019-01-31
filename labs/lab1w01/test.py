#!/usr/bin/env python3

import os
import lab
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)

class TestImage(unittest.TestCase):
    def test_load(self):
        result = lab.Image.load('test_images/centered_pixel.png')
        expected = lab.Image(11, 11,
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(result, expected)


class TestInvert(unittest.TestCase):
    def test_invert_1(self):
        im = lab.Image.load('test_images/centered_pixel.png')
        result = im.inverted()
        expected = lab.Image(11, 11,
                             [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255])
        self.assertEqual(result,  expected)

    def test_invert_2(self):
        im = lab.Image(1, 4, [10, 91, 147, 203])
        result = im.inverted()
        expected = lab.Image(1, 4, [245, 164, 108, 52])
        self.assertEqual(result, expected)

    def test_invert_images(self):
        for fname in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=fname):
                inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_invert.png' % fname)
                result = lab.Image.load(inpfile).inverted()
                expected = lab.Image.load(expfile)
                self.assertEqual(result,  expected)


class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.im = lab.Image(3, 3, [-4, 7, 2.2, 267, -8, 12.4, 9, 32, 629.7])

    def test_01(self):
        # Test Up and Left of bound get_pixel_alt()
        result = self.im.get_pixel_alt(-1, -2)
        expected = -4
        self.assertEqual(result, expected)

    def test_02(self):
        # Test Up of bound get_pixel_alt()
        result = self.im.get_pixel_alt(1, -2)
        expected = 7
        self.assertEqual(result, expected)

    def test_03(self):
        # Test Up and Right of bound get_pixel_alt()
        result = self.im.get_pixel_alt(4, -1)
        expected = 2.2
        self.assertEqual(result, expected)

    def test_04(self):
        # Test Left of bound get_pixel_alt()
        result = self.im.get_pixel_alt(-2, 1)
        expected = 267

        self.assertEqual(result, expected)

    def test_05(self):
        # Test in bound get_pixel_alt()
        result = self.im.get_pixel_alt(1, 1)
        expected = -8
        self.assertEqual(result, expected)

    def test_06(self):
        # Test Right of bound get_pixel_alt()
        result = self.im.get_pixel_alt(5, 1)
        expected = 12.4
        self.assertEqual(result, expected)

    def test_07(self):
        # Test Down and Left of bound get_pixel_alt()
        result = self.im.get_pixel_alt(-1, 4)
        expected = 9
        self.assertEqual(result, expected)

    def test_08(self):
        # Test Down of bound get_pixel_alt()
        result = self.im.get_pixel_alt(1, 3)
        expected = 32
        self.assertEqual(result, expected)

    def test_09(self):
        # Test Down and Righn of bound get_pixel_alt()
        result = self.im.get_pixel_alt(3, 3)
        expected = 629.7
        self.assertEqual(result, expected)
    
    def test_10(self):
        # Test clip()
        result = self.im.clip()
        expected = lab.Image(3, 3, [0, 7, 2, 255, 0, 12, 9, 32, 255])
        self.assertEqual(result, expected)

    def test_11(self):
        # Test correlate() with identity kernel
        kernel = ((0, 0, 0),
                  (0, 1, 0),
                  (0, 0, 0))
        im = lab.Image.load('test_images/centered_pixel.png')
        result = im.correlate(kernel)
        expected = lab.Image.load('test_results/centered_pixel_identity.png')
        self.assertEqual(result, expected)

    def test_12(self):
        # Test correlate() with translation kernel
        kernel = ((0, 0, 0, 0, 0),
                  (0, 0, 0, 0, 0),
                  (1, 0, 0, 0, 0),
                  (0, 0, 0, 0, 0),
                  (0, 0, 0, 0, 0))
        im = lab.Image.load('test_images/centered_pixel.png')
        result = im.correlate(kernel)
        expected = lab.Image.load('test_results/centered_pixel_translation.png')
        self.assertEqual(result, expected)

    def test_13(self):
        # Test correlate() with average kernel
        kernel = ((0,   0.2, 0),
                  (0.2, 0.2, 0.2),
                  (0,   0.2, 0))
        im = lab.Image.load('test_images/centered_pixel.png')
        result = im.correlate(kernel)
        expected = lab.Image.load('test_results/centered_pixel_average.png')
        self.assertEqual(result, expected)


class TestFilters(unittest.TestCase):
    def test_blur(self):
        for kernsize in (1, 3, 7):
            for fname in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=kernsize, f=fname):
                    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_blur_%02d.png' % (fname, kernsize))
                    result = lab.Image.load(inpfile).blurred(kernsize)
                    expected = lab.Image.load(expfile)
                    self.assertEqual(result,  expected)

    def test_sharpen(self):
        for kernsize in (1, 3, 9):
            for fname in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=kernsize, f=fname):
                    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_sharp_%02d.png' % (fname, kernsize))
                    result = lab.Image.load(inpfile).sharpened(kernsize)
                    expected = lab.Image.load(expfile)
                    self.assertEqual(result,  expected)

    def test_edges(self):
        for fname in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=fname):
                inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_edges.png' % fname)
                result = lab.Image.load(inpfile).edges()
                expected = lab.Image.load(expfile)
                self.assertEqual(result,  expected)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
