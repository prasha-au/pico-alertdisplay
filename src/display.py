import time
from math import sin
import board
import displayio
import rgbmatrix
import framebufferio
import terminalio
from adafruit_display_text.label import Label
import asyncio


class Box:
    pass

__m = Box()

def init_display():
    displayio.release_displays()
    display = framebufferio.FramebufferDisplay(
        rgbmatrix.RGBMatrix(
            width=64, bit_depth=2,
            rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
            addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
            clock_pin=board.GP10, latch_pin=board.GP12, output_enable_pin=board.GP13),
        auto_refresh=False)

    group = displayio.Group()

    line1 = Label(text="Hello", font=terminalio.FONT, color=0xff9600)
    line1.x = 2
    line1.y = 7
    group.append(line1)


    line2 = Label(text="<3 <3 <3", font=terminalio.FONT, color=0xff9600)
    line2.x = 2
    line2.y = 21
    group.append(line2)

    display.root_group = group

    __m.display = display


    __m.line1 = line1
    __m.line2 = line2


def set_line_1(text, color=0x444444):
    __m.line1.text = text
    __m.line1.color = color

def set_line_2(text, color=0x444444):
    __m.line2.text = text
    __m.line2.color = color

async def get_display_task():
    while True:
        __m.display.refresh()
        await asyncio.sleep(0.2)
