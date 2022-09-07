# With multiprocessing
import cv2
import queue
from multiprocessing import JoinableQueue, Process

# Consumer process takes the frame from the queue and detects the faces and loads them on the result window and HDD
def consumer(face_cascade, q: JoinableQueue, output_video):
    frame_number = 1
    while True:
        try:
            frame = q.get(block=False) # Fetch the element at the front of the queue
            if frame is None: break # Last element in the queue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert to grayscale
            faces = face_cascade.detectMultiScale(gray, 1.1, 4) # Detect faces
            for (x, y, w, h) in faces: # Iterate over all the detected faces
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2) # Put rectangle on faces
            cv2.putText(img=frame, text='{0:05d}'.format(frame_number), org=(0, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255)) # Put the frame number on top left
            cv2.imshow('face_detection', frame) # Displaying the frame on the window
            output_video.write(frame)
            frame_number+=1
        except queue.Empty:
            pass

# Producer process generates the frame from the webcam and pushes it on the queue
def producer(camera_object, q: JoinableQueue):
    while(True):
        success, frame = camera_object.read() # Reads a frame from video camera
        if not success: break
        q.put(frame) # Enqueue the frame to be processed by the consumer
        key_pressed = cv2.waitKey(1) # Press the key using keyboard
        if key_pressed == 27: break # Hit ESC key to terminate the program
    q.put(None) # Last frame as None. Used to synchronize the consumer
    q.join()

if __name__ == "__main__":
    q = JoinableQueue()
    camera_object = cv2.VideoCapture(0) # Start the webcam
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml') # load the face detection model
    output_video = cv2.VideoWriter(filename='output.mp4', fourcc=cv2.VideoWriter_fourcc(*'mp4v'), fps=25, frameSize=(int(camera_object.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera_object.get(cv2.CAP_PROP_FRAME_HEIGHT)))) # stores video on disk

    producer_process = Process(target=producer, args=(camera_object, q))
    producer_process.start()
    consumer_process = Process(target=consumer, args=(face_cascade, q, output_video))
    consumer_process.start()

    producer_process.join()
    consumer_process.join()

    cv2.destroyAllWindows() # Release the window resources
    camera_object.release() # Close the camera
    output_video.release() # Close the video writer