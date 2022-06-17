from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from widget.area_selector import AreaSelector

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Main Window")
        self.area_selector = AreaSelector()
        self.button_select_area = QPushButton("Select Area")
        self.button_select_area.clicked.connect(self.handle_select_area)

        self.setCentralWidget(self.button_select_area)
    
    def handle_select_area(self):
        self.area_selector.init()
        self.area_selector.show()

def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()