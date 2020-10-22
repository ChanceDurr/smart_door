import cv2
import numpy as np
import os
import time
class Detector():

    base_path = "/home/pi/Desktop/smart_door/"
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(base_path + 'face_detection/trainer.yml')
    cascadePath = base_path + "face_detection/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0

    # names related to ids: example ==> Blake: id=1,  etc
    names = ['None', 'Blake', 'Chance', 'David', 'Mom', 'Dad']

    # Check if name shows frequently with a certain confidence
    confidence_check = '00000'

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    def c_check(self, myBool):
        if myBool:
            self.confidence_check = '1' + self.confidence_check[:4]
        else:
            self.confidence_check = '0' + self.confidence_check[:4]


    def start(self):
        start_time = time.time()
        while time.time() - start_time < 15:
            ret, img = self.cam.read()
            #img = cv2.flip(img, -1) # Flip vertically
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            
            faces = self.faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(self.minW), int(self.minH)),
            )

            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])

                if id == 2 and confidence > 35:
                    self.c_check(True)
                else:
                    self.c_check(False)
                
                # If confidence is less them 100 ==> "0" : perfect match 
                if (confidence < 100):
                    id = self.names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                

                cv2.putText(
                            img,
                            str(id),
                            (x+5,y-5),
                            self.font,
                            1, 
                            (255,255,255), 
                            2
                        )
                cv2.putText(
                            img,
                            str(confidence),
                            (x+5,y+h-5),
                            self.font, 
                            1, 
                            (255,255,0), 
                            1
                        )  
            
            cv2.imshow('identify',img)
            print(self.confidence_check)
            if self.confidence_check == '11111':
                return True
        return False

if __name__ == '__main__':
    test = Detector()
    print(test.start())