from md5 import md5
import os

from PIL import Image


def prepocess_captcha(image):
    pixel_data = image.load()
    output = []

    for x in xrange(image.size[0]):
        # The rightmost pixels gets a more sensitive threshold
        factor = x / 2.0
        threshold = 190 + factor

        for y in xrange(image.size[1]):
            pixel = pixel_data[x, y]

            if x - (y * 0.4) > 102:
                # Ignores the top-right white
                pass
            elif pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold:
                # Letter pixel found!
                output.append((x, y))

    return set(output)


def get_black_pixels(image):
    pixels = image.convert('1').load()

    width, height = image.size
    return {(i%width, i/width) for i in xrange(width * height) if not pixels[i%width, i/width]}


def neighbors_coords(x, y):
    return {(x, y+1), (x, y-1),
            (x-1, y+1), (x-1, y-1),
            (x+1, y+1), (x+1, y-1),
            (x-1, y), (x+1, y)}


def get_neighbors(pixels, image_set):
    out = set()
    for p in pixels:
        out |= neighbors_coords(*p)

    return out & image_set


def group_regions(image_array):
    region_list = []
    while image_array:
        region = {image_array.pop()}

        neighbors = get_neighbors(region, image_array)
        while neighbors:
            image_array -= neighbors
            region |= neighbors
            neighbors = get_neighbors(region, image_array)

        region_list.append(region)

    return region_list


def get_dimensions(region):
    min_x = min(region, key=lambda x: x[0])[0]
    min_y = min(region, key=lambda x: x[1])[1]
    width = max(region, key=lambda x: x[0])[0] - min_x + 1
    height = max(region, key=lambda x: x[1])[1] - min_y + 1

    return min_x, width, min_y, height


def region_to_image(region):
    min_x, width, min_y, height = get_dimensions(region)

    image = Image.new('1', (width, height), 'white')
    pixels = image.load()

    for p in region:
        pixels[p[0] - min_x, p[1] - min_y] = 0

    return image


def save_regions(regions, base_path='data/'):
    for r in regions:
        image = region_to_image(r)
        file_name = md5(image.tobytes()).hexdigest() + '.png'
        image.save(base_path + file_name)


def generate_letter_iamges():
    file_list = [f for f in os.listdir('captcha') if f.endswith('.jpg')]
    print "Processing {0} files".format(len(file_list))

    for i, file_name in enumerate(file_list):
        if not i % 1000:
            print "{0} of {1}".format(i, len(file_list))

        image = Image.open('captcha/' + file_name)
        regions = group_regions(prepocess_captcha(image))

        if len(regions) != 5:
            print "Ignoring file", file_name
        else:
            save_regions(regions)
