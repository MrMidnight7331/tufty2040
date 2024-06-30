# @Name: NFT-Slider
# @Author: MrMidnight
# @Version: 1.4

#==(Imports)=======================================================================================================================
from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button
import time
import jpegdec
import os

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
LIGHTEST = display.create_pen(203, 166, 247)
LIGHT = display.create_pen(245, 224, 220)
DARK = display.create_pen(30, 30, 46)
DARKEST = display.create_pen(30, 30, 46)

# Image Directory
NFT_DIR = "nfts"
print(f"Looking for collections in {NFT_DIR} directory...")
collections = [f for f in os.listdir(NFT_DIR) if f not in ('.', '..') and (os.stat(NFT_DIR + '/' + f)[0] & 0x4000)]
print(f"Found collections: {collections}")
current_collection_index = 0
current_image_index = 0
in_slideshow = False
in_menu = True

def get_image_files(collection):
    collection_path = NFT_DIR + '/' + collection
    print(f"Looking for images in {collection_path}...")
    files = [f for f in os.listdir(collection_path) if f.endswith('.jpg') or f.endswith('.jpeg')]
    print(f"Found images: {files}")
    return files

# Initialize the image files for the first collection
IMAGE_FILES = get_image_files(collections[current_collection_index])

if not IMAGE_FILES:
    raise RuntimeError("No images found in the collections")

# Print Image
def show_photo(image_name):
    j = jpegdec.JPEG(display)
    
    # Open the JPEG file
    print(f"Opening image file: {image_name}")
    j.open_file(image_name)
    
    # Decode the JPEG
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)

def draw_badge():
    display.set_pen(DARKEST)
    display.clear()

def update_display():
    draw_badge()
    
    # Display image on the left
    image_path = NFT_DIR + '/' + collections[current_collection_index] + '/' + IMAGE_FILES[current_image_index]
    show_photo(image_path)
    
    # Display text vertically on the right
    display.set_pen(LIGHTEST)
    text = IMAGE_FILES[current_image_index]
    if text.endswith('.jpg') or text.endswith('.jpeg'):
        text = text[:-4]  # Remove the file extension
    
    x = WIDTH - 60  # Adjust x-coordinate to move text to the left
    y = 1           # Adjust y-coordinate to control text position
    text_width = 20  # Adjust text width to fit the screen
    
    # Calculate number of characters per column
    num_chars_per_column = 12
    chars_left = text[:num_chars_per_column]
    chars_right = text[num_chars_per_column:]
    
    # Display left column of text
    for i, char in enumerate(chars_left):
        display.text(char, x, y + i * 20, scale=3)
    
    # Display right column of text
    for i, char in enumerate(chars_right):
        display.text(char, x + text_width + 10, y + i * 20, scale=3)
    
    display.update()


def show_menu():
    display.set_pen(DARKEST)
    display.clear()
    display.set_pen(LIGHTEST)
    display.text("NFT Slider", 10, 10, 10, 4)
    
    # Display collections
    text_height = 20  # Adjust spacing between lines
    y_start = 100     # Starting y-coordinate for collections
    
    for i, collection in enumerate(collections):
        if i == current_collection_index:
            display.set_pen(LIGHTEST)
        else:
            display.set_pen(LIGHT)
        display.text(collection, 10, y_start + i * text_height, scale=3)
    
    display.update()



def slideshow():
    global current_image_index, in_slideshow
    while in_slideshow:
        current_image_index = (current_image_index + 1) % len(IMAGE_FILES)
        update_display()
        for _ in range(50):  # Check every 0.1 seconds if the slideshow should stop
            if button_b.is_pressed:
                in_slideshow = False
                return
            time.sleep(0.2)

# Draw the initial menu
show_menu()

# Buttons
while True:
    if in_menu:
        if button_up.is_pressed:
            current_collection_index = (current_collection_index - 1) % len(collections)
            show_menu()
            time.sleep(0.2)
        elif button_down.is_pressed:
            current_collection_index = (current_collection_index + 1) % len(collections)
            show_menu()
            time.sleep(0.2)
        elif button_a.is_pressed:
            in_menu = False
            IMAGE_FILES = get_image_files(collections[current_collection_index])
            current_image_index = 0
            update_display()
            time.sleep(0.2)
        elif button_c.is_pressed:
            in_menu = False
            time.sleep(0.2)
    else:
        if button_b.is_pressed:
            in_slideshow = not in_slideshow
            if in_slideshow:
                slideshow()
            time.sleep(0.2)
        elif button_a.is_pressed:
            if in_slideshow:
                in_slideshow = False
            current_image_index = (current_image_index - 1) % len(IMAGE_FILES)
            update_display()
            time.sleep(0.2)
        elif button_c.is_pressed:
            if in_slideshow:
                in_slideshow = False
            current_image_index = (current_image_index + 1) % len(IMAGE_FILES)
            update_display()
            time.sleep(0.2)
        elif button_up.is_pressed or button_down.is_pressed:
            in_menu = True
            show_menu()
            time.sleep(0.2)
    time.sleep(0.1)  # Main loop delay to prevent excessive CPU usage

