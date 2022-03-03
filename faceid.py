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

from PIL import Image

# Build app and layout
class CamApp(App):

    def build(self):
        # Main layout components
        # self.web_cam = Image()
        self.web_cam = Camera(play=True, index=1, resolution=(640, 480))
        self.button = Button(text="Verify", on_press=self.verify, size_hint=(1,.1))
        self.emotion_label = Label(text="No Emotion", size_hint=(1,.1))
        self.emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']


        # Add items to layout
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.web_cam)
        layout.add_widget(self.button)
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
    # # Verification function to verify person
    # def verify(self, *args):
    #     # Specify thresholds
    #     detection_threshold = 0.99
    #     verification_threshold = 0.8
    #
    #     # Capture input image from our webcam
    #     SAVE_PATH = os.path.join('application_data', 'input_image', 'input_image.jpg')
    #     ret, frame = self.capture.read()
    #     frame = frame[120:120+250, 200:200+250, :]
    #     cv2.imwrite(SAVE_PATH, frame)
    #
    #     # Build results array
    #     results = []
    #     for image in os.listdir(os.path.join('application_data', 'verification_images')):
    #         input_img = self.preprocess(os.path.join('application_data', 'input_image', 'input_image.jpg'))
    #         validation_img = self.preprocess(os.path.join('application_data', 'verification_images', image))
    #
    #         # Make Predictions
    #         result = self.model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))
    #         results.append(result)
    #
    #     # Detection Threshold: Metric above which a prediciton is considered positive
    #     detection = np.sum(np.array(results) > detection_threshold)
    #
    #     # Verification Threshold: Proportion of positive predictions / total positive samples
    #     verification = detection / len(os.listdir(os.path.join('application_data', 'verification_images')))
    #     verified = verification > verification_threshold
    #
    #     # Set verification text
    #     self.verification_label.text = 'Verified' if verified == True else 'Unverified'
    #
    #     # Log out details
    #     Logger.info(results)
    #     Logger.info(detection)
    #     Logger.info(verification)
    #     Logger.info(verified)
    #
    #
    #     return results, verified



if __name__ == '__main__':
    CamApp().run()
