import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

image = None

def load_image():
    global image
    path = filedialog.askopenfilename()
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    show_image(image)

def show_image(img):
    img = Image.fromarray(img)
    img = img.resize((300,300))
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.image = img

def quantize():
    global image
    bits = int(bits_entry.get())
    method = method_var.get()

    k = 8 - bits
    mask_and = 255 << k
    mask_or = (1 << k) - 1

    img = image.copy()

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            p = img[i,j]

            if method == "lower":
                img[i,j] = p & mask_and

            elif method == "higher":
                img[i,j] = p | mask_or

            elif method == "middle":
                bin_size = 2**k
                img[i,j] = (p//bin_size)*bin_size + bin_size//2

    show_image(img)

def igs():
    global image
    bits = int(bits_entry.get())
    k = 8 - bits
    bin_size = 2**k

    img = image.copy()

    noise = np.random.randint(0, bin_size, img.shape)
    img = img + noise
    img = np.clip(img,0,255)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i,j] = (img[i,j]//bin_size)*bin_size

    show_image(img)

root = tk.Tk()
root.title("Gray Level Quantization")

btn = tk.Button(root,text="Load Image",command=load_image)
btn.pack()

tk.Label(root,text="Bits").pack()
bits_entry = tk.Entry(root)
bits_entry.insert(0,"5")
bits_entry.pack()

method_var = tk.StringVar(value="lower")

tk.Radiobutton(root,text="Lower",variable=method_var,value="lower").pack()
tk.Radiobutton(root,text="Higher",variable=method_var,value="higher").pack()
tk.Radiobutton(root,text="Middle",variable=method_var,value="middle").pack()

tk.Button(root,text="Apply Quantization",command=quantize).pack()
tk.Button(root,text="Apply IGS",command=igs).pack()

panel = tk.Label(root)
panel.pack()

root.mainloop()