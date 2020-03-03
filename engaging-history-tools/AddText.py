#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

#    callirhoe - high quality calendar rendering
#    Copyright (C) 2012-2015 George M. Tzoumas

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/

#   Basically this part is designed for adding text(like image description) into images

import sys

import Image, ImageDraw, ImageFont

# Text font；/Library/Fonts/
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 24)

# image:   text： font：
def add_text_to_image(image, text, font=font):
  rgba_image = image.convert('RGBA')
  text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
  image_draw = ImageDraw.Draw(text_overlay)

  text_size_x, text_size_y = image_draw.textsize(text, font=font)
  # text place
  print(rgba_image)
  text_xy = (rgba_image.size[0] - text_size_x, rgba_image.size[1] - text_size_y)
  # colour
  image_draw.text(text_xy, text, font=font, fill=(76, 234, 124, 180))

  image_with_text = Image.alpha_composite(rgba_image, text_overlay)

  return image_with_text

im_before = Image.open("uouo123.jpg")
im_before.show()
im_after = add_text_to_image(im_before, 'blog.uouo123.com')
im_after.show()
# im.save('im_after.jpg')
