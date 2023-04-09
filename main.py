import tkinter as tk
from os import name
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import torch
import cv2
import numpy as np
import sys
from datetime import datetime

sys.path.append('./yolov5')
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./train_model/tracffict01.pt', force_reload=True)


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
        self.video_file_path = ''

    def init_ui(self):
        self.label1 = tk.Label(self, text="Detect Traffic Light", font=("Microsoft Sans Serif", 48))
        self.label1.pack(pady=20)

        self.panel1 = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.panel1.place(x=46, y=141, width=890, height=419)
        self.preview = tk.Canvas(self.panel1, width=890, height=419, bg="white")
        self.preview.pack(padx=5, pady=5)

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

        self.btn_video = tk.Button(self.panel3, text="Upload Video", state=tk.DISABLED, command=self.open_video)
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
        image = Image.fromarray(cv2.cvtColor(np.squeeze(results.render()), cv2.COLOR_BGR2RGB))
        img = ImageTk.PhotoImage(image)
        # self.image_label.config(image=img)
        # self.image_label.image = img
        # self.richTextBox1.config(state=tk.NORMAL)
        # self.richTextBox1.insert(tk.END, results)
        # self.richTextBox1.config(state=tk.DISABLED)

        x_center = (self.preview.winfo_width() - image.width) // 2
        y_center = (self.preview.winfo_height() - image.height) // 2

        self.preview.delete("all")
        self.preview.create_image(x_center, y_center, image=img, anchor=tk.NW)

        self.preview.image = img

        self.richTextBox1.config(state=tk.NORMAL)
        self.richTextBox1.insert(tk.END, results)
        self.richTextBox1.config(state=tk.DISABLED)

    def process_video(self, option):
        self.btn_video.config(state=tk.NORMAL)
        self.cap = cv2.VideoCapture(self.video_file_path)
        self.update_preview()
        # cap = cv2.VideoCapture(self.video_file_path)
        # while cap.isOpened():
        #     ret, frame = cap.read()
        #     if not ret:
        #         break
        #
        #     # Convert frame to PIL Image and pass it to the YOLO model
        #     pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        #     results = model(pil_frame)
        #
        #     # Draw the detections on the frame
        #     for *xyxy, conf, cls in results.xyxy[0].cpu().numpy():
        #         x1, y1, x2, y2 = map(int, xyxy)
        #         label = model.names[int(cls)]
        #         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #         cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        #
        #     # Show the frame with detections
        #     cv2.imshow('Detections', frame)
        #
        #     # Break the loop if 'q' key is pressed
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break

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

        x_center = (self.preview.winfo_width() - image.width) // 2
        y_center = (self.preview.winfo_height() - image.height) // 2

        self.preview.delete("all")
        self.preview.create_image(x_center, y_center, image=tkinter_image, anchor=tk.NW)
        self.preview.image = tkinter_image

    def open_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
        self.video_file_path = file_path
        # Read the first frame of the video\

        cap = cv2.VideoCapture(file_path)
        ret, frame = cap.read()
        cap.release()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image.thumbnail((880, 410))
            tkinter_image = ImageTk.PhotoImage(image)

            x_center = (self.preview.winfo_width() - image.width) // 2
            y_center = (self.preview.winfo_height() - image.height) // 2

            self.preview.delete("all")
            self.preview.create_image(x_center, y_center, image=tkinter_image, anchor=tk.NW)
            self.preview.image = tkinter_image

    def open_webcam(self):
        cap = cv2.VideoCapture(0)  # 0 is the default webcam index

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # You can perform your desired operations on the frame here

            cv2.imshow('Webcam', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def update_preview(self):
        if not self.cap:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            return

        pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        results = model(pil_frame)
        label = ''
        # Draw the detections on the frame
        for *xyxy, conf, cls in results.xyxy[0].cpu().numpy():
            x1, y1, x2, y2 = map(int, xyxy)
            label = model.names[int(cls)]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        tkinter_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

        x_center = (self.preview.winfo_width() - tkinter_image.width()) // 2
        y_center = (self.preview.winfo_height() - tkinter_image.height()) // 2

        self.preview.delete("all")
        self.preview.create_image(x_center, y_center, image=tkinter_image, anchor=tk.NW)
        self.preview.image = tkinter_image

        if label != '':
            self.richTextBox1.config(state=tk.NORMAL)
            self.richTextBox1.insert(tk.END,
                                     "Detect " + label + " at " + datetime.now().strftime("%H:%M:%S %d/%m/%Y") + "\n")
            self.richTextBox1.config(state=tk.DISABLED)

        self.preview.after(10, self.update_preview)


app = TrafficLightApp()
app.mainloop()
