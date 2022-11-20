from flask import Flask, render_template, Response
from flask_cors import CORS
from camera import VideoCamera
import cv2
import pickle
import cvzone
import numpy as np
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')
    
available = set();

def gen(camera):
    while True:
        frame = camera.get_frame()
        with open('carParkPos', 'rb') as f:
          posList = pickle.load(f)
        width = 108
        height = 60
        availableSpace = 0

        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3,3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
        for i, pos in enumerate(posList):
            x,y = pos

            # crop image
            img = imgDilate[y:y+height, x:x+width]
            #cv2.imshow(str(x*y), frame)
            count = cv2.countNonZero(img)

            if count < 2800:
                color = (0,255,0)
                thickness = 5
                availableSpace += 1
                cvzone.putTextRect(frame, f'{str(i+1)}', (x, y+height-3), scale=1.5, thickness=2, offset=0, colorR=color)
                available.add(str(i+1))
                    
            else:
                color = (0,0,255)
                thickness = 2
                if str(i+1) in available:
                    available.remove(str(i+1))
            cv2.rectangle(frame, pos, (pos[0] + width, pos[1] + height), color, thickness)
            # cvzone.putTextRect(frame, str(count), (x, y+height-3), scale=1.5, thickness=2, offset=0, colorR=color)

        cvzone.putTextRect(frame, str(availableSpace), (100, 50), scale=3, thickness=5, offset=20)
        ret, jpeg = cv2.imencode('.jpg', frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
               
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/available')
def availableSlots():
    json_str = json.dumps(list(available))
    return {"Slots": json_str}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, threaded=True, use_reloader=False)
