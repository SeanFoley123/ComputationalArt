import math
import random
from PIL import Image
from recursive_art2 import remap_interval, build_random_function, color_map, generate_art

def make_function():
	func_list = [lambda a, b : a, lambda a, b : b, lambda a, b : math.cos(math.pi*a), lambda a, b : math.sin(math.pi*a), lambda a, b : math.cos(2*math.pi*a),
	        lambda a, b : math.sin(2*math.pi*a), lambda a, b : .2**abs(a), lambda a, b : a**3, lambda a, b : a*b, lambda a, b: .5*(a+b)]
	function = build_random_function(8, 10, func_list, 0)
	return function

def new_picture(mark, nodes, distance, functions, filenumber):
	pixels = mark.load()
	x_size, y_size = mark.size
	for start_position in nodes:
		for theta in range(0, int(200*math.pi), int(math.pi/180*100)):
			x_position = min(max(int(start_position[0] + distance*math.cos(theta/100.0)), 0), x_size-1)
			y_position = min(max(int(start_position[1] + distance*math.sin(theta/100.0)), 0), y_size-1)
			pixels[x_position, y_position] = (color_map(functions[0](remap_interval(x_position, 0, x_size, -1, 1), remap_interval(y_position, 0, y_size, -1, 1))), color_map(functions[1](remap_interval(x_position, 0, x_size, -1, 1), remap_interval(y_position, 0, y_size, -1, 1))), color_map(functions[2](remap_interval(x_position, 0, x_size, -1, 1), remap_interval(y_position, 0, y_size, -1, 1))))

	mark.save("weird_mark" + str(filenumber) + ".png")

def reverse(real_mark, messed_up_mark, nodes, distance, functions, filenumber):
	mark_pixels = real_mark.load()
	messed_up_pixels = messed_up_mark.load()
	x_size, y_size = real_mark.size
	for start_position in nodes:
		for theta in range(0, int(200*math.pi), int(math.pi/180*100)):
			x_position = min(max(int(start_position[0] + distance*math.cos(theta/100.0)), 0), x_size-1)
			y_position = min(max(int(start_position[1] + distance*math.sin(theta/100.0)), 0), y_size-1)
			messed_up_pixels[x_position, y_position] = mark_pixels[x_position, y_position]
	messed_up_mark.save("weird_mark" + str(filenumber) + ".png")

markymark = Image.open('mark.jpg')
x_size, y_size = markymark.size

nodes = [(145, 130), (205, 140)]
# nodes = range(random.randint(4, 6))
# for i in nodes:
# 	nodes[i] = (random.randint(0, x_size), random.randint(0, y_size))

functions = [make_function(), make_function(), make_function()]
filenumber = 0
for distance in range(0, 100):
	filenumber +=1
	new_picture(markymark, nodes, distance, functions, filenumber)
new_mark = Image.open('mark.jpg')
for distance in range(0, 100):
	filenumber += 1
	reverse(new_mark, markymark, nodes, 100-1-distance, functions, filenumber)

for i in range(6):
	print i
	nodes = [(145, 130), (205, 140)]
	for i in range(random.randint(5, 8)):
		nodes.append((random.randint(0, x_size), random.randint(0, y_size)))
	functions = [make_function(), make_function(), make_function()]
	max_dist = random.randint(50, 180)
	for distance in range(max_dist):
		filenumber +=1
		new_picture(markymark, nodes, distance, functions, filenumber)
	new_mark = Image.open('mark.jpg')
	for distance in range(max_dist):
		filenumber += 1
		reverse(new_mark, markymark, nodes, max_dist-1-distance, functions, filenumber)