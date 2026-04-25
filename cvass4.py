import cv2 
import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

class HoughApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hough Transform GUI - Assignment")

        self.image = None
        self.processed_image = None

        Button(root, text="Load Image", command=self.load_image).pack(pady=5)

        self.angle = Scale(root, from_=1, to=180, orient=HORIZONTAL, label="Line Angles")
        self.angle.set(1)
        self.angle.pack()

        self.threshold = Scale(root, from_=10, to=200, orient=HORIZONTAL, label="Line Pixels (Threshold)")
        self.threshold.set(100)
        self.threshold.pack()

        self.minLineLength = Scale(root, from_=10, to=300, orient=HORIZONTAL, label="Delta Length")
        self.minLineLength.set(50)
        self.minLineLength.pack()

        self.maxLineGap = Scale(root, from_=1, to=50, orient=HORIZONTAL, label="Connect Distance")
        self.maxLineGap.set(10)
        self.maxLineGap.pack()

        self.segment = Scale(root, from_=1, to=100, orient=HORIZONTAL, label="Segment Pixels/Length")
        self.segment.set(20)
        self.segment.pack()

        Button(root, text="Apply Hough Transform", command=self.apply_hough).pack(pady=5)

        self.info = Label(root, text="Load an image, set parameters, then apply Hough Transform.")
        self.info.pack()

        self.panel = Label(root)
        self.panel.pack(pady=8)

    def load_image(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        self.image = cv2.imread(path)
        if self.image is None:
            messagebox.showerror("Load Error", "Could not read the selected image file.")
            return

        self.display_image(self.image)
        self.info.config(text="Image loaded. You can now adjust parameters and apply transform.")

    def apply_hough(self):
        if self.image is None:
            messagebox.showwarning("No Image", "Please load an image first.")
            return

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(blur, 50, 150)

        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.deg2rad(max(1, self.angle.get())),
            threshold=self.threshold.get(),
            minLineLength=self.minLineLength.get(),
            maxLineGap=self.maxLineGap.get()
        )

        result = self.image.copy()

        if lines is not None:
            count = 0
            for line in lines:
                x1, y1, x2, y2 = line[0]

                length = np.hypot(x2 - x1, y2 - y1)

                if length >= self.segment.get():
                    cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    count += 1

            self.info.config(text=f"Detected and drew {count} line segments.")
        else:
            self.info.config(text="No lines detected with current parameters.")

        self.display_image(result)
        self.processed_image = result

    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)

        max_w, max_h = 500, 400
        w, h = img.size
        scale = min(max_w / w, max_h / h)
        new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
        img = img.resize(new_size)

        imgtk = ImageTk.PhotoImage(img)
        self.panel.imgtk = imgtk
        self.panel.config(image=imgtk)

root = Tk()
app = HoughApp(root)
root.mainloop()