from os import path
import os
from numpy import ndarray
import cv2

this_path = os.path.dirname(__file__)
faceProto=path.join(this_path, "opencv_face_detector.pbtxt")
faceModel=path.join(this_path, "opencv_face_detector_uint8.pb")
genderProto=path.join(this_path, "gender_deploy.prototxt")
genderModel=path.join(this_path, "gender_net.caffemodel")

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
genderList=['Male','Female']

face_net=cv2.dnn.readNet(faceModel,faceProto)
gender_net=cv2.dnn.readNet(genderModel,genderProto)

def detect_faces(image: ndarray):
    """
    Detect faces in an image.
    :param image: The image to detect faces in.
    :return: A list of bounding boxes for the faces and image.
    """
    frame = image.copy()
    frame_height=frame.shape[0]
    frame_width=frame.shape[1]
    blob=cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], True, False)
    face_net.setInput(blob)
    detections=face_net.forward()
    face_boxes=[]
    for i in range(detections.shape[2]):
        confidence=detections[0,0,i,2]
        if confidence>0.7:
            x1=int(detections[0,0,i,3]*frame_width)
            y1=int(detections[0,0,i,4]*frame_height)
            x2=int(detections[0,0,i,5]*frame_width)
            y2=int(detections[0,0,i,6]*frame_height)
            face_boxes.append([x1,y1,x2,y2])
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), int(round(frame_height/150)), 8)
    return frame, face_boxes

def detect_gender(box, img: ndarray):
    try:
        blob = cv2.dnn.blobFromImage(img, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
        gender_net.setInput(blob)
        genderPreds=gender_net.forward()
        gender=genderList[genderPreds[0].argmax()]
        return gender
    except Exception as e:
        return e