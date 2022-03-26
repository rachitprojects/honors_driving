# Import kivy dependencies first
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

# Import kivy UX components
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera

# Import other kivy stuff
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger

# Import other dependencies
import cv2
import tensorflow as tf
from keras.preprocessing.image import img_to_array
import os
import numpy as np

import boto3
import json

from PIL import Image
import subprocess

# Build app and layout
class CamApp(App):

    def build(self):
        # Main layout components
        # self.web_cam = Image()
        self.coords = [(12.9716, 77.5946), (12.8431, 77.4863), (13.1048, 77.5763), (12.925453, 77.546761), (12.9249, 77.5662), (12.9271, 77.5548), (12.972442, 77.580643), (12.972442, 77.580643), (12.9462, 77.5103), (12.9426, 77.6027), (12.9426, 77.6027), (13.0108, 77.6493), (12.9422, 77.5748), (12.9957, 77.5419), (12.9966, 77.6042), (13.0588, 77.59385), (12.9062, 77.7066), (12.9586, 77.5634), (12.9708, 77.5806), (13.0823, 77.5068), (12.9846, 77.6622), (13.0458, 77.5111), (12.9376, 77.5991), (12.8807, 77.5576), (12.961, 77.6387), (13.0077, 77.6737), (13.0007, 77.6165), (12.9791, 77.5777), (12.9463, 77.5669), (13.0821, 77.5762), (12.9716, 77.5946), (13.0324, 77.5992), (13.1585, 77.4888), (13.1585, 77.4888), (12.98551, 77.60678), (13.0311, 77.5569), (12.9956, 77.6113), (12.9716, 77.5946), (12.9719, 77.6412), (12.9876, 77.6379), (13.0519, 77.5416), (12.9329, 77.5839), (12.9301, 77.5877), (12.9301, 77.5877), (12.9105, 77.5857), (12.9986, 77.7631), (12.9, 77.4833), (13.0585, 77.6407), (13.0006, 77.6746), (12.9716, 77.5946), (12.9317, 77.6227), (12.9382, 77.6228), (12.9211, 77.6134), (12.9709, 77.5658), (12.9904, 77.6842), (13.0114, 77.5467), (13.0081, 77.5648), (12.9996, 77.5689), (12.9512, 77.6998), (13.0002, 77.6336), (13.032, 77.5605), (12.9717, 77.5132), (13.02889, 77.44233), (12.9642, 77.6207), (13.0124, 77.5361), (12.9396, 77.5204), (12.9769, 77.6493), (13.0085, 77.4996), (12.9906, 77.5533), (12.9634, 77.6035), (13.0223, 77.5949), (12.9864, 77.582), (12.9611, 77.6047), (12.987, 77.5662), (12.991388, 77.61186), (13.0059, 77.6231), (12.9052, 77.5433), (12.9293, 77.568), (12.9815, 77.6192), (12.9911, 77.592), (13.0754, 77.5591), (12.9699, 77.5333), (12.9645, 77.6865), (13.0319, 77.7322), (13.0041, 77.5749), (12.9496, 77.6223), (12.9698, 77.7499), (12.949, 77.5978), (13.1048, 77.5763), (13.0178, 77.5572)]

        self.web_cam = Camera(play=True, index=1, resolution=(640, 480))
        # self.button = Button(text="Verify", on_press=self.verify, size_hint=(1,.1))
        self.emotion_label = Label(text="NoEmotion", size_hint=(1,.1))
        self.emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']
        self.emotion_data = []
        self.count = 0

        # Add items to layout
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.web_cam)
        # layout.add_widget(self.button)
        layout.add_widget(self.emotion_label)

        # Load tensorflow/keras model
        self.model = tf.keras.models.load_model('siamesemodel.h5')
        self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Setup video capture device
        # self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0)

        return layout

    # Run continuously to get webcam feed
    def update(self, *args):

        # self.web_cam.export_to_png("IMG_{}.png".format("randomimg"))
        texture = self.web_cam.texture
        if texture:
            # print(texture.pixels)
            pil_image = Image.frombytes(mode='RGBA', size=texture.size, data=texture.pixels)
            numpy_picture = np.array(pil_image)
            # print(numpy_picture)

            gray = cv2.cvtColor(numpy_picture,cv2.COLOR_BGR2GRAY)
            faces = self.face_classifier.detectMultiScale(gray)

            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+h,x:x+w]
                roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray])!=0:
                    roi = roi_gray.astype('float')/255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi,axis=0)

                    prediction = self.model.predict(roi)[0]
                    label=self.emotion_labels[prediction.argmax()]
                    self.emotion_label.text = label
            # payload = {
            #     "latitude" : self.coords[self.count][0],
            #     "longitude" : self.coords[self.count][1],
            #     "emotion" : self.emotion_label.text
            # }
            # self.emotion_data.append([len(self.emotion_data), json.dumps(payload)]    )
            data = str(self.coords[self.count][0]) + " " + str(self.coords[self.count][1]) + " " + self.emotion_label.text
            self.emotion_data.append(data)

            # self.emotion_data.append((self.coords[self.count][0], self.coords[self.count][1], self.emotion_label.text))
            self.count += 1
            # print(len(self.emotion_data))
            if len(self.emotion_data) == 9:
                # print(self.emotion_data)
                # Implement Kinesis code
                # Convert to a big array and send
                # emo_data = str(dict(self.emotion_data)) + "         "
                # print(emo_data)
                emo_data = ";".join(self.emotion_data)
                # print(emo_data)
                subprocess.Popen(["python3", "kinesis_tests.py", emo_data])
                self.emotion_data = []
            if self.count == 89:
                self.count = 0
        # Read frame from opencv
        # ret, frame = self.capture.read()
        # print(frame)
        # frame = frame[120:120+250, 200:200+250, :]

        # Flip horizontall and convert image to texture
        # buf = cv2.flip(frame, 0).tostring()
        # img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        # img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # self.web_cam.texture = img_texture

    # Load image from file and conver to 100x100px
    # def preprocess(self, file_path):
    #     # Read in image from file path
    #     byte_img = tf.io.read_file(file_path)
    #     # Load in the image
    #     img = tf.io.decode_jpeg(byte_img)
    #
    #     # Preprocessing steps - resizing the image to be 100x100x3
    #     img = tf.image.resize(img, (100,100))
    #     # Scale image to be between 0 and 1
    #     img = img / 255.0
    #
    #     # Return image
    #     return img
    #
    def verify(self, *args):
        pass



if __name__ == '__main__':
    CamApp().run()
