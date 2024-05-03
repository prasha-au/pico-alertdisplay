import board
import displayio
import rgbmatrix
import framebufferio
import terminalio
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect
import adafruit_imageload

class Box:
    timer1: Label = None
    timer2: Label = None
    weather: displayio.Group = None
    icons: list[(str, displayio.TileGrid)] = None
    last_weather_icon: str | None = None

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


    timer1 = Label(text="", font=terminalio.FONT, color=0xff9600, x=2, y=7)
    group.append(timer1)
    __m.timer1 = timer1


    timer2 = Label(text="", font=terminalio.FONT, color=0xff9600, x=2, y=21)
    group.append(timer2)
    __m.timer2 = timer2

    __m.icons = []


    weather = displayio.Group(x=45, y=5)
    weather.append(Label(text="", font=terminalio.FONT, color=0xda8f57))
    weather.append(Rect(0, 6, 17, 1, fill=0x000000))
    weather.append(Rect(0, 6, 1, 1, fill=0x000000))
    weather.append(Rect(0, 0, 1, 1, fill=0x000000))
    __m.weather = weather
    __m.last_weather_icon = None
    group.append(weather)


def set_power(is_on: bool):
    __m.display.root_group.hidden = not is_on

def set_timer_1(text, color=0x000000):
    __m.timer1.text = text
    __m.timer1.color = color

def set_timer_2(text, color=0x000000):
    __m.timer2.text = text
    __m.timer2.color = color


def set_weather(temp, temp_pct, icon):
    __m.weather[0].text = f'{temp}C'
    pct_width = (17 * temp_pct) // 100
    __m.weather[1] = Rect(0, 6, 17, 1, fill=0xda8f57)
    __m.weather[2] = Rect(0, 6, max(1, pct_width), 1, fill=0x9e5f30)
    __m.weather[2].hidden = pct_width == 0
    if __m.last_weather_icon != icon:
        b, p = adafruit_imageload.load(f'{icon}.bmp')
        tile = displayio.TileGrid(b, pixel_shader=p, y=10)
        __m.weather[3] = tile
        __m.last_weather_icon = icon


def set_icon_visibility(icon, is_visible):
    icon_names = [ v[0] for v in __m.icons ]

    if is_visible:
        if icon in icon_names:
            return
        b, p = adafruit_imageload.load(f'{icon}.bmp')
        tile = displayio.TileGrid(b, pixel_shader=p)
        __m.icons.append((icon, tile))
        __m.display.root_group.append(tile)
    else:
        if icon not in icon_names:
            return
        item = next((v for v in __m.icons if v[0] == icon))
        __m.display.root_group.remove(item[1])
        __m.icons.remove(item)



def _assert_icon(idx: int, hidden: bool, coords: tuple[int, int] | None = None):
    if idx < len(__m.icons):
        __m.icons[idx][1].hidden = hidden
        if coords is not None:
            __m.icons[idx][1].x = coords[0]
            __m.icons[idx][1].y = coords[1]


# Layout with 2 icons and weather
def _set_layout_1():
    __m.timer1.hidden = True
    __m.timer2.hidden = True
    __m.weather.hidden = False
    _assert_icon(0, False, (2, 8))
    _assert_icon(1, False, (22, 8))
    _assert_icon(2, True)
    _assert_icon(3, True)


# Layout with 4 icons and weather
def _set_layout_2():
    __m.timer1.hidden = True
    __m.timer2.hidden = True
    __m.weather.hidden = False
    _assert_icon(0, False, (2, 1))
    _assert_icon(1, False, (22, 1))
    _assert_icon(2, False, (2, 16))
    _assert_icon(3, False, (22, 16))


# Layout with 1 timer and 3 icons
def _set_layout_3():
    __m.timer1.hidden = False
    __m.timer2.hidden = True
    __m.weather.hidden = True
    _assert_icon(0, False, (2, 16))
    _assert_icon(1, False, (22, 16))
    _assert_icon(2, False, (42, 16))
    _assert_icon(3, True)

# Layout with 2 timers
def _set_layout_4():
    __m.timer1.hidden = False
    __m.timer2.hidden = False
    __m.weather.hidden = True
    _assert_icon(0, True)
    _assert_icon(1, True)
    _assert_icon(2, True)
    _assert_icon(3, True)




def refresh_display():
    if __m.timer1.text != "":
        if __m.timer2.text != "":
            _set_layout_4()
        else:
            _set_layout_3()
    else:
        if len(__m.icons) > 2:
            _set_layout_2()
        else:
            _set_layout_1()
    __m.display.refresh()
