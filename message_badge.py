from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332
import math
import time
from pimoroni import Button

display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332, rotate=180)

button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)



# convert a hue, saturation, and value into rgb values
def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p, q, t = v * (1.0 - s), v * (1.0 - s * f), v * (1.0 - s * (1.0 - f))
    v, t, p, q = int(v * 255), int(t * 255), int(p * 255), int(q * 255)
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q

message = "   Hello World!"
display.set_backlight(1.0)


text_size = 7
message_width = display.measure_text(message, text_size)

x_scroll = 0

while 1:

    
    t = time.ticks_ms() / 1000.0
    display.set_pen(display.create_pen(30, 30, 46))
    display.clear()

    x_scroll -= 10
    if x_scroll < -(message_width + 320 + 100):
        x_scroll = 0

    # for each character we'll calculate a position and colour, then draw it
    for i in range(0, len(message)):
        cx = int(x_scroll + (i * text_size * 5.5))
        cy = int(80 + math.sin(t * 10 + i) * 20)

        # to speed things up we only bother doing the hardware if the character will be visible on screen
        if cx > -50 and cx < 320:
            # draw a shadow for the character
            #display.set_pen(display.create_pen(0, 0, 0))
            #display.text(message[i], cx + 15, cy + 15, -1, text_size)

            # generate a rainbow colour that cycles with time
            r, g, b = hsv_to_rgb(i / 10 + t / 5, 1, 1)
            display.set_pen(display.create_pen(r, g, b))
            display.text(message[i], cx, cy, -1, text_size)
            

            
    if button_a.is_pressed:
        message = "   we do a lil hacking :)"
    elif button_b.is_pressed:
        message = "   we do a lil programming :0" 
    elif button_c.is_pressed:
        message = "   we do a lil gaming ;)" 
    elif button_up.is_pressed:
        message = "   we do a lil trolling 0.0"         
    elif button_down.is_pressed:
        message = "   we do a lil scamming ._."         
    display.update()
     


    


    


