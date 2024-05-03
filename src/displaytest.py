import board
import displayio
import rgbmatrix
import framebufferio
import terminalio
from adafruit_display_text.label import Label
import adafruit_imageload
import time


displayio.release_displays()
display = framebufferio.FramebufferDisplay(
    rgbmatrix.RGBMatrix(
        width=64, bit_depth=2,
        rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
        addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
        clock_pin=board.GP10, latch_pin=board.GP12, output_enable_pin=board.GP13),
    auto_refresh=False)

group = displayio.Group()
display.root_group = group


b, p = adafruit_imageload.load(f'chicken.bmp')
tile1 = displayio.TileGrid(b, pixel_shader=p)
tile1.x = 0
tile1.y = 10
group.append(tile1)



b, p = adafruit_imageload.load(f'washing.bmp')
tile2 = displayio.TileGrid(b, pixel_shader=p)
tile2.x = 2
tile2.y = 16
group.append(tile2)



b, p = adafruit_imageload.load(f'rain.bmp')
tile4 = displayio.TileGrid(b, pixel_shader=p)
tile4.x = 20
tile4.y = 0
group.append(tile4)








wg = displayio.Group()
wg.x = 45
wg.y = 5

line1 = Label(text="20C", font=terminalio.FONT, color=0xff9600)
wg.append(line1)

rect = Rect(0, 6, 17, 1, fill=0xda8f57)
wg.append(rect)
rect2 = Rect(0, 6, 5, 1, fill=0x9e5f30)
wg.append(rect2)

b, p = adafruit_imageload.load(f'sun.bmp')
icon = displayio.TileGrid(b, pixel_shader=p)
icon.y = 10
wg.append(icon)



group.pop()
group.append(wg)
display.refresh()







from adafruit_display_shapes.rect import Rect

group.pop()
group.pop()
rect = Rect(45, 11, 17, 1, fill=0xda8f57)
group.append(rect)
rect2 = Rect(45, 11, 5, 1, fill=0x9e5f30)
group.append(rect2)
display.refresh()


















while True:
  tile.x = (tile.x + 1) % 64
  tile2.x = (tile2.x + 1) % 64
  display.refresh()
  time.sleep(0.1)


