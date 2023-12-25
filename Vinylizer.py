# @Name: Vinylizer tufty
# @Author: MrMidnight
# @Version: 2.6

#==(Imports)================================================================================================================

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button
import time
import qrcode
from machine import Pin, PWM
import urandom as random


#==(Init Variables)================================================================================================================

vinyl_albums = [
    # Add more albums if needed:
    # {"name": "Name", "sides": ["A", "B"]},
    
    {"name": "Stray OST", "sides": ["A", "B", "C", "D"]},
    {"name": "Happier Than Ever", "sides": ["A", "B", "C", "D"]},
    {"name": "Ballo Della Vita", "sides": ["A", "B"]},
    {"name": "1989 (Taylor's Version)", "sides": ["A", "B", "C", "D"]},
    {"name": "Thriller", "sides": ["A", "B"]},
       
]

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

# Buttons assignment
button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)

# Mytheme
LIGHTEST = display.create_pen(203, 166, 247)
LIGHT = display.create_pen(245, 224, 220)
DARK = display.create_pen(30, 30, 46)
DARKEST = display.create_pen(30, 30, 46)

BORDER_SIZE = 4
PADDING = 10
TOP_HEIGHT = 40

# Text
TOP_NAME = "Vinylizer"
desc = "By: MrMridnight, Version: 2.6"
ALBUM = "No Album found"
SIDE = ""
RNG_Count = 0
Discogs = "https://www.discogs.com/user/MrMidnight53/collection"
Status = "init"


pwm = PWM(Pin(25))
pwm.freq(1000)


#==(Define Functions)================================================================================================================

def blink_light():
    for duty in range(65025, 0, -1):
        pwm.duty_u16(duty)

# Draw Starting Screen
def init_badge():
    # draw border
    display.set_pen(LIGHTEST)
    display.clear()

    # draw background
    display.set_pen(DARK)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), HEIGHT - (BORDER_SIZE * 2))

    # draw INIT text
    display.set_pen(LIGHT)
    display.set_font("bitmap6")
    display.text(TOP_NAME, BORDER_SIZE + 13 + PADDING, BORDER_SIZE + PADDING + TOP_HEIGHT, WIDTH, 6)
    
    # draw Version etc.
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(desc, BORDER_SIZE + 20 +  PADDING, BORDER_SIZE + 10 + PADDING + TOP_HEIGHT + 35, WIDTH, 2)
    
    # draw Count
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("START", BORDER_SIZE + PADDING + 40, BORDER_SIZE + 125 + PADDING + TOP_HEIGHT + 30, WIDTH, 2)


# Draw Vinylizer Badge
def draw_badge():
    # draw border
    display.set_pen(LIGHTEST)
    display.clear()

    # draw background
    display.set_pen(DARK)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), HEIGHT - (BORDER_SIZE * 2))

    # draw TOP text
    display.set_pen(LIGHT)
    display.set_font("bitmap6")
    display.text(TOP_NAME, BORDER_SIZE + PADDING, BORDER_SIZE + PADDING, WIDTH, 5)

    # draw Album name
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(ALBUM, BORDER_SIZE + PADDING, BORDER_SIZE + 10 + PADDING + TOP_HEIGHT, WIDTH, 3.5)

    # draw Side
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(SIDE, BORDER_SIZE + PADDING, BORDER_SIZE + 10 + PADDING + TOP_HEIGHT + 60, WIDTH, 3.5)

    # draw Count
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(f"RTD: {RNG_Count}", BORDER_SIZE + PADDING + 40, BORDER_SIZE + 125 + PADDING + TOP_HEIGHT + 30, WIDTH, 2)
    
    # draw Discogs
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("DISCOGS", BORDER_SIZE + PADDING + 120, BORDER_SIZE + 125 + PADDING + TOP_HEIGHT + 30, WIDTH, 2)    
    
    
    # draw Reset
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("RESET", BORDER_SIZE + PADDING + 220, BORDER_SIZE + 125 + PADDING + TOP_HEIGHT + 30, WIDTH, 2)


# QR Code requirements
def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size

def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.set_pen(LIGHTEST)
    display.rectangle(ox, oy, size, size)
    display.set_pen(DARKEST)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size , oy + y * module_size, module_size, module_size)


# Draws QR Code
def show_qr():
    display.set_pen(DARK)
    display.clear()

    code = qrcode.QRCode()
    code.set_text(Discogs)

    size, module_size = measure_qr_code(HEIGHT, code)
    left = int((WIDTH // 2) - (size // 2))
    top = int((HEIGHT // 2) - (size // 2))

    draw_qr_code(left, top, size, code)
    display.update()
    blink_light()
    
    
# Randomizer
def randomize_vinyl(albums):
    if not albums:
        print("No albums available.")
        return None, None

    random_album = random.choice(albums)
    random_side = random.choice(random_album['sides'])

    return random_album['name'], random_side


# RNG
def rng():
    global ALBUM, SIDE, RNG_Count  # Declare global variables
    random_album, random_side = randomize_vinyl(vinyl_albums)
    if random_album is not None and random_side is not None:
        ALBUM = f"Album: {random_album}"
        SIDE = f"Side: {random_side}"
        RNG_Count += 1
        
        
#==(Main Function)================================================================================================================
        
init_badge()
display.update()

while True:
    if Status == "init":
        if button_a.is_pressed:
            rng()
            draw_badge()
            display.update()
            time.sleep(0.5)
            Status = "vinylizer"
            
    elif Status == "vinylizer":
        
        if button_a.is_pressed:
            rng()
            draw_badge()
            display.update()
            time.sleep(0.5)
            Status = "vinylizer"
        
        elif button_b.is_pressed:
            show_qr()
            Status = "qr"
        elif button_c.is_pressed:
            RNG_Count = 0
            init_badge()
            display.update()
            blink_light()
            Status = "init"
            time.sleep(0.5)
            
    
    elif Status == "qr":
        if button_a.is_pressed or button_b.is_pressed or button_c.is_pressed:
            rng()
            draw_badge()
            display.update()
            time.sleep(0.5)
            Status = "vinylizer"