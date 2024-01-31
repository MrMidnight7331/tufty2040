# @Name: Vinylizer tufty
# @Author: MrMidnight
# @Version: 4.1

# ==(Imports)================================================================================================================

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button
import time
import qrcode
from machine import Pin, PWM
import urandom as random
import json

# ==(Init Variables)================================================================================================================

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

BORDER_SIZE = 4
PADDING = 10
TOP_HEIGHT = 40

# Text
TOP_NAME = "Vinylizer"
desc = "By: MrMridnight, Version: 4.1"
ALBUM = "No Album found"
SIDE = ""
RNG_Count = 0
Discogs = "https://www.discogs.com/user/MrMidnight53/collection"
Status = "init"


pwm = PWM(Pin(25))
pwm.freq(1000)


# Initialize the variable
vinyl_albums = []

# Read vinyl albums from a JSON file
try:
    with open("vinyl_albums.json", "r") as file:
        vinyl_albums = json.load(file)
except OSError:
    print("Error: File not found or unable to open")
except ValueError:
    print("Error: JSON decoding failed")
except Exception as e:
    print(f"Error: {e}")


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
    display.text("Album:", BORDER_SIZE + PADDING, BORDER_SIZE + 10 + PADDING + TOP_HEIGHT + 5, WIDTH, 3)
    display.text(ALBUM, BORDER_SIZE + PADDING, BORDER_SIZE + 10 + PADDING + TOP_HEIGHT + 35, WIDTH, 2)

    # draw Side
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(SIDE, BORDER_SIZE + PADDING, BORDER_SIZE + 10 + PADDING + TOP_HEIGHT + 70, WIDTH, 3.5)

    # draw Count
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(f"RTD: {RNG_Count}", BORDER_SIZE + PADDING + 38, BORDER_SIZE + 125 + PADDING + TOP_HEIGHT + 30, WIDTH, 2)

    # draw Discogs
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("DISCOGS", BORDER_SIZE + PADDING + 117, BORDER_SIZE + 125 + PADDING + TOP_HEIGHT + 30, WIDTH, 2)

    # draw Reset
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("RESET", BORDER_SIZE + PADDING + 215, BORDER_SIZE + 125 + PADDING + TOP_HEIGHT + 30, WIDTH, 2)

# Draw management_mode
def management_mode():
    # draw border
    display.set_pen(LIGHTEST)
    display.clear()

    # draw background
    display.set_pen(DARK)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), HEIGHT - (BORDER_SIZE * 2))

    # draw Manage Mode text
    display.set_pen(LIGHT)
    display.set_font("bitmap8")
    display.text("Management Mode", BORDER_SIZE + PADDING -3, BORDER_SIZE + PADDING + TOP_HEIGHT, WIDTH, 4)

    # draw instructions
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("In the Console:", BORDER_SIZE + PADDING, BORDER_SIZE + 60 + PADDING + TOP_HEIGHT, WIDTH, 2)
    display.text("Enter (A) to Add", BORDER_SIZE + PADDING, BORDER_SIZE + 80 + PADDING + TOP_HEIGHT, WIDTH, 2)
    display.text("Enter (D) to Delete", BORDER_SIZE + PADDING, BORDER_SIZE + 100 + PADDING + TOP_HEIGHT, WIDTH, 2)
    display.text("Enter (L) to List", BORDER_SIZE + PADDING, BORDER_SIZE + 120 + PADDING + TOP_HEIGHT, WIDTH, 2)
    display.text("Enter (Q) to Quit", BORDER_SIZE + PADDING, BORDER_SIZE + 140 + PADDING + TOP_HEIGHT, WIDTH, 2)

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


# Function to add a new album to the vinyl_albums list
def add_album(album_name, album_sides):
    # Replace commas and commas followed by space with spaces and convert to uppercase for each side
    album_sides = [chr(65 + i) for i in range(int(album_sides))]

    new_album = {"name": album_name, "sides": album_sides}
    vinyl_albums.append(new_album)

# Function to display the list of albums with index numbers
def display_albums():
    print("Albums:")
    for i, album in enumerate(vinyl_albums):
        print(f"{i + 1}. {album['name']} - Sides: {', '.join(album['sides'])}")
        
# Function to delete an album from the vinyl_albums list by index
def delete_album(index):
    if 0 <= index < len(vinyl_albums):
        del vinyl_albums[index]

# Main function encapsulating the script
def manage_vinyls():
    print("Management Mode")
    global vinyl_albums
    
    # Read vinyl albums from a JSON file
    try:
        with open("vinyl_albums.json", "r") as file:
            vinyl_albums = json.load(file)
    except OSError:
        print("Error: File not found or unable to open")
        vinyl_albums = []

    while True:
        # Prompt user to write, delete, or list
        action = input("Do you want to (A)dd, (D)elete, (L)ist, or (Q)uit? ").upper()

        if action == "A":
            # Adding a new album
            album_name = input("Enter the album name: ")
            
            # Modified input handling
            try:
                sides_input = int(input("Enter the number of sides: "))
                add_album(album_name, sides_input)
            except ValueError:
                print("Invalid input. Please enter a valid number.")

            # Save the updated list to the vinyl_albums.json file
            with open("vinyl_albums.json", "w") as file:
                json.dump(vinyl_albums, file)

        elif action == "D":
            # Deleting an album
            display_albums()
            try:
                index = int(input("Enter the number of the album to delete: ")) - 1
                delete_album(index)

                # Save the updated list to the vinyl_albums.json file
                with open("vinyl_albums.json", "w") as file:
                    json.dump(vinyl_albums, file)
                print("Album deleted successfully!")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif action == "L":
            display_albums()

        elif action == "Q":
            draw_badge()
            display.update()
            time.sleep(0.5)
            Status = "vinylizer"
            break
            
        else:
            print("Invalid action. Please choose 'A' to Add, 'D' to delete, 'L' to list, or 'Q' to quit.")


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
        ALBUM = f"{random_album}"
        SIDE = f"Side: {random_side}"
        RNG_Count += 1
        
        

# ==(Main Function)================================================================================================================

init_badge()
display.update()

while True:
    
    if button_up.is_pressed and button_down.is_pressed:
        management_mode()
        display.update()
        time.sleep(0.5)
        manage_vinyls()
        
    elif Status == "init":
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
        if button_a.is_pressed or button_b.is_pressed or button_c.is_pressed or button_up.is_pressed or button_down.is_pressed:
            draw_badge()
            display.update()
            time.sleep(0.5)
            Status = "vinylizer"
