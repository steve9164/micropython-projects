# Micropython image loader. Works with .qim and .qimz files created by convert_image

import framebuf
import zlib

def load_image(filename, compressed=None):
  if compressed is None
    compressed = filename.endswith('.qimz')
  # Open the image
  with open(filename, 'rb') as f:
    wh = f.read(2)
    width = int(wh[0])
    height = int(wh[1])
    im_buf = bytearray(f.read())
  if compressed:
    im_buf = zlib.decompress(im_buf)
  return framebuf.FrameBuffer(im_buf, width, height, framebuf.MONO_HLSB)

