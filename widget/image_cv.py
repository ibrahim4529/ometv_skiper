from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QImage, QResizeEvent
from PySide6.QtCore import Qt, Slot
import numpy as np

class ImageCv(QLabel):
    def __init__(self, parent=None, width=640, height=480):
        QLabel.__init__(self, parent)
        self.pixmap = QPixmap(width, height)
        self.pixmap.fill(Qt.gray)
        self.setMinimumSize(320, 200)
        self.setMaximumSize(width, height)
        self.setPixmap(self.pixmap)
    
    @Slot(np.ndarray)
    def update_image_cv(self, cv_image: np.ndarray):
        image_pixmap = self.convert_cv_to_pixmap(cv_image)
        self.setPixmap(image_pixmap)
        self.update()
    
    def convert_cv_to_pixmap(self, cv_image: np.ndarray):
        """Convert from an opencv image to QPixmap"""
        h, w, ch = cv_image.shape
        bytes_perline = ch * w
        pixmap_image = QImage(cv_image.data, w, h, bytes_perline, QImage.Format_RGB888)
        qt_image = pixmap_image.scaled(self.width(), self.height(), Qt.IgnoreAspectRatio)
        pixmap = QPixmap.fromImage(qt_image)
        return pixmap
    
    def reset_frame(self):
        self.pixmap = QPixmap(self.width(), self.height())
        self.pixmap.fill(Qt.gray)
        self.setPixmap(self.pixmap)
        self.update()