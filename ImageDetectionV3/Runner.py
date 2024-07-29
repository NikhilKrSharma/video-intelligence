import tkinter as tk
from tkinter import ttk, messagebox
from TrackerModules.SortDetection import detectObject
import os

# Fetching all video files in the Media folder.
def fetchVideos(count = 1, videos = [], directory = "ImageDetectionV3/Media"):
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

        # Show Checkbox
        self.view_checkbutton = ttk.Checkbutton(frame)
        self.view_label = ttk.Label(frame, text="Show Video:")
        self.view_var = tk.BooleanVar(value=True)
        self.view_checkbutton.config(variable=self.view_var)
        self.view_label.grid(row=1, column=0, sticky=tk.W)
        self.view_checkbutton.grid(row=1, column=1, sticky=tk.W)

        # Save Checkbox
        self.save_checkbutton = ttk.Checkbutton(frame)
        self.save_label = ttk.Label(frame, text="Save Video: ")
        self.save_var = tk.BooleanVar(value=False)
        self.save_checkbutton.config(variable=self.save_var)
        self.save_label.grid(row=2, column=0, sticky=tk.W)
        self.save_checkbutton.grid(row=2, column=1,sticky=tk.W)

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
            self.file_label.grid(row=3, column=0, sticky=tk.W)
            self.file_combobox.grid(row=3, column=1, sticky=tk.E)
            self.file_combobox.current(0)
        else:
            self.file_label.grid_forget()
            self.file_combobox.grid_forget()

    def startAlgorithm(self):
        try:
            mode = int(self.mode_var.get()[0])
            view = self.view_var.get()
            save = self.save_var.get()
            videoFile = f"{self.file_var.get()[3::]}.mp4" if mode == 2 else None
            detectObject(mode, videoFile, save, view)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = ImageDetection(root)
    root.mainloop()

if __name__ == "__main__":
    main()