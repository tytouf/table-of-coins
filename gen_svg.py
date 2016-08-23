from optparse import OptionParser
from PIL import Image
import math

def my_range(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step


parser = OptionParser()
parser.add_option("-i", "--image", dest="image", type="string",
                  help="Image used to mask coins")
parser.add_option("--width", dest="width", type="int",
                  default=1200, help="Output width")
parser.add_option("--height", dest="height", type="int",
                  default=700, help="Output height")
parser.add_option("-d", "--diameter", dest="diameter", type="float",
                  default=16.5, help="Coin diameter")
parser.add_option("-s", "--staggered", dest="staggered",
                  action="store_true", help="Staggered rows")

(options, args) = parser.parse_args()

if options.image:
    img = Image.open(options.image)
    img = img.resize((options.width, options.height))
    data = list(img.getdata(0)) # get Red color

print('<svg width="{}mm" height="{}mm">'.format(options.width, options.height))

radius = options.diameter / 2
y_step = options.diameter if not options.staggered else options.diameter * math.cos(30*math.pi/180)
x_offset = 0

for y in my_range(radius, options.height, y_step):
    for x in my_range(radius - x_offset, options.width, options.diameter):
        i = math.floor(y) * options.width + math.floor(x)
        if data[i] < 120:
            print ('<circle cx="{}mm" cy="{}mm" r="{}mm"></circle>'.format(x, y, radius))
    x_offset = radius if x_offset == 0 else 0

print('</svg>')
