import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog

class ImageDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Downloader")
        width= root.winfo_screenwidth()
        height= root.winfo_screenheight()
        self.root.geometry("%dx%d" % (width, height))
        self.root.geometry("300x200")
        # self.root.attributes('-fullscreen',False)

        self.url_label = tk.Label(root, text="Enter the URL:")
        self.url_label.pack()
       

        self.url_entry = tk.Entry(root)
        self.url_entry.pack()

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.browse_button.pack()

        self.download_button = tk.Button(root, text="Download Images", command=self.download_images)
        self.download_button.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

    def browse_folder(self):
        self.save_folder = filedialog.askdirectory(title="Select folder to save images")

    def download_images(self):
        url = self.url_entry.get()
        if url and hasattr(self, 'save_folder'):
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                img_tags = soup.find_all('img')

                for img_tag in img_tags:
                    img_url = img_tag.get('src')
                    if img_url and not img_url.startswith('data:'):
                        img_response = requests.get(img_url)
                        if img_response.status_code == 200:
                            img_name = os.path.basename(img_url)
                            img_path = os.path.join(self.save_folder, img_name)
                            with open(img_path, 'wb') as img_file:
                                img_file.write(img_response.content)
                            self.status_label.config(text=f"Downloaded: {img_name}")
                            self.root.update_idletasks()  # Update the GUI

                self.status_label.config(text="All images downloaded successfully!")
            else:
                self.status_label.config(text="Failed to fetch URL content.")
        else:
            self.status_label.config(text="URL or save folder not provided.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDownloaderApp(root)
    root.mainloop()
