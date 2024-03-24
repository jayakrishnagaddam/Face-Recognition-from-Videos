from flask import Flask, render_template, Response
import cv2
import dlib

app = Flask(__name__)

# Load the pre-trained face detection model from dlib
detector = dlib.get_frontal_face_detector()

# Function to detect faces in a frame
def detect_faces(frame):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces in the frame
    faces = detector(gray_frame)
    # Draw rectangles around the detected faces
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame

# Function to read video frames
def gen_frames():
    cap = cv2.VideoCapture('static/video.mp4')
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        else:
            frame = detect_faces(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to render the HTML template
@app.route('/')
def index():
    return render_template('video.html')

# Route to stream video frames
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
