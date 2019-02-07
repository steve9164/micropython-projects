# Written by Stephen Davies
# Converts a .png to a format read by load_image for the Quokka board

from PIL import Image
import zlib
import sys

def convert_image(filename, width=None, height=None):
  image = Image.open(filename)
  if width and height:
    image = image.resize((width, height))
  # Convert resized image to black and white
  im_bw = image.convert('1')
  image_buf = im_bw.tobytes()
  compressed_im = zlib.compress(image_buf)
  # Note filename .qimz meaning zlib compressed quokka image
  out_filename = '{}.qimz'.format('.'.join(filename.split('.')[0:-1]))
  with open(out_filename, 'wb') as output_file:
    wh = bytearray([image.width, image.height])
    output_file.write(wh)
    output_file.write(compressed_im)
  print('Image converted! Upload {} to Quokka and use load_image.'.format(out_filename))

if __name__ == '__main__':
  convert_image(sys.argv[1])
