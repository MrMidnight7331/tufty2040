# @Name: Hacker Badge
# @Author: MrMidnight
# @Version: 2.1


#==(Imports)=======================================================================================================================

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button
import time
import jpegdec
import qrcode
from machine import Pin, PWM


#==(Init Variables)================================================================================================================

# Buttons assignment
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)
button_boot = Button(23, invert=False)

WIDTH, HEIGHT = display.get_bounds()

# Mytheme
LIGHTEST= display.create_pen(203, 166, 247)
LIGHT = display.create_pen(245, 224, 220)
DARK = display.create_pen(30, 30, 46)
DARKEST = display.create_pen(30, 30, 46)


# Change badge and QR details here!
TOP_NAME = "Hacker:"
NAME = "Mr.Midnight"
BLURB1 = "HTB: Pro-Hacker"
BLURB2 = "Main: Hack, Code"
BLURB3 = "Misc: CTF, OSINT"
BLURB4 = "Cert: eJPT"

QR_TEXT1 = "https://twitter.com/MrMidnight53"
QR_TEXT2 = "https://youtube.com/@mrmidnight7331?si=7tnpSpfo6dE_eKiP"
QR_TEXT3 = "https://github.com/MrMidnight7331"

IMAGE_NAME = "profilepicture.jpg"

BORDER_SIZE = 4
PADDING = 10
TOP_HEIGHT = 40


#==(Define Functions)===============================================================================================================

# Draws badge
def draw_badge():
    # draw border
    display.set_pen(LIGHTEST)
    display.clear()

    # draw background
    display.set_pen(DARK)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), HEIGHT - (BORDER_SIZE * 2))

    # draw TOP box
    display.set_pen(DARKEST)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), TOP_HEIGHT)

    # draw TOP text
    display.set_pen(LIGHT)
    display.set_font("bitmap6")
    display.text(TOP_NAME, BORDER_SIZE + PADDING, BORDER_SIZE + PADDING, WIDTH, 3)

    # draw name text
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(NAME, BORDER_SIZE + PADDING, BORDER_SIZE + PADDING + TOP_HEIGHT, WIDTH, 5)

    # draws the bullet points
    display.set_pen(LIGHTEST)
    display.text("-", BORDER_SIZE + PADDING + 120 + PADDING, 105, 160, 2)
    display.text("-", BORDER_SIZE + PADDING + 120 + PADDING, 140, 160, 2)
    display.text("-", BORDER_SIZE + PADDING + 120 + PADDING, 175, 160, 2)
    display.text("-", BORDER_SIZE + PADDING + 120 + PADDING, 210, 160, 2)
    
    # draws the blurb text (4 - 5 words on each line works best)
    display.set_pen(LIGHTEST)
    display.text(BLURB1, BORDER_SIZE + PADDING + 135 + PADDING, 105, 160, 2)
    display.text(BLURB2, BORDER_SIZE + PADDING + 135 + PADDING, 140, 160, 2)
    display.text(BLURB3, BORDER_SIZE + PADDING + 135 + PADDING, 175, 160, 2)
    display.text(BLURB4, BORDER_SIZE + PADDING + 135 + PADDING, 210, 160, 2)

# Print PFP
def show_photo():
    j = jpegdec.JPEG(display)

    # Open the JPEG file
    j.open_file(IMAGE_NAME)

    # Draws a box around the image
    display.set_pen(DARKEST)
    display.rectangle(PADDING, HEIGHT - ((BORDER_SIZE * 2) + PADDING) - 120, 120 + (BORDER_SIZE * 2), 120 + (BORDER_SIZE * 2))

    # Decode the JPEG
    j.decode(BORDER_SIZE + PADDING, HEIGHT - (BORDER_SIZE + PADDING) - 120)

# More QR code stuff
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

# Shows Twitter
def show_qr():
    display.set_pen(DARK)
    display.clear()

    code = qrcode.QRCode()
    code.set_text(QR_TEXT1)

    size, module_size = measure_qr_code(HEIGHT, code)
    left = int((WIDTH // 2) - (size // 2))
    top = int((HEIGHT // 2) - (size // 2))
    draw_qr_code(left, top, HEIGHT, code)
    
    display.set_pen(LIGHT)
    display.text("T", 19, 10)
    display.text("w", 19, 30)
    display.text("i", 20, 50)
    display.text("t", 20, 70)
    display.text("t", 20, 90)
    display.text("e", 20, 110)
    display.text("r", 20, 130)

# Shows YouTube
def show_qr2():
    display.set_pen(DARK)
    display.clear()

    code = qrcode.QRCode()
    code.set_text(QR_TEXT2)

    size, module_size = measure_qr_code(HEIGHT, code)
    left = int((WIDTH // 2) - (size // 2))
    top = int((HEIGHT // 2) - (size // 2))
    draw_qr_code(left, top, HEIGHT, code)
    
    
    display.set_pen(LIGHT)
    display.text("Y", 20, 10)
    display.text("o", 20, 30)
    display.text("u", 20, 50)
    display.text("T", 20, 70)
    display.text("u", 20, 90)
    display.text("b", 20, 110)
    display.text("e", 20, 130)
    
# Shows GitHub
def show_qr3():
    display.set_pen(DARK)
    display.clear()

    code = qrcode.QRCode()
    code.set_text(QR_TEXT3)

    size, module_size = measure_qr_code(HEIGHT, code)
    left = int((WIDTH // 2) - (size // 2))
    top = int((HEIGHT // 2) - (size // 2))
    draw_qr_code(left, top, HEIGHT, code)
    
    
    display.set_pen(LIGHT)
    display.text("G", 20, 10)
    display.text("i", 20, 30)
    display.text("t", 20, 50)
    display.text("H", 20, 70)
    display.text("u", 20, 90)
    display.text("b", 20, 110)



# draw the badge for the first time
badge_mode = "photo"
draw_badge()
show_photo()
display.update()

# light variables

pwm = PWM(Pin(25))

pwm.freq(1000)

def blink_light():
    for duty in range(65025, 0, -1):
        pwm.duty_u16(duty)


#==(Main Function)================================================================================================================

while True:
    if button_up.is_pressed or button_down.is_pressed:
        badge_mode = "photo"
        draw_badge()
        show_photo()
        display.update()
        blink_light()
    
    elif button_a.is_pressed:
            badge_mode = "qr"
            show_qr()
            display.update()
            blink_light()
       
    elif button_b.is_pressed:
            badge_mode = "qr"
            show_qr2()
            display.update()
            blink_light()

    elif button_c.is_pressed:
            badge_mode = "qr"
            show_qr3()
            display.update()
            blink_light()