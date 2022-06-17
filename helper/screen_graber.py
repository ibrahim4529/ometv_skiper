from typing import Optional
from PySide6.QtCore import QThread, Signal
import mss
import numpy as np
import cv2

class ScreenGraberThread(QThread):
    """
    This class is used to grab the screen and emit the image.
    """
    image_updated = Signal(np.ndarray)
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
                self.image_updated.emit(img)

    def stop(self):
        self.running = False
        self.wait()
    
    def start(self, priority = QThread.Priority.InheritPriority):
        self.running = True
        return super().start(priority)
    
    def set_monitor(self, monitor):
        self.monitor = monitor
