import tkinter as tk
from PIL import Image, ImageTk
import math


# ------------------------------------------------------------
# Function: manual_rotate
# Purpose:
#   Rotates an image manually using rotation transformation.
#   No built-in rotation functions are used.
#
# Parameters:
#   image  -> input image
#   angle  -> rotation angle given by user
#
# Returns:
#   rotated image
# ------------------------------------------------------------
def manual_rotate(image, angle):

    width, height = image.size

    # creating empty image for result
    rotated = Image.new("RGB", (width, height))

    pixels = image.load()
    new_pixels = rotated.load()

    # converting angle to radians
    theta = math.radians(angle)

    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)

    # center of image
    cx = width // 2
    cy = height // 2

    for x in range(width):
        for y in range(height):

            # shifting origin to center
            xt = x - cx
            yt = y - cy

            # applying rotation
            src_x = int(xt * cos_theta + yt * sin_theta + cx)
            src_y = int(-xt * sin_theta + yt * cos_theta + cy)

            # edge cases checking
            if 0 <= src_x < width and 0 <= src_y < height:
                new_pixels[x, y] = pixels[src_x, src_y]

    return rotated


# ------------------------------------------------------------
# Function: rotate_image
# Purpose:
#   Gets user input angle and displays rotated image
# ------------------------------------------------------------
def rotate_image():

    global img

    angle = float(angle_entry.get())

    rotated = manual_rotate(img, angle)

    display_image(rotated)


# ------------------------------------------------------------
# Function: display_image
# Purpose:
#   Displays image on GUI canvas
# ------------------------------------------------------------
def display_image(image):

    global img_tk

    img_tk = ImageTk.PhotoImage(image)

    canvas.delete("all")
    canvas.create_image(250, 250, image=img_tk)


# ------------------------------------------------------------
# Function: load_image
# Purpose:
#   Loads image from file
# ------------------------------------------------------------
def load_image():

    global img

    img = Image.open("test.png")  # put your image name here
    img = img.resize((500, 500))
    display_image(img)


# ---------------- GUI ----------------

window = tk.Tk()
window.title("Image Rotation (Manual Algorithm)")

canvas = tk.Canvas(window, width=750, height=500, bg="black")
canvas.pack()

angle_label = tk.Label(window, text="Enter rotation angle (0-360):")
angle_label.pack()

angle_entry = tk.Entry(window)
angle_entry.pack()

rotate_button = tk.Button(window, text="Rotate Image", command=rotate_image)
rotate_button.pack()

load_button = tk.Button(window, text="Load Image", command=load_image)
load_button.pack()

window.mainloop()