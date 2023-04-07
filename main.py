import tkinter as tk
from os import name
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import torch
import cv2
import numpy as np
import sys

sys.path.append('./yolov5')
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./train_model/best.pt', force_reload=True)


# img = cv2.imread('./data/road876.png')
# results = model(img)
# print(results)
# cv2.imshow("212", cv2.cvtColor(np.squeeze(results.render()), cv2.COLOR_BGR2RGB))


class TrafficLightApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Detect Traffic Light")
        self.geometry("1346x805")

        self.init_ui()
        self.photo = ''
        self.video = ''
        self.live = ''
        self.file_path = ''

    def init_ui(self):
        self.label1 = tk.Label(self, text="Detect Traffic Light", font=("Microsoft Sans Serif", 48))
        self.label1.pack(pady=20)

        self.panel1 = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.panel1.place(x=46, y=141, width=890, height=419)
        self.image_label = tk.Label(self.panel1)
        self.image_label.pack(padx=5, pady=5)

        self.panel2 = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.panel2.place(x=46, y=573, width=1255, height=220)

        self.label3 = tk.Label(self.panel2, text="Logs:", font=("Microsoft Sans Serif", 12))
        self.label3.pack(padx=5, pady=5, anchor=tk.W)

        self.richTextBox1 = tk.Text(self.panel2, wrap=tk.WORD)
        self.richTextBox1.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        self.richTextBox1.config(state=tk.DISABLED)

        self.panel3 = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.panel3.place(x=952, y=141, width=349, height=419)

        self.label2 = tk.Label(self.panel3, text="Control", font=("Microsoft Sans Serif", 20))
        self.label2.pack(pady=10)

        self.label6 = tk.Label(self.panel3, text="Choose option:", font=("Microsoft Sans Serif", 16))
        self.label6.pack(fill=tk.X, padx=5, pady=5)

        self.options_frame = tk.Frame(self.panel3)
        self.options_frame.pack(fill=tk.X, padx=5, pady=5)

        self.var_option = tk.StringVar()
        self.var_option.set("identification")

        self.rBtn_identification = tk.Radiobutton(self.options_frame, text="Identification", variable=self.var_option,
                                                  value="identification")
        self.rBtn_identification.pack(side=tk.LEFT, padx=5, pady=5)

        self.rBtn_classify = tk.Radiobutton(self.options_frame, text="Classify", variable=self.var_option,
                                            value="classify")
        self.rBtn_classify.pack(side=tk.LEFT, padx=5, pady=5)

        self.label4 = tk.Label(self.panel3, text="Choose type:", font=("Microsoft Sans Serif", 12))
        self.label4.pack(padx=5, pady=5, anchor=tk.W)

        self.cb_type = ttk.Combobox(self.panel3, state="readonly", values=["Image", "Video", "Livestream", "Camera"],
                                    font=("Microsoft Sans Serif", 12))
        self.cb_type.current(0)
        self.cb_type.pack(fill=tk.X, padx=5, pady=5)
        self.cb_type.bind("<<ComboboxSelected>>", self.on_cb_type_change)

        self.btn_image = tk.Button(self.panel3, text="Upload Image", command=self.open_image)
        self.btn_image.pack(fill=tk.X, padx=5, pady=5)

        self.btn_video = tk.Button(self.panel3, text="Upload Video", state=tk.DISABLED)
        self.btn_video.pack(fill=tk.X, padx=5, pady=5)

        self.btn_live = tk.Button(self.panel3, text="Live Video", state=tk.DISABLED)
        self.btn_live.pack(fill=tk.X, padx=5, pady=5)

        self.btn_camera = tk.Button(self.panel3, text="Camera", state=tk.DISABLED)
        self.btn_camera.pack(fill=tk.X, padx=5, pady=5)
        self.button_start = tk.Button(self.panel3, text="Start", command=self.start_processing)
        self.button_start.pack(fill=tk.X, padx=5, pady=20)

    def start_processing(self):
        option = self.var_option.get()
        media_type = self.cb_type.get()
        if media_type == "Image":
            self.process_image(option)
        elif media_type == "Video":
            self.process_video(option)
        elif media_type == "Livestream":
            self.process_livestream(option)
        else:  # media_type == "Camera"
            self.process_camera(option)

    def process_image(self, option):
        img = cv2.imread(self.file_path)
        results = model(img)
        img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(np.squeeze(results.render()), cv2.COLOR_BGR2RGB)))
        self.image_label.config(image=img)
        self.image_label.image = img
        self.richTextBox1.config(state=tk.NORMAL)
        self.richTextBox1.insert(tk.END, results)
        self.richTextBox1.config(state=tk.DISABLED)

    def process_video(self, option):
        self.btn_video.config(state=tk.NORMAL)

    def process_livestream(self, option):
        pass  # Implement the livestream processing code here

    def process_camera(self, option):
        pass  # Implement the camera processing code here

    def on_cb_type_change(self, event):
        current_selection = self.cb_type.get()
        btn = ''
        if current_selection == "Image":
            btn = self.btn_image
        elif current_selection == "Video":
            btn = self.btn_video
        elif current_selection == "Livestream":
            btn = self.btn_live
        else:  # media_type == "Camera"
            btn = self.btn_camera
        self.toggle_btn(btn)

    def toggle_btn(self, btn_active):
        self.btn_image.config(state=tk.DISABLED)
        self.btn_video.config(state=tk.DISABLED)
        self.btn_live.config(state=tk.DISABLED)
        self.btn_camera.config(state=tk.DISABLED)
        btn_active.config(state=tk.NORMAL)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        image = Image.open(file_path)
        self.file_path = file_path
        self.photo = cv2.imread(file_path)
        image.thumbnail((880, 410))
        tkinter_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=tkinter_image)
        self.image_label.image = tkinter_image


app = TrafficLightApp()
app.mainloop()
