""" Make some trippy pictures maaaaaan"""
import math
import random
from PIL import Image


def build_random_function(min_depth, max_depth, len_dict, level):
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
        return random.choice([['x'], ['y']])
    func = random.choice(len_dict.keys())
    length = len_dict[func]
    print level
    if length == 1:
        return [func]
    if length == 2:
        return [func, build_random_function(min_depth, max_depth, len_dict, level+1)]
    if length == 3:
        return [func, build_random_function(min_depth, max_depth, len_dict, level+1), build_random_function(min_depth, max_depth, len_dict, level+1)]

def evaluate_random_function(f, x, y, func_dict):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(Symbol('x'),-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(Symbol('y'),0.1,0.02)
        0.02
    """
    if len(f) == 1:
        return func_dict[f[0]](x, y)
    elif len(f) == 2:
        return func_dict[f[0]](evaluate_random_function(f[1], x, y, func_dict))
    elif len(f) == 3:
        return func_dict[f[0]](evaluate_random_function(f[1], x, y, func_dict), evaluate_random_function(f[2], x, y, func_dict))


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
    func_dict = {'x': lambda a, b : x, 'y': lambda a, b : y, 'cos_pi': lambda a : math.cos(math.pi*a), 'sin_pi': lambda a : math.sin(math.pi*a),
    'cos_2pi': lambda a : math.cos(2*math.pi*a), 'sin_2pi': lambda a : math.sin(2*math.pi*a), 'prod': lambda a, b : a*b, 'avg': lambda a, b: .5*(a+b),
    'exp': lambda a: .2**abs(a), 'cubic': lambda a: a**3}
    len_dict = {'cos_pi': 2, 'sin_pi': 2, 'cos_2pi': 2, 'sin_2pi': 2, 'prod': 3, 'avg': 3, 'exp': 2, 'cubic': 2}
    red_function = build_random_function(0, 3, len_dict, 0)
    green_function = build_random_function(0, 3, len_dict, 0)
    blue_function = build_random_function(0, 3, len_dict, 0)
    print red_function
    print green_function
    print blue_function
    
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y, func_dict)),
                    color_map(evaluate_random_function(green_function, x, y, func_dict)),
                    color_map(evaluate_random_function(blue_function, x, y, func_dict))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    # doctest.run_docstring_examples(evaluate_random_function, globals(), verbose=True)

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")  
    #'x': 1, 'y': 1,  