import tkinter as tk
from tkinter import ttk, messagebox
from ObjectDetection import detectObject
import os

# Fetching all video files in the Media folder.
def fetchVideos(count = 1, videos = [], directory = "Media"):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and f.endswith('.mp4'):
            videos.append(f"{count}: {filename[:-4]}")
        count += 1
    return videos

class ImageDetection:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Detection")
        self.createWidgets()

    def createWidgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
  
        # Video Mode
        ttk.Label(frame, text="Video Mode:").grid(row=0, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar()
        mode_options = ["1: Camera", "2: Video File"]
        self.mode_combobox = ttk.Combobox(frame, textvariable=self.mode_var, values=mode_options, state="readonly")
        self.mode_combobox.grid(row=0, column=1, sticky=tk.E)
        self.mode_combobox.current(0)

        # People only Checkbox
        ttk.Label(frame, text="People Only: ").grid(row=1, column=0, sticky=tk.W)
        self.people_var = tk.BooleanVar(value=False)
        self.people_checkbutton = ttk.Checkbutton(frame)
        self.people_checkbutton.config(variable=self.people_var)
        self.people_checkbutton.grid(row=1, column=1, columnspan=2, sticky=tk.W)

        # Video File Option
        self.file_label = ttk.Label(frame, text="Video File:")
        self.file_var = tk.StringVar()
        file_options = fetchVideos()
        self.file_combobox = ttk.Combobox(frame, values=file_options, textvariable=self.file_var, state="readonly")

        # Start Button
        tk.Button(frame, text="Start", command=self.startAlgorithm, bg='green', activebackground='blue').grid(row=12, column=0, columnspan=2, sticky=(tk.W, tk.E))
        self.mode_combobox.bind("<<ComboboxSelected>>", self.updateFileComboboxVisibility)    

    def updateFileComboboxVisibility(self, event):
        if self.mode_var.get().startswith("2:"):
            self.file_label.grid(row=7, column=0, sticky=tk.W)
            self.file_combobox.grid(row=7, column=1, sticky=tk.E)
            self.file_combobox.current(0)
        else:
            self.file_label.grid_forget()
            self.file_combobox.grid_forget()

    def startAlgorithm(self):
        try:
            mode = int(self.mode_var.get()[0])
            peopleOnly = self.people_var.get()
            videoFile = f"{self.file_var.get()[3::]}.mp4" if mode == 2 else None
            detectObject(mode, peopleOnly, videoFile)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = ImageDetection(root)
    root.mainloop()

if __name__ == "__main__":
    main()