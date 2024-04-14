import board
import displayio
import rgbmatrix
import framebufferio
import terminalio
from adafruit_display_text.label import Label
import adafruit_imageload


class Box:
    pass

__m = Box()

def init_display():
    displayio.release_displays()
    __m.display = framebufferio.FramebufferDisplay(
        rgbmatrix.RGBMatrix(
            width=64, bit_depth=2,
            rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
            addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
            clock_pin=board.GP10, latch_pin=board.GP12, output_enable_pin=board.GP13),
        auto_refresh=False)

    group = displayio.Group()
    __m.display.root_group = group


    line1 = Label(text="", font=terminalio.FONT, color=0xff9600)
    line1.x = 2
    line1.y = 7
    group.append(line1)
    __m.line1 = line1


    line2 = Label(text="", font=terminalio.FONT, color=0xff9600)
    line2.x = 2
    line2.y = 21
    group.append(line2)
    __m.line2 = line2


    icons = ['chicken', 'mail', 'bin_green', 'bin_yellow', 'washing']
    __m.icons = {}
    for icon in icons:
        b, p = adafruit_imageload.load(f'{icon}.bmp')
        tile = displayio.TileGrid(b, pixel_shader=p)
        tile.hidden = True
        group.append(tile)
        __m.icons[icon] = tile



def set_line_1(text, color=0x000000):
    __m.line1.text = text
    __m.line1.color = color

def set_line_2(text, color=0x000000):
    __m.line2.text = text
    __m.line2.color = color


def set_icons(icons, position):
    for k, v in __m.icons.items():
        v.hidden = k not in icons
        if k in icons:
            v.x = 5 + 19 * icons.index(k)
        if position == 'c':
            v.y = 8
        elif position == 'b':
            v.y = 16
        elif position == 't':
            v.y = 2

def refresh_display():
    __m.display.refresh()
