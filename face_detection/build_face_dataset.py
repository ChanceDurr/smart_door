from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True, help="path to where the face cascade resides")
ap.add_argument("-o", "--output", required=True, help="path to the output directory")
ap.add_argument("-i", "--id", required=True, help="id of person that is being added")
args = vars(ap.parse_args())
detector = cv2.CascadeClassifier(args['cascade'])

# initilize the video stream and allow the camera sensor to warm up,
# and initialize the total number of example face written to disk
print("[INFO] starting video stream...")

# switch this when running on rpi
#vs = VideoStream(src=0).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2)

# Check if pictures already exist
if os.listdir(args["output"]):
    total = int(os.listdir(args["output"])[-1].split(".")[1].lstrip("0")) + 1
else:
    total = 0

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream, clone it, (just
    # in case we want to write it to disk), and the resize the frame
    # so we can apply face detection faster
    frame = vs.read()
    orig = frame.copy()
    frame = imutils.resize(frame, width=400)

    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(
        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1,
        minNeighbors=5, minSize=(30,30)
    )

    # loop over the face detections and draw them on the frame
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the k key was pressed, write the original frame to disk
    # so we can later process it and use it for face recognition
    if key == ord("k"):
        p = os.path.sep.join([args["output"],  f"{args['id']}.{str(total).zfill(5)}.png"])
        cv2.imwrite(p, orig)
        total +=1

    # if the 'q' key was pressed, break from the loop
    elif key == ord("q"):
        break

# print the total faces saved and do a bit of cleanup
print(f"[INFO] {total} face images stored")
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()
