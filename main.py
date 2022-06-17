from PySide6.QtWidgets import QApplication, QMainWindow,QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Slot
import numpy as np
from widget.area_selector import AreaSelector
from widget.image_cv import ImageCv
from helper.screen_graber import ScreenGraberThread

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Main Window")
        self.area_selector = AreaSelector()
        self.button_select_area = QPushButton("Select Area")
        self.button_start = QPushButton("Start")
        self.image = ImageCv()

        self.screen_graber_thread = ScreenGraberThread()

        vbox = QVBoxLayout()
        vbox.addWidget(self.image)
        vbox.addWidget(self.button_select_area)
        vbox.addWidget(self.button_start)
        widget = QWidget()
        widget.setLayout(vbox)

        self.button_select_area.clicked.connect(self.handle_select_area)
        self.button_start.clicked.connect(self.handle_start)
        self.screen_graber_thread.image_updated.connect(self.handle_image)

        self.setCentralWidget(widget)
    
    def handle_select_area(self):
        self.screen_graber_thread.stop()
        self.image.reset_frame()
        self.area_selector.init()
        self.area_selector.setVisible(True)
        self.button_start.setEnabled(True)
    
    def handle_start(self):
        self.button_start.setEnabled(False)
        self.button_select_area.setEnabled(True)
        self.area_selector.hide()
        area_rect = self.area_selector.get_react()
        monitor = {"top": area_rect.top(), "left": area_rect.left(), "width": area_rect.width(), "height": area_rect.height()}
        self.screen_graber_thread.set_monitor(monitor=monitor)
        self.screen_graber_thread.start()

    
    def closeEvent(self, event):
        self.screen_graber_thread.stop()
        event.accept()

    @Slot(np.ndarray)
    def handle_image(self, image: np.ndarray):
        self.image.update_image_cv(image)
        # Todo make face and gender detection on here

def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()