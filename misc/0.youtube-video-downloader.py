# # # import tkinter as tk
# # # from tkinter import filedialog, messagebox
# # # from pytube import YouTube
# # #
# # # class YouTubeDownloader:
# # #     def __init__(self, root):
# # #         self.root = root
# # #         self.root.title("YouTube Video Downloader")
# # #         self.root.geometry("400x200")
# # #
# # #         self.create_widgets()
# # #
# # #     def create_widgets(self):
# # #         self.url_label = tk.Label(self.root, text="YouTube URL:")
# # #         self.url_label.pack(pady=10)
# # #
# # #         self.url_entry = tk.Entry(self.root, width=50)
# # #         self.url_entry.pack(pady=5)
# # #
# # #         self.download_button = tk.Button(self.root, text="Download", command=self.download_video)
# # #         self.download_button.pack(pady=20)
# # #
# # #     def download_video(self):
# # #         url = self.url_entry.get()
# # #         if not url:
# # #             messagebox.showerror("Error", "Please enter a YouTube URL")
# # #             return
# # #
# # #         try:
# # #             yt = YouTube(url)
# # #             stream = yt.streams.get_highest_resolution()
# # #
# # #             save_path = filedialog.askdirectory()
# # #             if not save_path:
# # #                 return
# # #
# # #             stream.download(save_path)
# # #             messagebox.showinfo("Success", f"Downloaded '{yt.title}' successfully!")
# # #         except Exception as e:
# # #             messagebox.showerror("Error", f"Failed to download video: {e}")
# # #
# # # if __name__ == "__main__":
# # #     root = tk.Tk()
# # #     app = YouTubeDownloader(root)
# # #     root.mainloop()
# #
# #
# #
# # import tkinter as tk
# # from tkinter import filedialog, messagebox
# # from pytube import YouTube
# #
# # class YouTubeDownloader:
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title("YouTube Video Downloader")
# #         self.root.geometry("400x300")
# #
# #         self.create_widgets()
# #
# #     def create_widgets(self):
# #         self.url_label = tk.Label(self.root, text="YouTube URL:")
# #         self.url_label.pack(pady=10)
# #
# #         self.url_entry = tk.Entry(self.root, width=50)
# #         self.url_entry.pack(pady=5)
# #
# #         self.quality_label = tk.Label(self.root, text="Select Quality:")
# #         self.quality_label.pack(pady=10)
# #
# #         self.quality_options = ["Highest Resolution", "Lowest Resolution", "Only Audio"]
# #         self.quality_var = tk.StringVar(value=self.quality_options[0])
# #         self.quality_menu = tk.OptionMenu(self.root, self.quality_var, *self.quality_options)
# #         self.quality_menu.pack(pady=5)
# #
# #         self.download_button = tk.Button(self.root, text="Download", command=self.download_video)
# #         self.download_button.pack(pady=20)
# #
# #     def download_video(self):
# #         url = self.url_entry.get()
# #         if not url:
# #             messagebox.showerror("Error", "Please enter a YouTube URL")
# #             return
# #
# #         try:
# #             yt = YouTube(url)
# #             quality = self.quality_var.get()
# #
# #             if quality == "Highest Resolution":
# #                 stream = yt.streams.get_highest_resolution()
# #             elif quality == "Lowest Resolution":
# #                 stream = yt.streams.get_lowest_resolution()
# #             elif quality == "Only Audio":
# #                 stream = yt.streams.filter(only_audio=True).first()
# #             else:
# #                 messagebox.showerror("Error", "Invalid quality selection")
# #                 return
# #
# #             save_path = filedialog.askdirectory()
# #             if not save_path:
# #                 return
# #
# #             stream.download(save_path)
# #             messagebox.showinfo("Success", f"Downloaded '{yt.title}' successfully!")
# #         except Exception as e:
# #             messagebox.showerror("Error", f"Failed to download video: {e}")
# #
# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     app = YouTubeDownloader(root)
# #     root.mainloop()
#
#
# import tkinter as tk
# from tkinter import filedialog, messagebox
# from tkinter import ttk
# from pytube import YouTube
# import threading
#
# class YouTubeDownloader:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("YouTube Video Downloader")
#         self.root.geometry("400x350")
#
#         self.create_widgets()
#
#     def create_widgets(self):
#         self.url_label = tk.Label(self.root, text="YouTube URL:")
#         self.url_label.pack(pady=10)
#
#         self.url_entry = tk.Entry(self.root, width=50)
#         self.url_entry.pack(pady=5)
#
#         self.quality_label = tk.Label(self.root, text="Select Quality:")
#         self.quality_label.pack(pady=10)
#
#         self.quality_options = ["Highest Resolution", "Lowest Resolution", "Only Audio"]
#         self.quality_var = tk.StringVar(value=self.quality_options[0])
#         self.quality_menu = tk.OptionMenu(self.root, self.quality_var, *self.quality_options)
#         self.quality_menu.pack(pady=5)
#
#         self.download_button = tk.Button(self.root, text="Download", command=self.download_video)
#         self.download_button.pack(pady=20)
#
#         self.progress = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='determinate')
#         self.progress.pack(pady=10)
#
#     def download_video(self):
#         url = self.url_entry.get()
#         if not url:
#             messagebox.showerror("Error", "Please enter a YouTube URL")
#             return
#
#         threading.Thread(target=self.start_download, args=(url,)).start()
#
#     def start_download(self, url):
#         try:
#             yt = YouTube(url, on_progress_callback=self.progress_callback)
#             quality = self.quality_var.get()
#
#             if quality == "Highest Resolution":
#                 stream = yt.streams.get_highest_resolution()
#             elif quality == "Lowest Resolution":
#                 stream = yt.streams.get_lowest_resolution()
#             elif quality == "Only Audio":
#                 stream = yt.streams.filter(only_audio=True).first()
#             else:
#                 messagebox.showerror("Error", "Invalid quality selection")
#                 return
#
#             save_path = filedialog.askdirectory()
#             if not save_path:
#                 return
#
#             self.progress['value'] = 0
#             self.progress['maximum'] = 100
#             stream.download(save_path)
#             messagebox.showinfo("Success", f"Downloaded '{yt.title}' successfully!")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to download video: {e}")
#
#     def progress_callback(self, stream, chunk, bytes_remaining):
#         total_size = stream.filesize
#         bytes_downloaded = total_size - bytes_remaining
#         percentage_of_completion = bytes_downloaded / total_size * 100
#         self.progress['value'] = percentage_of_completion
#         self.root.update_idletasks()
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = YouTubeDownloader(root)
#     root.mainloop()


import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pytube import YouTube
import threading

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("400x350")

        self.create_widgets()

    def create_widgets(self):
        self.url_label = tk.Label(self.root, text="YouTube URL:")
        self.url_label.pack(pady=10)

        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.pack(pady=5)

        self.quality_label = tk.Label(self.root, text="Select Quality:")
        self.quality_label.pack(pady=10)

        self.quality_options = ["Highest Resolution", "Lowest Resolution", "Only Audio"]
        self.quality_var = tk.StringVar(value=self.quality_options[0])
        self.quality_menu = tk.OptionMenu(self.root, self.quality_var, *self.quality_options)
        self.quality_menu.pack(pady=5)

        self.download_button = tk.Button(self.root, text="Download", command=self.download_video)
        self.download_button.pack(pady=20)

        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(pady=10)

    def download_video(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return

        threading.Thread(target=self.start_download, args=(url,)).start()

    def start_download(self, url):
        try:
            yt = YouTube(url, on_progress_callback=self.progress_callback)
            quality = self.quality_var.get()

            if quality == "Highest Resolution":
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            elif quality == "Lowest Resolution":
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()
            elif quality == "Only Audio":
                stream = yt.streams.filter(only_audio=True).first()
            else:
                messagebox.showerror("Error", "Invalid quality selection")
                return

            save_path = filedialog.askdirectory()
            if not save_path:
                return

            self.progress['value'] = 0
            self.progress['maximum'] = 100
            stream.download(save_path)
            messagebox.showinfo("Success", f"Downloaded '{yt.title}' successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download video: {e}")

    def progress_callback(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        self.progress['value'] = percentage_of_completion
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
