from PySide6.QtWidgets import QApplication, QLabel, QMainWindow,QFormLayout,QWidget, QPushButton, QVBoxLayout, QComboBox
from PySide6.QtCore import Slot, QRect, QPoint, QTimer
import numpy as np
import pyautogui
from widget.area_selector import AreaSelector
from widget.button_next_selector import ButtonNextSelector
from widget.image_cv import ImageCv
from helper.screen_graber import ScreenGraberThread


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("OMETV SKIPER")
        self.area_selector = AreaSelector()
        self.button_select_area = QPushButton("Select Area")
        self.button_select_start_btn = QPushButton("Select Start Area")
        self.button_select_start_btn.setEnabled(False)
        self.button_start = QPushButton("Start")
        self.button_start.setEnabled(False)
        self.cb_gender = QComboBox()
        self.cb_gender.setCurrentText("Male")
        self.cb_gender.addItem("Male")
        self.cb_gender.addItem("Female")
        self.cb_gender.addItem("Not Found")
        self.image = ImageCv()
        self.timer = QTimer()
        self.can_click = True
        self.label_gender = QLabel()
        self.button_next_selector = ButtonNextSelector()
        self.screen_graber_thread = ScreenGraberThread()
        self.stop = QPushButton("Stop")
        self.stop.setEnabled(False)


        vbox = QVBoxLayout()
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form.addRow(QLabel("Skip On gender"), self.cb_gender)
        vbox.addWidget(self.image)
        vbox.addLayout(form)
        vbox.addWidget(self.button_select_area)
        vbox.addWidget(self.button_select_start_btn)
        vbox.addWidget(self.button_start)
        vbox.addWidget(self.label_gender)
        vbox.addWidget(self.stop)
        widget = QWidget()
        widget.setLayout(vbox)

        self.start_point = QPoint(0, 0)

        self.area_selector.area_selected.connect(self.handle_area_selected)
        self.button_next_selector.area_selected.connect(self.handle_button_start_selected)

        self.button_select_area.clicked.connect(self.handle_select_area)
        self.button_start.clicked.connect(self.handle_start)
        self.screen_graber_thread.image_updated.connect(self.handle_image)
        self.screen_graber_thread.gender_detected.connect(self.handle_gender_detection)
        self.button_select_start_btn.clicked.connect(self.on_select_start_btn)
        self.stop.clicked.connect(self.on_stop)
        self.setCentralWidget(widget)
        
    def on_stop(self):
        self.screen_graber_thread.stop()
        self.button_select_area.setEnabled(True)

    def on_select_start_btn(self):
        self.button_next_selector.init()
        self.button_next_selector.setVisible(True)
    
    @Slot(QRect)
    def handle_area_selected(self, rect):
        monitor = {"top": rect.top(), "left": rect.left(), "width": rect.width(), "height": rect.height()}
        self.screen_graber_thread.set_monitor(monitor)
        self.area_selector.hide()
        self.button_select_start_btn.setEnabled(True)

    @Slot(QPoint)
    def handle_button_start_selected(self, point):
        self.start_point = point
        self.button_next_selector.hide()
        self.button_start.setEnabled(True)

    def handle_select_area(self):
        self.screen_graber_thread.stop()
        self.image.reset_frame()
        self.area_selector.init()
        self.area_selector.setVisible(True)
    
    def handle_start(self):
        self.button_start.setEnabled(False)
        self.stop.setEnabled(True)
        self.button_select_area.setEnabled(True)
        self.screen_graber_thread.start()

    @Slot(str)
    def handle_gender_detection(self, gender: str):
        self.label_gender.setText("Gender: {}".format(gender))
        if gender == self.cb_gender.currentText() and self.can_click:
            pyautogui.click(x=self.start_point.x(), y=self.start_point.y())
            self.can_click = False
            self.timer.singleShot(5000, self.on_timer)
        
    def closeEvent(self, event):
        self.screen_graber_thread.stop()
        event.accept()
    
    def on_timer(self):
        self.can_click = True

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