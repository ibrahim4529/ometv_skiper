from typing import Optional
from PySide6.QtCore import QThread, Signal
import mss
import numpy as np
import cv2
from detector.detector import detect_faces, detect_gender

class ScreenGraberThread(QThread):
    """
    This class is used to grab the screen and emit the image.
    """
    image_updated = Signal(np.ndarray)
    gender_detected = Signal(str)
    monitor = {"top": 100, "left": 100, "width": 640, "height": 480}
    def __init__(self):
        QThread.__init__(self)
        self.running = False

    def run(self):
        self.running = True
        with mss.mss() as sct:
            while self.running:
                # The screen part to capture
                img = np.array(sct.grab(self.monitor))
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
                image, faces = detect_faces(img)
                if not faces:
                    self.gender_detected.emit("Not Foud")
                for box in faces:
                    face = img[max(0, box[1] - 20):
                           min(box[3] + 20, img.shape[0] - 1), max(0, box[0] - 20)
                           :min(box[2] + 20, img.shape[1] - 1)]
                    gender = detect_gender(box, face)
                    self.gender_detected.emit(gender)
                self.image_updated.emit(image)

    def stop(self):
        self.running = False
        self.wait()
    
    def start(self, priority = QThread.Priority.InheritPriority):
        self.running = True
        return super().start(priority)
    
    def set_monitor(self, monitor):
        self.monitor = monitor
