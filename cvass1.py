import cv2

#Group members:
#1. 23L-3030  - Rayan Ahmad Khan
#2. 23L-0813 - Muhammad Usman Saboor

# LOAD IMAGE

image_path = "test.png"
img_original = cv2.imread(image_path)

if img_original is None:
    print("Error loading image.")
    exit()

# RESIZE IMAGE TO FIT SCREEN

max_width = 900
max_height = 700

h0, w0 = img_original.shape[:2]

scale_w = max_width / w0
scale_h = max_height / h0

scale = min(scale_w, scale_h, 1) 

new_w = int(w0 * scale)
new_h = int(h0 * scale)

img = cv2.resize(img_original, (new_w, new_h))

clone = img.copy()

points = []

print("Click in this order:")
print("1. Top of A4")
print("2. Bottom of A4")
print("3. Top of your head")
print("4. Bottom of your feet")


# MOUSE CLICK FUNCTION

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 6, (0, 0, 255), -1)
        cv2.imshow("Image", img)


# SHOW IMAGE

cv2.imshow("Image", img)
cv2.setMouseCallback("Image", click_event)

while True:
    key = cv2.waitKey(1)
    if key == 27 or len(points) == 4:
        break

cv2.destroyAllWindows()

if len(points) != 4:
    print("You must select exactly 4 points.")
    exit()

# CALCULATIONS

a4_pixel_height = abs(points[1][1] - points[0][1])
person_pixel_height = abs(points[3][1] - points[2][1])

A4_REAL_HEIGHT = 29.7  # cm

height_cm = (person_pixel_height / a4_pixel_height) * A4_REAL_HEIGHT

print(f"\nEstimated Height: {height_cm:.2f} cm")

# RESULT

result_img = clone.copy()

cv2.putText(result_img,
            f"Estimated Height: {height_cm:.2f} cm",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2)

cv2.imshow("Result", result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
