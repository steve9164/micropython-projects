# Written by Stephen Davies
# Converts a .png to a format read by load_image for the Quokka board

from PIL import Image
import zlib

def convert_image(filename, width, height):
  image = Image.open(filename)
  im_small = image.resize((width, height))
  # Convert resized image to black and white
  im_bw = im_small.convert('1')
  image_buf = im_bw.tobytes()
  compressed_im = zlib.compress(image_buf)
  # Note filename .qimz meaning zlib compressed quokka image
  out_filename = '{}.qimz'.format(filename)
  with open(out_filename, 'wb') as output_file:
    wh = bytearray([width, height])
    output_file.write(wh)
    output_file.write(compressed_im)
  print('Image converted! Upload {} to Quokka and use load_image.'.format(out_filename))
