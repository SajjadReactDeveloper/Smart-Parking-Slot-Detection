import cv2
import pickle
import cvzone
import numpy as np

class VideoCamera(object):

    def __init__(self):
      self.video = cv2.VideoCapture("geh.mp4")
      # with open('carParkPos', 'rb') as f:
      #   posList = pickle.load(f)

      # #Width and Height of Rectangle
      # width = 60
      # height = 108

      # def checkParkingSpace(imgProc):
      #   availableSpace = 0

      #   for i, pos in enumerate(posList):
      #       # print(posList)
      #       x,y = pos

      #       #crop image
      #       frame = imgProc[y:y+height, x:x+width]
      #       #cv2.imshow(str(x*y), frame)
      #       count = cv2.countNonZero(frame)

      #       if count < 2800:
      #           color = (0,255,0)
      #           thickness = 5
      #           availableSpace += 1
      #           cvzone.putTextRect(img, f'{str(i+1)}', (x, y+height-3), scale=1.5, thickness=2, offset=0, colorR=color)
      #           # available.add(str(i+1))
                    
      #       else:
      #           color = (0,0,255)
      #           thickness = 2
      #       cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
      #       # cvzone.putTextRect(img, str(count), (x, y+height-3), scale=1.5, thickness=2, offset=0, colorR=color)

      #   cvzone.putTextRect(img, str(availableSpace), (100, 50), scale=3, thickness=5, offset=20)
      #   # print(available)


      # while True:
      #   if self.video.get(cv2.CAP_PROP_POS_FRAMES) == self.video.get(cv2.CAP_PROP_FRAME_COUNT):
      #       self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)

      #   success, img = self.video.read();
        
      #   imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      #   imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
      #   imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
      #   imgMedian = cv2.medianBlur(imgThreshold, 5)
      #   kernel = np.ones((3,3), np.uint8)
      #   imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

      #   checkParkingSpace(imgDilate)

      #   cv2.imshow("Image", img)
      #   cv2.waitKey(10)

    def __del__(self):
      self.video.release()

    def get_frame(self):
      with open('carParkPos', 'rb') as f:
          posList = pickle.load(f)
      width = 60
      height = 108
      availableSpace = 0

      def checkParkingSpace(imgProc):
        availableSpace = 0

        for i, pos in enumerate(posList):
            # print(posList)
            x,y = pos

            #crop image
            frame = imgProc[y:y+height, x:x+width]
            #cv2.imshow(str(x*y), frame)
            count = cv2.countNonZero(frame)

            if count < 2800:
                color = (0,255,0)
                thickness = 5
                availableSpace += 1
                cvzone.putTextRect(frame, f'{str(i+1)}', (x, y+height-3), scale=1.5, thickness=2, offset=0, colorR=color)
                # available.add(str(i+1))
                    
            else:
                color = (0,0,255)
                thickness = 2
            cv2.rectangle(frame, pos, (pos[0] + width, pos[1] + height), color, thickness)
            # cvzone.putTextRect(img, str(count), (x, y+height-3), scale=1.5, thickness=2, offset=0, colorR=color)

        cvzone.putTextRect(frame, str(availableSpace), (100, 50), scale=3, thickness=5, offset=20)
      if self.video.get(cv2.CAP_PROP_POS_FRAMES) == self.video.get(cv2.CAP_PROP_FRAME_COUNT):
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
      ret, frame = self.video.read()
      imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
      imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
      imgMedian = cv2.medianBlur(imgThreshold, 5)
      kernel = np.ones((3,3), np.uint8)
      imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

      checkParkingSpace(imgDilate)
      ret, jpeg = cv2.imencode('.jpg', frame)
      cv2.waitKey(10)
      # return jpeg.tobytes()
      return frame
