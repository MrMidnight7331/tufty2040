# @Name: Rock Paper Scissors tufty
# @Author: MrMidnight
# @Version: 1.4

#==(Imports)=======================================================================================================================

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button
import time
from machine import Pin, PWM
import urandom as random


#==(Init Variables)================================================================================================================

# Initialize display
WIDTH = 240
HEIGHT = 135
BORDER_SIZE = 5
PADDING = 5
TOP_HEIGHT = 20

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

# Buttons assignment
button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)

# Mytheme
LIGHTEST = display.create_pen(203, 166, 247)
LIGHT = display.create_pen(245, 224, 220)
DARK = display.create_pen(30, 30, 46)
DARKEST = display.create_pen(30, 30, 46)

# Text
TITLE = "Rock Paper Scissors"
COMPUTER = ""
PLAYER = ""
WLD = ""
P_WIN = 0
C_WIN = 0

# Light
pwm = PWM(Pin(25))
pwm.freq(1000)

# Initialize computer_rng
computer_rng = None


#==(Define Functions)===============================================================================================================

def blink_light():
    for duty in range(65025, 0, -1):
        pwm.duty_u16(duty)

# Draw RPS Badge
def draw_badge():
    # draw border
    display.set_pen(LIGHTEST)
    display.clear()

    # draw background
    display.set_pen(DARK)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), HEIGHT - (BORDER_SIZE * 2))

    # draw TITLE
    display.set_pen(LIGHT)
    display.set_font("bitmap6")
    display.text(TITLE, BORDER_SIZE + PADDING, BORDER_SIZE + PADDING, WIDTH, 5)

    # draw ROCK
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("ROCK", BORDER_SIZE + PADDING + 40, BORDER_SIZE + 150 + PADDING + TOP_HEIGHT + 30, WIDTH, 2)
    
    # draw PAPER
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("PAPER", BORDER_SIZE + PADDING + 130, BORDER_SIZE + 150 + PADDING + TOP_HEIGHT + 30, WIDTH, 2)    
    
    # draw SCISSORS
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("SCISSORS", BORDER_SIZE + PADDING + 210, BORDER_SIZE + 150 + PADDING + TOP_HEIGHT + 30, WIDTH, 2)
    
    # draw COMPUTER CHOICE name
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("Computer: " + COMPUTER, BORDER_SIZE + PADDING, BORDER_SIZE + 70 + PADDING + TOP_HEIGHT, WIDTH, 3.5)

    # draw WIN LOOSE DRAW
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(WLD, BORDER_SIZE + PADDING, BORDER_SIZE + 100 + PADDING + TOP_HEIGHT, WIDTH, 3.5)
    
    # draw PLAYER count
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(f"PLAYER: {P_WIN}", BORDER_SIZE + PADDING, BORDER_SIZE + 130 + PADDING + TOP_HEIGHT, WIDTH, 2)
    
    # draw COMPUTER count
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(f"CPU: {C_WIN}", BORDER_SIZE + PADDING, BORDER_SIZE + 150 + PADDING + TOP_HEIGHT, WIDTH, 2)

    # draw RESET 1 count
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("RESET", BORDER_SIZE + PADDING + 250, BORDER_SIZE + 35 + PADDING + TOP_HEIGHT, WIDTH, 2)
    
    # draw RESET 2 count
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("RESET", BORDER_SIZE + PADDING + 250, BORDER_SIZE + 130 + PADDING + TOP_HEIGHT, WIDTH, 2)


# RPS Logic
def logic(userimp):
    
    global computer_rng, WLD, P_WIN, C_WIN  # Make computer_rng accessible from the function

    choices = ["rock", "paper", "scissors"]

    computer_rng = random.choice(choices)
    
    if computer_rng == userimp:
        WLD = "It's a Draw!"
        C_WIN += 1
        P_WIN += 1
    elif userimp == "rock":
        if computer_rng == "scissors":
            WLD = "Player Wins!"
            P_WIN += 1
        else:
            WLD = "Computer Wins!"
            C_WIN += 1
    elif userimp == "paper":
        if computer_rng == "rock":
            WLD = "Player Wins!"
            P_WIN += 1
        else:
            WLD = "Computer Wins!"
            C_WIN += 1
    elif userimp == "scissors":
        if computer_rng == "paper":
            WLD = "Player Wins!"
            P_WIN += 1
        else:        
            WLD = "Computer Wins!"
            C_WIN += 1
            
            
#==(Main Function)================================================================================================================

draw_badge()
display.update()

while True:
    if button_a.is_pressed:
        userimp = "rock" 
        logic(userimp)
        COMPUTER = computer_rng
        draw_badge()
        display.update()
        time.sleep(0.3)
        
    elif button_b.is_pressed:
        userimp = "paper"
        logic(userimp)
        COMPUTER = computer_rng
        draw_badge()
        display.update()
        time.sleep(0.3)
        
    elif button_c.is_pressed:
        userimp = "scissors"
        logic(userimp)
        COMPUTER = computer_rng
        draw_badge()
        display.update()
        time.sleep(0.3)
        
    elif button_up.is_pressed or button_down.is_pressed:
        COMPUTER = ""
        C_WIN = 0
        P_WIN = 0
        WLD = ""
        draw_badge()
        display.update()
        
        