import cv2
import torch
import numpy as np
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
import pathlib
import threading
from PIL import Image, ImageTk

# Temporarily adjust pathlib for Windows compatibility
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

class HelmetDetectionApp:
    def __init__(self, master):
        self.master = master
        self.setup_ui()
        self.center_window(800, 600)
        self.model = None
        self.cap = None
        self.thread = None

    def setup_ui(self):
        self.master.title("Helmet Detection")
        
        self.entPathTrain = Entry(self.master, width=50)
        self.entPathTrain.grid(row=0, column=0, padx=5, pady=5)

        self.btnBrowseTrain = Button(self.master, text="Browse", command=self.browse_train)
        self.btnBrowseTrain.grid(row=0, column=1, padx=5, pady=5)

        self.btnRunDetection = Button(self.master, text="Run Helmet Detection", command=self.run_helmet_detection)
        self.btnRunDetection.grid(row=1, columnspan=2, padx=5, pady=5)

        self.btnExit = Button(self.master, text="Exit", command=self.on_closing)
        self.btnExit.grid(row=0, column=2, padx=5, pady=5)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def browse_train(self):
        self.entPathTrain.delete(0, END)
        filetypes = (('All files', '*.*'), ('Pdf files', '*.pdf'))
        filename = fd.askopenfilename(title='Chọn file để mở', initialdir=r'C:\Users\User\Desktop', filetypes=filetypes)
        self.entPathTrain.insert(0, filename)

    def run_helmet_detection(self):
        path_train = self.entPathTrain.get()
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path_train, force_reload=True)
        self.cap = cv2.VideoCapture(0)

        # Set video capture properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1020)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

        # Start a separate thread for video display
        self.thread = threading.Thread(target=self.display_video)
        self.thread.daemon = True
        self.thread.start()

        self.center_window(1020, 640)

    def display_video(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (1020, 640))
            results = self.model(frame)
            frame = np.squeeze(results.render())
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            panel = Label(self.master, image=imgtk)
            panel.image = imgtk
            panel.grid(row=2, columnspan=2, padx=10, pady=10)

            key = cv2.waitKey(1)
            if key == 27:
                break

    def on_closing(self):
        if messagebox.askokcancel("Thoát", "Bạn có muốn thoát chương trình không?"):
            if self.cap:
                self.cap.release()
            self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    app = HelmetDetectionApp(root)
    root.mainloop()
