import tkinter as tk
from tkinter import Label, filedialog, messagebox
import random
import cv2
from PIL import Image, ImageTk


def update_position(event):
    x, y = event.x, event.y
    position_label.config(text=f'X: {x} Y: {y}')


def load_media():
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("Media Files", ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif", '*.mp4', '*.avi'])])
    except Exception:
        print("OOF")

    if file_path:
        try:
            display_image(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
    else:
        messagebox.showinfo("No file selected", "Please select an image file.")


def display_image(file_path):
    if file_path.split('.')[-1] in ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif"]:
        image = Image.open(file_path)
        photo = ImageTk.PhotoImage(image)

        canvas.config(width=photo.width(), height=photo.height())
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo
    else:
        cap = cv2.VideoCapture(file_path)
        frame_no = int(random.random()*3000)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)

        canvas.config(width=cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo


def create_app():
    global canvas, position_label

    root = tk.Tk()
    root.title("Image Cursor Position App")

    load_button = tk.Button(root, text="Load Media", command=load_media)
    load_button.pack()

    canvas = tk.Canvas(root)
    canvas.pack()

    position_label = Label(root, text="X: 0 Y: 0", bg='white')
    position_label.pack()
    position_label.place(relx=1.0, rely=0.0, anchor='ne')

    canvas.bind('<Motion>', update_position)

    root.mainloop()


if __name__ == "__main__":
    create_app()
