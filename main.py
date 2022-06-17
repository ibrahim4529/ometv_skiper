from PySide6.QtWidgets import QApplication, QLabel, QMainWindow,QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Slot, QRect
import numpy as np
from widget.area_selector import AreaSelector
from widget.image_cv import ImageCv
from helper.screen_graber import ScreenGraberThread

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("OMETV SKIPER")
        self.area_selector = AreaSelector()
        self.button_select_area = QPushButton("Select Area")
        self.button_start = QPushButton("Start")
        self.button_start.setEnabled(False)
        self.image = ImageCv()
        self.label_gender = QLabel()

        self.screen_graber_thread = ScreenGraberThread()

        vbox = QVBoxLayout()
        vbox.addWidget(self.image)
        vbox.addWidget(self.button_select_area)
        vbox.addWidget(self.button_start)
        vbox.addWidget(self.label_gender)
        widget = QWidget()
        widget.setLayout(vbox)

        self.area_selector.area_selected.connect(self.handle_area_selected)
        self.button_select_area.clicked.connect(self.handle_select_area)
        self.button_start.clicked.connect(self.handle_start)
        self.screen_graber_thread.image_updated.connect(self.handle_image)
        self.screen_graber_thread.gender_detected.connect(self.handle_gender_detection)
        self.setCentralWidget(widget)
    
    @Slot(QRect)
    def handle_area_selected(self, rect):
        monitor = {"top": rect.top(), "left": rect.left(), "width": rect.width(), "height": rect.height()}
        self.screen_graber_thread.set_monitor(monitor)
        self.area_selector.hide()
        self.button_start.setEnabled(True)

    def handle_select_area(self):
        self.screen_graber_thread.stop()
        self.image.reset_frame()
        self.area_selector.init()
        self.area_selector.setVisible(True)
    
    def handle_start(self):
        self.button_start.setEnabled(False)
        self.button_select_area.setEnabled(True)
        self.screen_graber_thread.start()

    @Slot(str)
    def handle_gender_detection(self, gender: str):
        self.label_gender.setText("Gender: {}".format(gender))
    
    def closeEvent(self, event):
        self.screen_graber_thread.stop()
        event.accept()

    @Slot(np.ndarray)
    def handle_image(self, image: np.ndarray):
        self.image.update_image_cv(image)

def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()