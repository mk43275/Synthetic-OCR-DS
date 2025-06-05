#----------------------LIBRARIES----------------------
import turtle               # Draw graphics (including the text from OCR text dataset)
import tkinter as tk        # Mainly used for tilting text in turtle
from PIL import Image       # type: ignore # Convert EPS to PNG using PIL
import albumentations as A  # type: ignore # Augmentations effects for images
import cv2                  # type: ignore # Read and write images
import pandas as pd         # type: ignore # Read the OCR text dataset
import random
from copy import deepcopy
import os

# ----------------------CONSTANTS/GLOBALS----------------------
IMG_NUM = 0
PREV_IMG_NUM = -1                                  # always behind IMG_NUM by 1
FILE_NAME_SAVE_AS = 'OCR_IMG_'                     # The OCR text dataset
DIR_LOC = 'OCR_Image_Dataset/'                     # The directory location to save the images
OUT_OF_BOUNDS_ERR = 10
FILL_ERR = 30
FORMAT_TYPE = '.jpeg'                              # The format of the image to be saved
ANGLE = [0, 15, 30, 45, 60, 75, 90]                # ANGLE[0] is default
FONT = ['Arial', 'Courier', 'Times New Roman', 
        'Verdana', 'Helvetica', 'Onyx', 'MS Gothic',
        'Lato', 'Ubuntu', 'MoolBoran', 'Mesquite Std']
FONT_SIZE = [30, 34, 40, 46, 50, 56, 60, 68, 78, 86]
EMPHASIS = ['normal', 'bold']
COLOR = ['red', 'green', 'blue', 'gold',
         'lavender', 'orange', 'lightblue',
         'lightgreen', 'pink', 'brown', 'grey']                             
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

# ----------------------HELPER FUNCTIONS----------------------
def kill_turtle():
    turtle.bye()

def reset_turtle_env():
    turtle.clearscreen()
    turtle.resetscreen()

# Number of predefined shapes: 9
def draw_square(turtle_obj, x, y, size, color):
    turtle_obj.penup()
    turtle_obj.goto(x, y)
    turtle_obj.pendown()
    turtle_obj.pencolor(color)
    turtle_obj.fillcolor(color)
    turtle_obj.begin_fill()
    for _ in range(4):  
        turtle_obj.forward(size)  
        turtle_obj.left(90)
    turtle_obj.end_fill()
    turtle_obj.penup()

def draw_cirle(turtle_obj, x, y, radius, color):
    turtle_obj.penup()
    turtle_obj.goto(x, y)
    turtle_obj.pendown()
    turtle_obj.pencolor(color)
    turtle_obj.pencolor(color)
    turtle_obj.fillcolor(color)
    turtle_obj.begin_fill()
    turtle_obj.circle(radius)
    turtle_obj.end_fill()
    turtle_obj.penup()

def draw_star(turtle_obj, x, y, size, color):
    turtle_obj.penup()
    turtle_obj.goto(x, y)
    turtle_obj.pendown()
    turtle_obj.pencolor(color)
    turtle_obj.fillcolor(color)
    turtle_obj.begin_fill()
    for _ in range(5):
        turtle_obj.forward(size)
        turtle_obj.right(120)
        turtle_obj.forward(size)
        turtle_obj.right(72 - 120)
    turtle_obj.end_fill()
    turtle_obj.penup()

def draw_triangle(turtle_obj, x, y, size, color):
    turtle_obj.penup()
    turtle_obj.goto(x, y)
    turtle_obj.pendown()
    turtle_obj.pencolor(color)
    turtle_obj.fillcolor(color)
    turtle_obj.begin_fill()
    for _ in range(3): 
        turtle_obj.forward(size) 
        turtle_obj.right(-120) 
    turtle_obj.end_fill()
    turtle_obj.penup()

def draw_diamond(turtle_obj, x, y, size, color):
    turtle_obj.penup()
    turtle_obj.goto(x, y)
    turtle_obj.pendown()
    turtle_obj.pencolor(color)
    turtle_obj.fillcolor(color)
    turtle_obj.begin_fill()
    for _ in range(2):
        turtle_obj.forward(size)
        turtle_obj.right(60)
        turtle_obj.forward(size)
        turtle_obj.right(120)
    turtle_obj.end_fill()
    turtle_obj.penup()

def draw_hexagon(turtle_obj, x, y, size, color):
    turtle_obj.penup()
    turtle_obj.goto(x, y)
    turtle_obj.pendown()
    turtle_obj.pencolor(color)
    turtle_obj.fillcolor(color)
    turtle_obj.begin_fill()
    for _ in range(6):
        turtle_obj.forward(size)
        turtle_obj.right(60)
    turtle_obj.end_fill()
    turtle_obj.penup()

def draw_octagon(turtle_obj, x, y, size, color):
    turtle_obj.penup()
    turtle_obj.goto(x, y)
    turtle_obj.pendown()
    turtle_obj.pencolor(color)
    turtle_obj.fillcolor(color)
    turtle_obj.begin_fill()
    for _ in range(8):
        turtle_obj.forward(size)
        turtle_obj.right(45)
    turtle_obj.end_fill()
    turtle_obj.penup()


def draw_pentagon(turtle_obj, x, y, size, color):
    turtle_obj.penup()
    turtle_obj.goto(x, y)
    turtle_obj.pendown()
    turtle_obj.pencolor(color)
    turtle_obj.fillcolor(color)
    turtle_obj.begin_fill()
    for _ in range(5):
        turtle_obj.forward(size)
        turtle_obj.right(72)
    turtle_obj.end_fill()
    turtle_obj.penup()

def draw_trapazoid(turtle_obj, x, y, size, color):
    turtle_obj.penup()
    turtle_obj.goto(x, y)
    turtle_obj.pendown()
    turtle_obj.pencolor(color)
    turtle_obj.fillcolor(color)
    turtle_obj.begin_fill()
    turtle_obj.forward(size)
    turtle_obj.right(60)
    turtle_obj.forward(size)
    turtle_obj.right(120)
    turtle_obj.forward(size * 2)
    turtle_obj.right(120)
    turtle_obj.forward(size)
    turtle_obj.end_fill()
    turtle_obj.penup()

def draw_colored_bg(turtle_obj, color):
    left_corner_x = int(-((SCREEN_WIDTH/2) + OUT_OF_BOUNDS_ERR))
    left_corner_y = int(-((SCREEN_HEIGHT/2) + OUT_OF_BOUNDS_ERR))
    draw_square(turtle_obj, left_corner_x, left_corner_y,
                SCREEN_WIDTH + FILL_ERR, color)

def random_font_size(text):
    # obtain font size depending on the length (word count) of the text
    if len(text.split()) <= 4:
        r_set_range = random.randint(int(len(FONT_SIZE) / 2), len(FONT_SIZE) - 1) # upper halve represents bigger font size
        font_size = FONT_SIZE[r_set_range]
    elif len(text.split()) > 4 and len(text.split()) <= 6:
        r_set_range = random.randint(0, int(len(FONT_SIZE) / 2)) # lower halve represents smaller font size
        font_size = FONT_SIZE[r_set_range]
    else:
        r_set_range = random.randint(0, 1) # smallest possible font sizes
        font_size = FONT_SIZE[r_set_range]
    return font_size

def random_font_and_emphasis():
    # obtain random font
    font = random.choice(FONT)
    emphasis = random.choice(EMPHASIS)
    return font, emphasis

def random_coordinates():
    # obtain random coordinates
    x = random.randint(int(-SCREEN_WIDTH/4), int(SCREEN_WIDTH/4.5))
    y = random.randint(int(-SCREEN_HEIGHT/4), int(SCREEN_HEIGHT/4.5))
    return x, y

# phase 1
def base_image(text, x, y, font_size):
    # set up canvas
    s = turtle.Screen()
    s.bgcolor("white")
    s.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    # choose random font and emphasis (bold or normal) on text for this image
    r_font, r_emphasis = random_font_and_emphasis() 

    tk_canvas = turtle.getcanvas() 
    tk_canvas.create_text(x, y, text=text, angle=ANGLE[0], fill='black', font=(r_font, font_size, r_emphasis)) 
    # turtle_obj.write(text, move=False, align='left', font=(font, font_size, 'bold')) 
    return s

# phase 2
def diff_text_color(text, x, y, font_size):
    # set up canvas
    s = turtle.Screen()
    s.bgcolor("white")
    s.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    r_color = random.choice(COLOR)
    r_font, r_emphasis = random_font_and_emphasis() 
    tk_canvas = turtle.getcanvas()
    tk_canvas.create_text(x, y, text=text, angle=ANGLE[0], fill=r_color, font=(r_font, font_size, r_emphasis))
    return s

# phase 3
def diff_text_and_bg_color(turtle_obj, text, x, y, font_size):
    colors = deepcopy(COLOR)
    # randomly choose background color
    r_color = random.choice(colors)
    colors.remove(r_color)
    # set up canvas
    s = turtle.Screen()
    s.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    # only way PIL will acknowledge the background color is to draw a square as the background
    draw_colored_bg(turtle_obj, r_color)
    # randomly choose text color
    r_color = random.choice(colors)
    r_font, r_emphasis = random_font_and_emphasis() 
    tk_canvas = turtle.getcanvas()
    tk_canvas.create_text(x, y, text=text, angle=ANGLE[0], fill=r_color, font=(r_font, font_size, r_emphasis))
    return s

# phase 4
def text_with_dot_noise(turtle_obj, text, x, y, font_size):
    s = turtle.Screen()
    s.bgcolor("white")
    s.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    # draw random dots in the background
    for _ in range(500):
        r_x = random.randint(int(-SCREEN_WIDTH/2), int(SCREEN_WIDTH/2))
        r_y = random.randint(int(-SCREEN_HEIGHT/2), int(SCREEN_HEIGHT/2))
        r_color = random.choice(COLOR)
        draw_cirle(turtle_obj, r_x, r_y, 5, r_color)

    r_font, r_emphasis = random_font_and_emphasis() 
    tk_canvas = turtle.getcanvas()
    tk_canvas.create_text(x, y, text=text, angle=ANGLE[0], fill='black', font=(r_font, font_size, r_emphasis))
    return s

# phase 5
def tilted_text(text, x, y, font_size):
    # set up canvas
    s = turtle.Screen()
    s.bgcolor("white")
    s.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    angles = deepcopy(ANGLE)
    angles.remove(0)

    r_angle = random.choice(angles)
    neg_angle = random.randint(0, 1)
    if neg_angle == 1:
        r_angle = -r_angle

    r_font, r_emphasis = random_font_and_emphasis() 
    tk_canvas = turtle.getcanvas()
    tk_canvas.create_text(x, y, text=text, angle=r_angle, fill='black', font=(r_font, font_size, r_emphasis))
    # turtle_obj.write(text, move=False, align='left', font=(font, font_size, 'bold'))
    return s

# phase 6
def text_in_front_of_shape(turtle_obj, text, font_size):
    r_shape = random.randint(0, 8)
    r_color = random.choice(COLOR)
    s = turtle.Screen()
    s.bgcolor("white")
    s.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    # the x and y coordinates are set to the center of the screen (trial and error approach)
    if r_shape == 0:
        draw_square(turtle_obj, -260, -260, 520, r_color)
    elif r_shape == 1:
        draw_cirle(turtle_obj, 0, -300, 300, r_color)
    elif r_shape == 2:
        draw_star(turtle_obj, 70, 150, 225, r_color)
    elif r_shape == 3:
        draw_triangle(turtle_obj, -300, -200, 600, r_color)
    elif r_shape == 4:
        draw_diamond(turtle_obj, -350, 200, 450, r_color)
    elif r_shape == 5:
        draw_hexagon(turtle_obj, -190, 320, 375, r_color) 
    elif r_shape == 6:
        draw_octagon(turtle_obj, -120, 275, 225, r_color) 
    elif r_shape == 7:
        draw_pentagon(turtle_obj, -180, 280, 375, r_color)
    elif r_shape == 8:
        draw_trapazoid(turtle_obj, -190, 210, 380, r_color)

    r_font, r_emphasis = random_font_and_emphasis() 
    tk_canvas = turtle.getcanvas()
    tk_canvas.create_text(0, 0, text=text, angle=ANGLE[0], fill='black', font=(r_font, font_size, r_emphasis))
    return s

# phase 7
def random_shapes(turtle_obj, text, x, y, font_size):
    s = turtle.Screen()
    s.bgcolor("white")
    s.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    colors = deepcopy(COLOR)
    r_shape = random.randint(0, 8)
    for _ in range(8):
        r_color = random.choice(colors)
        colors.remove(r_color)
        r_x, r_y = random_coordinates()
        # temporary solution to seperate clustering
        r_x = r_x + random.randint(75, 200)
        r_y = r_y + random.randint(75, 200)

        if r_shape == 0:
            draw_square(turtle_obj, r_x, r_y, 170, r_color)
        elif r_shape == 1:
            draw_cirle(turtle_obj, r_x, r_y, 120, r_color)
        elif r_shape == 2:
            draw_star(turtle_obj, r_x, r_y, 110, r_color)
        elif r_shape == 3:
            draw_triangle(turtle_obj, r_x, r_y, 195, r_color)
        elif r_shape == 4:
            draw_diamond(turtle_obj, r_x, r_y, 170, r_color)
        elif r_shape == 5:
            draw_hexagon(turtle_obj, r_x, r_y, 110, r_color)
        elif r_shape == 6:
            draw_octagon(turtle_obj, r_x, r_y, 100, r_color)
        elif r_shape == 7:
            draw_pentagon(turtle_obj, r_x, r_y, 110, r_color)
        elif r_shape == 8:
            draw_trapazoid(turtle_obj, r_x, r_y, 170, r_color)
        
        # choose new shape for next iteration
        r_shape = random.randint(0, 8)

    r_font, r_emphasis = random_font_and_emphasis() 
    r_color = random.choice(colors)
    tk_canvas = turtle.getcanvas()
    tk_canvas.create_text(x, y, text=text, angle=ANGLE[0], fill=r_color, font=(r_font, font_size, r_emphasis))
    return s
        

# last phase
def augment_prev_image():
    global IMG_NUM
    global PREV_IMG_NUM
    file_to_augment = DIR_LOC + FILE_NAME_SAVE_AS + str(PREV_IMG_NUM) + FORMAT_TYPE
    # read image from disk
    img = cv2.imread(file_to_augment)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # apply random augmentation
    r_aug = random.randint(0, 7) # DEBUG

    if r_aug == 0:
        aug = A.Blur(blur_limit=(7, 7), p=1) # blur augmentation
    elif r_aug == 1:
        aug = A.MultiplicativeNoise(multiplier=[0.5, 1.5], elementwise=True, per_channel=True, p=1) # noise augmentation
    elif r_aug == 2:
        aug = A.ToSepia(p=1) # dry filter augmentation
    elif r_aug == 3:
        aug = A.RandomRain(p=0.8) # "rain" augmentation
    elif r_aug == 4:
        aug = A.ChannelDropout(channel_drop_range=(1, 1), fill_value=0, p=1) # random filter augmentation 
    elif r_aug == 5:
        aug = A.ColorJitter(p=1) # color jitter augmentation
    elif r_aug == 6:
        aug = A.ShiftScaleRotate(p=1)
    elif r_aug == 7:
        aug = A.InvertImg(p=1) # invert image augmentation
    aug_img = aug(image=img)['image']
    # save the augmented image
    augmented_file = DIR_LOC + FILE_NAME_SAVE_AS + str(IMG_NUM) + FORMAT_TYPE
    cv2.imwrite(augmented_file, cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR))

    # update the global variables to keep track 
    IMG_NUM += 1
    PREV_IMG_NUM += 1

def save_turtle_canvas(screen):
    '''
    Save the turtle canvas as an image with the format specified
    '''
    global IMG_NUM
    global PREV_IMG_NUM
    PREV_IMG_NUM += 1
    screen.update()
    c = screen.getcanvas()
    file_eps = FILE_NAME_SAVE_AS + str(IMG_NUM) + ".eps"
    c.postscript(file=file_eps, colormode='color')

    img = Image.open(file_eps)
    file_jpeg = DIR_LOC + FILE_NAME_SAVE_AS + str(IMG_NUM) + FORMAT_TYPE
    img.save(file_jpeg)
    # remove the EPS file
    os.remove(file_eps)
    IMG_NUM += 1

def gen_image_from_text_pipeline(text):
    '''
    Main function that will generate 10 different and unique images from each
    text from given OCR text dataset.
    '''
    # set up turtle object
    t = turtle.Turtle(visible=False)
    t.speed(0) # fastest speed

    # random coordinates to place the text
    x, y = random_coordinates()
    
    # random font and font size
    r_font_size = random_font_size(text)

    # draw the base image
    image_1 = base_image(text, x, y, r_font_size)
    save_turtle_canvas(image_1)

    # Reset the Turtle environment
    reset_turtle_env()

    # draw the image with random text color (other than black)
    image_2 = diff_text_color(text, x, y, r_font_size)
    save_turtle_canvas(image_2)

    reset_turtle_env()

    # draw the image with random text and background color
    image_3 = diff_text_and_bg_color(t, text, x, y, r_font_size)
    save_turtle_canvas(image_3)

    reset_turtle_env()

    # draw the image with text and dot noise in the background
    image_4 = text_with_dot_noise(t, text, x, y, r_font_size)
    save_turtle_canvas(image_4)

    reset_turtle_env()

    # augment the previous image randomly
    augment_prev_image()

    # draw the image with tilted text
    image_5 = tilted_text(text, x, y, r_font_size)
    save_turtle_canvas(image_5)

    reset_turtle_env()
    
    # draw the image with text in front of a random shape (no coordinates needed since the shape and text is centered in the screen)
    image_6 = text_in_front_of_shape(t, text, r_font_size)
    save_turtle_canvas(image_6)

    reset_turtle_env()

    augment_prev_image()

    # draw the image with random shapes in the background
    image_7 = random_shapes(t, text, x, y, r_font_size)
    save_turtle_canvas(image_7)

    reset_turtle_env()

    augment_prev_image()

# ----------------------CONSOLE----------------------
def main():
    #long_test = 'The Fantastic Adventures of Captain Cosmos and the Interstellar Dare'
    #test = 'Test run'

    OCR_text_df = pd.read_csv('OCR_text_dataset.csv')

    for text in OCR_text_df['Words/Short Phrases'][:5]:
        gen_image_from_text_pipeline(text)
    kill_turtle() # terminate the turtle graphics window

if __name__ == "__main__":
    main()