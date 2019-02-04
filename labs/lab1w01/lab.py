#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as PILImage

## NO ADDITIONAL IMPORTS ALLOWED!

def get_box_blur(n, total=1):
    """Create box blur with size n x n"""
    value = total / n ** 2
    return [[value for _ in range(n)] for _ in range(n)]


class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels

    def _get_index(self, x, y):
        """Get pixel index for coordinates (x, y)"""
        return x + y * self.width

    def get_pixel(self, x, y):
        """Get value of the pixel with coordinates (x, y)"""
        # Check that coordinates are in bounds
        assert 0 <= x < self.width and 0 <= y < self.height
        return self.pixels[self._get_index(x, y)]

    def get_pixel_alt(self, x, y):
        """
        Get value of the pixel whih coordinates (x, y)
        
        If coordinates are out of bounds, set coordinate to min or max bound
        """
        x = min(self.width-1, max(0, x))
        y = min(self.height-1, max(0, y))
        return self.get_pixel(x, y)

    def set_pixel(self, x, y, c):
        """Set pixel value with coordinates (x, y) to c"""
        self.pixels[self._get_index(x, y)] = c

    def apply_per_pixel(self, func):
        """Create a new image by apply func to each pixel"""
        result = Image.new(self.width, self.height)
        for x in range(result.width):
            for y in range(result.height):
                color = self.get_pixel(x, y)
                newcolor = func(color)
                result.set_pixel(x, y, newcolor)
        return result

    def inverted(self):
        """
        Create a new image with inverted pixels
        """
        return self.apply_per_pixel(lambda c: 255-c)

    def clip(self):
        """Create image with pixels values are integer and in [0..255]"""
        result = Image.new(self.width, self.height)
        result.pixels = [min(255, max(0, round(c))) for c in self.pixels]
        return result

    def correlate(self, kernel):
        """
        Create image, that is result of correlation wih kernel
        
        Kernel size is n x n where n is odd
        """
        kernel_size = len(kernel)
        kernel_shift = kernel_size // 2
        result = Image.new(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                shift_x = x - kernel_shift
                shift_y = y - kernel_shift
                color = 0
                for dx in range(kernel_size):
                    for dy in range(kernel_size):
                        color += self.get_pixel_alt(shift_x+dx, shift_y+dy) * \
                                 kernel[dy][dx]
                result.set_pixel(x, y, color)
        return result

    def blurred(self, n):
        """Create blurred image, where kernel has size n x n"""
        kernel = get_box_blur(n)
        result = self.correlate(kernel).clip()
        return result

    def sharpened(self, n):
        """Create sharpen image, where kernel has size n x n"""
        # create sharp kernel
        kernel = get_box_blur(n, total=-1)
        center = n // 2
        kernel[center][center] += 2
        # apply correlation with that kernel
        result = self.correlate(kernel).clip()
        return result

    def edges(self):
        """Create image, which edge detect by apply Sobel operator"""
        result = Image.new(self.width, self.height)
        # defined kernels for Sobel operator
        kernel_x = ((-1, 0, 1),
                    (-2, 0, 2),
                    (-1, 0, 1))
        kernel_y = ((-1, -2, -1),
                    ( 0,  0,  0),
                    ( 1,  2,  1))
        # apply correlation whith these kernels
        o_x = self.correlate(kernel_x)
        o_y = self.correlate(kernel_y)
        # implement Sobel operator
        result.pixels = [(x ** 2 + y ** 2) ** 0.5
                        for x, y in zip(o_x.pixels, o_y.pixels)]
        result = result.clip()
        return result

    def shrink(self, n=1):
        """Create new image without n 'minimum energy' columns"""
        if n >= self.width:
            return Image(0, self.height, [])
        result = Image(self.width, self.height, self.pixels[:])
        for _ in range(n):
            # create energy map for the image
            energy_map = result.edges()
            # find index of minimum energy column
            index = energy_map.min_energy_column()
            # delete this column from the image
            result.pixels = [color for i, color in enumerate(result.pixels)
                                   if i % result.width != index]
            result.width -= 1
        return result

    def min_energy_column(self):
        """Return index of minimum energy column"""
        min_energy  = 255 * self.height
        result = 0
        for x in range(self.width):
            energy = 0
            for y in range(self.height):
                energy += self.get_pixel(x, y) 
            if energy < min_energy:
                min_energy = energy
                result = x
        return result

    def seam_carving(self, n=1):
        """Create a new image without n 'minimum energy' path from top to down"""
        result = Image(self.width, self.height, self.pixels[:])
        # do repeatedly
        for _ in range(n):
            # create energy map for the image
            map = result.edges()
            # transform energy map to cumulative energy map
            map.transform_map()
            # get seam coordinates from cumulative energy map
            path = map.get_min_path()
            # delete the seam from the image
            result.delete_path(path)
        return result

    def transform_map(self):
        """Transform energy map to cumulative energy map"""
        for y in range(1, self.height):
            for x in range(self.width):
                # take minimum cost path to one of the parent node
                min_parent_cost = min(self.get_pixel_alt(x_parent, y-1)
                                  for x_parent in (x-1, x, x+1))
                # find total cost to node
                min_cost = self.get_pixel(x, y) + min_parent_cost
                # change value in map
                self.set_pixel(x, y, min_cost)

    def get_min_path(self):
        """Return minimum cost path"""
        path = []
        # find leaf of path and add in to path
        _, x_min = min((self.get_pixel(x, self.height-1), x)
                        for x in range(self.width))
        path.append((x_min, self.height-1))
        # add other nodes
        for y in reversed(range(self.height-1)):
            x, _ = path[-1]
            # parents x (consider bounds)
            x_parents = (max(0, min(self.width-1, x_p)) for x_p in (x-1, x, x+1))
            _, x_min = min((self.get_pixel(x_p, y), x_p) for x_p in x_parents)
            path.append((x_min, y))
        return path

    def delete_path(self, path):
        """Delete seam from image"""
        seam_set = set(self._get_index(x, y) for x, y in path)
        self.pixels = [pixel for i, pixel in enumerate(self.pixels)
                             if i not in seam_set]
        self.width -= 1


    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()
    def reafter():
        tcl.after(500,reafter)
    tcl.after(500,reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass

    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
