from PIL import Image
import sys, getopt

# characters for drawing
ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

# resize the image, maintaining the ratio
def resize(image, new_width):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height) / float(old_width)
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image

# change every pixel with similar character
def modify(image, buckets=25):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)

def do(image, width):
    # resize and convert into gray
    image = resize(image, width).convert('L')
    pixels = modify(image)
    # Construct the image from the character list
    new_image = [pixels[index: index + width] for index in range(0, len(pixels), width)]
    return '\n'.join(new_image)

def runner(inpath, outpath, width):
    image = None
    try:
        image = Image.open(inpath)
    except Exception:
        print('Unable to find image in', inpath)
        return
    image = do(image, width)
    # To print on console
    print(image)
    # and print to file
    f = open(outpath, 'w')
    f.write(image)
    f.close()

def help():
    print('\nusage: python3 asciish.py [-option] [arg]\n' \
          '\targs\t\t meaning\n' \
          '\t-h, --help\t show this help again\n' \
          '\t-i, --input\t input filename\n' \
          '\t-o, --output\t output filename\n' \
          '\t-w, --width\t ascii image width\n' \
          '')

if __name__ == '__main__':
    try:  
        opts, args = getopt.getopt(sys.argv[1:], 'hi:o:w:', ['help', 'input=', 'output=', 'width='])
        infile = 'input.png'
        outfile = 'output.txt'
        width = 100
        for name, value in opts:
            if name in ('-h', '--help'):
                help()
                sys.exit()
            elif name in ('-i', '--input'):
                infile = value
            elif name in ('-o', '--output'):
                outfile = value
            elif name in ('-w', '--width'):
                width = int(value)
        runner(infile, outfile, width)
    except getopt.GetoptError:
        help()