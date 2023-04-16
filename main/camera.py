import cv2
import numpy as np
import threading 
import urllib
from main.audio import play_alarm

caffe_path = 'D:\Faculta\AN3_SEM1\SSC\Proiect\WebDetectionApp\main\models\MobileNetSSD_deploy.caffemodel'
deploy_path = 'D:\Faculta\AN3_SEM1\SSC\Proiect\WebDetectionApp\main\models\MobileNetSSD_deploy.prototxt'
min_certitude = 0.0

classes = ["background", "airplane", "bicycle", "bird", "boat", "bottle",
           "bus", "car", "cat", "chair", "cow", "table", "dog", "horse", "motorbike",
           "person", "plant", "sheep", "sofa", "train", "tv"]

class Camera(object):
    windowSize = (630, 480)
    def __init__(self):
        self.__alarmOn = False
        self.__prev_rect = (0,0,0,0)

    def set_alarmOn(self, alarmOn):
        self.__alarmOn = alarmOn 
        self.__prev_rect = (0,0,0,0)

    def imencode_frame(frame):
        resizedImg = cv2.resize(frame, Camera.windowSize, interpolation=cv2.INTER_LINEAR)
        image = cv2.flip(resizedImg, 1)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes();

    def drawRect(frame, rect):
        color = (0, 275, 0)
        thickness = 9
        topLeftCorner = (rect[0], rect[1])
        bottomRightCorner = (rect[2], rect[3])
        cv2.rectangle(frame, topLeftCorner, bottomRightCorner, color, thickness)
        return frame

    def detect(self, frame):
        if self.__alarmOn == False:
            return frame

        model_detection = cv2.dnn.readNetFromCaffe(deploy_path, caffe_path)

        blob = cv2.dnn.blobFromImage(frame, 1, (224,224), (0,0,0), True, crop=False)
        model_detection.setInput(blob)
        detections = model_detection.forward()

        width = frame.shape[0]
        height = frame.shape[1]
        chanells = detections.shape[2]
        color = (0, 255, 0)
        thickness = 9

        for chanell in range(chanells):
            certitude = detections[0][0][chanell][2]
            if certitude > min_certitude:
                class_index = int(detections[0, 0, chanell, 1])

                if classes.index("person") == class_index:
                    upper_left_x = int(detections[0, 0, chanell, 3] * width)
                    upper_left_y = int(detections[0, 0, chanell, 4] * height)

                    lower_right_x = int(detections[0, 0, chanell, 5] * width)
                    lower_right_y = int(detections[0, 0, chanell, 6] * height)

                    rect = (upper_left_x, upper_left_y, lower_right_x, lower_right_y)
                    
                    play_alarm()
                    print("detected")
                    
                    self.__prev_rect = (upper_left_x, upper_left_y, lower_right_x, lower_right_y)
                    cv2.rectangle(frame,  (upper_left_x, upper_left_y), (lower_right_x, lower_right_y), color, thickness)

        return frame

class VideoCamera(Camera):
    def __init__(self):
        super().__init__()
        self.video = cv2.VideoCapture(0)
        self.success, self.frame = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    #This function is used in views
    def get_frame(self):
        img = self.frame
        img = super().detect(self.frame)
        return Camera.imencode_frame(img)

    def update(self):
        while True:
            self.success, self.frame = self.video.read()

class MobileCamera(Camera):
    def __init__(self):
        super().__init__()
        self.url = "http://172.20.10.5:8080/shot.jpg"

    def __del__(self):
        cv2.destroyAllWindows()

    #This function is used in views
    def get_frame(self):
        response = urllib.request.urlopen(self.url)
        imgNpArray = np.array(bytearray(response.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNpArray, -1)
        img = super().detect(img)
        return Camera.imencode_frame(img)
