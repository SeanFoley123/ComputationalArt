""" Make some trippy pictures maaaaaan"""
import math
import random
from PIL import Image


def build_random_function(min_depth, max_depth, func_list, level):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    if level == max_depth:
        return random.choice(func_list[0:2])

    elif level >= min_depth:
        func_index = random.randint(0, len(func_list)-1)
        if func_index<2:
            return func_list[func_index]
        else:
            a = build_random_function(min_depth, max_depth, func_list, level + 1)
            if func_index > 7:
                b = build_random_function(min_depth, max_depth, func_list, level + 1)
            else:
                b = lambda x, y: 1
            return lambda x, y: func_list[func_index](a(x, y), b(x, y))

    else:
        func_index = random.randint(2, len(func_list)-1)
        a = build_random_function(min_depth, max_depth, func_list, level + 1)
        if func_index > 7:
            b = build_random_function(min_depth, max_depth, func_list, level + 1)
        else:
            b = lambda x, y: 1
        return lambda x, y: func_list[func_index](a(x, y), b(x, y))
        

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    equi_map = (output_interval_end-1.0*output_interval_start)/(input_interval_end-input_interval_start)
    return (val-input_interval_start)*equi_map + output_interval_start


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)

def generate_art(filename, x_size=500, y_size=500):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    func_list = [lambda a, b : a, lambda a, b : b, lambda a, b : math.cos(math.pi*a), lambda a, b : math.sin(math.pi*a), lambda a, b : math.cos(2*math.pi*a),
        lambda a, b : math.sin(2*math.pi*a), lambda a, b : .2**abs(a), lambda a, b : a**3, lambda a, b : a*b, lambda a, b: .5*(a+b)]
    # red_function = lambda x, y: 0
    # green_function = lambda x, y: 0
    red_function = build_random_function(2, 2, func_list, 0)
    green_function = build_random_function(2, 2, func_list, 0)
    blue_function = build_random_function(2, 2, func_list, 0)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            # print 'hi'
            pixels[i, j] = (
                    color_map(red_function(x, y)),
                    color_map(green_function(x, y)),
                    color_map(blue_function(x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    # doctest.run_docstring_examples(evaluate_random_function, globals(), verbose=True)
    generate_art("myart"+".png")
