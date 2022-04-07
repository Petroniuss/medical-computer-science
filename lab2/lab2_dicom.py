# AGH UST Medical Informatics 03.2021
# Lab 2 : DICOM

import pydicom
from tkinter import *
from PIL import Image, ImageTk
from math import sqrt

class MainWindow():

    ds = pydicom.dcmread("head.dcm")
    data = ds.pixel_array

    def __init__(self, main):
        # print patient name
        print(self.ds.PatientName)
        self.mouse_position = (0, 0)
        self.measurement_mode = False

        #todo: from ds get windowWidth and windowCenter
        self.window_width = self.ds.WindowWidth
        self.window_center = self.ds.WindowCenter

        # prepare canvas
        self.canvas = Canvas(main, width=512, height=512)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.init_window)
        self.canvas.bind("<B1-Motion>", self.motion)
        self.canvas.bind("<Double-1>", self.init_measurement)
        self.canvas.bind("<ButtonRelease-1>", self.finish_measurement)

        # load image
        # todo: apply transform
        self.array = self.transform_data(self.data)
        self.image = Image.fromarray(self.array)
        self.image = self.image.resize((512, 512), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image=self.image, master=root)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.img)


    def transform_data(self, data):
        # todo: transform data (apply window width and center)
        new_data = data.copy()
        s = max(0, self.window_center - (self.window_width // 2))
        for j in range(len(data)):
            for i in range(len(data[j])):
                p = data[j][i]
                if abs(p - self.window_center) <= self.window_width // 2:
                    new_data[j][i] = min(255, 255 * (p - s) // self.window_width)
                else:
                    new_data[j][i] = 0.

        return new_data

    def init_window(self, event):
        print('init_window: save mouse position.')
        self.mouse_position = (event.x, event.y)
        print("x: " + str(event.x) + " y: " + str(event.y))

    def motion(self, event):
        if self.measurement_mode:
            self.update_measurement(event)
        else:
            self.update_window(event)

    def update_window(self, event):
        print('update_window: modify window width and center')
        print("x: " + str(event.x) + " y: " + str(event.y))

        new_window_width = self.window_width + event.x - self.mouse_position[0]
        if 0 <= new_window_width <= 1024:
            self.window_width = new_window_width

        new_window_center = self.window_center - event.y + self.mouse_position[1]
        if 0 <= new_window_center <= 1024:
            self.window_center = new_window_center

        print(f'window_center: {self.window_center}, window_width: {self.window_width}')

        self.array = self.transform_data(self.data)
        self.new_image = Image.fromarray(self.array)
        self.new_image = self.new_image.resize((512, 512), Image.ANTIALIAS)
        self.new_img = ImageTk.PhotoImage(image=self.new_image, master=root)
        self.canvas.itemconfig(self.image_on_canvas, image=self.new_img)

    def init_measurement(self, event):
        # todo: save mouse position
        # todo: create line
        # hint: self.canvas.create_line(...)
        print('save mouse position, create line')
        print("x: " + str(event.x) + " y: " + str(event.y))

        self.measurement_mode = True
        self.mouse_position = (event.x, event.y)
        self.line = self.canvas.create_line(event.x, event.y, event.x, event.y)

    def update_measurement(self, event):
        # todo: update line
        # hint: self.canvas.coords(...)
        new_coords = [self.mouse_position[0], self.mouse_position[1], event.x, event.y]
        self.canvas.coords(self.line, *new_coords)

    def finish_measurement(self, event):
        # todo: print measured length in mm
        if self.measurement_mode:
            print("x: " + str(event.x) + " y: " + str(event.y))

            pixel_size_x, pixel_size_y = self.ds.PixelSpacing

            length_x = pixel_size_x * abs(event.x - self.mouse_position[0])
            length_y = pixel_size_y * abs(event.y - self.mouse_position[1])

            length = sqrt(length_x ** 2 + length_y ** 2)
            print("measurement: line's length: {:.2f}mm".format(length))

            self.canvas.delete(self.line)
            self.measurement_mode = False

#----------------------------------------------------------------------

root = Tk()
MainWindow(root)
root.mainloop()
