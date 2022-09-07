# Without multiprocessing
import cv2

camera_object = cv2.VideoCapture(0) # Start the webcam
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml') # load the face detection model
output_video = cv2.VideoWriter(filename='output.mp4', fourcc=cv2.VideoWriter_fourcc(*'mp4v'), fps=25, frameSize=(int(camera_object.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera_object.get(cv2.CAP_PROP_FRAME_HEIGHT)))) # stores video on disk
frame_number = 1

while(True):
    success, frame = camera_object.read() # Reads a frame from video camera
    if not success: break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.1, 4) # Detect faces
    for (x, y, w, h) in faces: # Iterate over all the detected faces
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2) # Put rectangle on faces
    cv2.putText(img=frame, text='{0:05d}'.format(frame_number), org=(0, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255)) # Put the frame number on top left
    cv2.imshow('face_detection', frame) # Displaying the frame on the window
    output_video.write(frame)
    key_pressed = cv2.waitKey(1) # Press the key using keyboard
    if key_pressed == 27: break # Hit ESC key to terminate the program
    frame_number+=1
cv2.destroyAllWindows() # Release the window resources
camera_object.release() # Close the camera
output_video.release()