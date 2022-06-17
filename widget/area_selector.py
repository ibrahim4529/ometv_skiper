from PySide6.QtCore import Qt, QRect, QPoint, Signal
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPixmap, QPainter, QPen, QBrush, QScreen, QCloseEvent,QMouseEvent, QPaintEvent, QGuiApplication
from helper.enum import HandlePosition, DegrePosition
from widget.arrow_button import ArrowButton

class AreaSelector(QWidget):
    area_selected = Signal(QRect)
    def __init__(self):
        QWidget.__init__(self)

        self.frame_screen: QScreen = None
        self.screen_width = 0
        self.screen_height = 0

        self.handle_press: HandlePosition = HandlePosition.NO_HANDLE
        self.handle_under_mouse: HandlePosition = HandlePosition.NO_HANDLE

        # parameters needed to resize properly
        self.mouse_delta_x = 0
        self.mouse_delta_y = 0
        self.old_mouse_x = 0
        self.old_mouse_y = 0
        self.old_frame_width = 0
        self.old_frame_height = 0
        self.old_frame_x = 0
        self.old_frame_y = 0

        # buttons params
        self.frame_pen_width = 4
        self.radius = 20
        self.pen_width = 2

        # frame props
        self.frame_x = 0
        self.frame_y = 0
        self.frame_width = 320 + self.frame_pen_width
        self.frame_height = 200 + self.frame_pen_width
        self.frame_min_width = self.frame_width
        self.frame_min_height = self.frame_height

        # size selected area
        self.pixel_width = 0
        self.pixel_height = 0

        # colors
        self.frame_color: QColor = Qt.black


        self.detection_mode = False

        self.setWindowTitle("Select Area")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.ToolTip)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setVisible(False)
    
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.LeftButton:
            return
        match self.handle_under_mouse:
            case HandlePosition.NO_HANDLE:
                self.handle_press = HandlePosition.NO_HANDLE
            case HandlePosition.TOP_LEFT:
                self.handle_press = HandlePosition.TOP_LEFT
            case HandlePosition.TOP_MIDDLE:
                self.handle_press = HandlePosition.TOP_MIDDLE
            case HandlePosition.TOP_RIGHT:
                self.handle_press = HandlePosition.TOP_RIGHT
            case HandlePosition.BOTTOM_LEFT:
                self.handle_press = HandlePosition.BOTTOM_LEFT
            case HandlePosition.BOTTOM_MIDDLE:
                self.handle_press = HandlePosition.BOTTOM_MIDDLE
            case HandlePosition.BOTTOM_RIGHT:
                self.handle_press = HandlePosition.BOTTOM_RIGHT
            case HandlePosition.MIDDLE_LEFT:
                self.handle_press = HandlePosition.MIDDLE_LEFT
            case HandlePosition.MIDDLE_RIGHT:
                self.handle_press = HandlePosition.MIDDLE_RIGHT
            case HandlePosition.MIDDLE:
                self.handle_press = HandlePosition.MIDDLE
            case HandlePosition.OK_HANDLE:
                self.area_selected.emit(self.get_react())
        self.mouse_delta_x = event.x() - self.frame_x
        self.mouse_delta_y = event.y() - self.frame_y
        self.old_mouse_x = event.x()
        self.old_mouse_y = event.y()
        self.old_frame_width = self.frame_width
        self.old_frame_height = self.frame_height
        self.old_frame_x = self.frame_x + self.frame_width
        self.old_frame_y = self.frame_y + self.frame_height
        self.repaint()
        self.update()


    def mouseMoveEvent(self, event: QMouseEvent):
        if self.detection_mode:
            self.unsetCursor()
            return
        match self.handle_press:
            case HandlePosition.NO_HANDLE:
                pass
            case HandlePosition.TOP_LEFT:
                self.frame_x = event.x() - self.mouse_delta_x
                self.frame_y = event.y() - self.mouse_delta_y
                self.frame_width = self.old_mouse_x - event.x() + self.old_frame_width
                self.frame_height = self.old_mouse_y - event.y() + self.old_frame_height

                if self.frame_width < self.frame_min_width:
                    self.frame_x = self.old_frame_x - self.frame_min_width
                    self.frame_width = self.frame_min_width
                if self.frame_height < self.frame_min_height:
                    self.frame_y = self.old_frame_y - self.frame_min_height
                    self.frame_height = self.frame_min_height
                
                if self.frame_y <= 0 - self.frame_pen_width / 2:
                    self.frame_y = 0 - self.frame_pen_width / 2
                    self.frame_height = self.old_frame_y + self.frame_pen_width / 2
                if self.frame_x <= 0 - self.frame_pen_width / 2:
                    self.frame_x = 0 - self.frame_pen_width / 2
                    self.frame_width = self.old_frame_x + self.frame_pen_width / 2
            case HandlePosition.TOP_MIDDLE:
                self.frame_y = event.y() - self.mouse_delta_y
                self.frame_height = self.old_mouse_y - event.y() + self.old_frame_height

                if self.frame_height < self.frame_min_height:
                    self.frame_y = self.old_frame_y - self.frame_min_height
                    self.frame_height = self.frame_min_height
                if self.frame_y <= 0 - self.frame_pen_width / 2:
                    self.frame_y = 0 - self.frame_pen_width / 2
                    self.frame_height = self.old_frame_y + self.frame_pen_width / 2
            case HandlePosition.TOP_RIGHT:
                self.frame_y = event.y() - self.mouse_delta_y
                self.frame_width = event.x() - self.old_mouse_x + self.old_frame_width
                self.frame_height = self.old_mouse_y - event.y() + self.old_frame_height

                if self.frame_width < self.frame_min_width:
                    self.frame_width = self.frame_min_width
                if self.frame_height < self.frame_min_height:
                    self.frame_y = self.old_frame_y - self.frame_min_height
                    self.frame_height = self.frame_min_height
                if self.frame_y <= 0 - self.frame_pen_width / 2:
                    self.frame_y = 0 - self.frame_pen_width / 2
                    self.frame_height = self.old_frame_y + self.frame_pen_width / 2
                if (self.frame_x + self.frame_width - self.frame_pen_width / 2) > self.screen_width:
                    self.frame_width = self.screen_width + self.frame_pen_width / 2 - self.frame_x
            
            case HandlePosition.MIDDLE_RIGHT:
                self.frame_width = event.x() - self.old_mouse_x + self.old_frame_width

                if self.frame_width < self.frame_min_width:
                    self.frame_width = self.frame_min_width
                
                if (self.frame_x + self.frame_width - self.frame_pen_width / 2) > self.screen_width:
                    self.frame_width = self.screen_width + self.frame_pen_width / 2 - self.frame_x
            case HandlePosition.BOTTOM_RIGHT:
                self.frame_width = event.x() - self.old_mouse_x + self.old_frame_width
                self.frame_height = event.y() - self.old_mouse_y + self.old_frame_height

                if self.frame_width < self.frame_min_width:
                    self.frame_width = self.frame_min_width
                
                if self.frame_height < self.frame_min_height:
                    self.frame_height = self.frame_min_height
                if (self.frame_x + self.frame_width - self.frame_pen_width / 2) > self.screen_width:
                    self.frame_width = self.screen_width + self.frame_pen_width / 2 - self.frame_x
                if (self.frame_y + self.frame_height - self.frame_pen_width / 2) > self.screen_height:
                    self.frame_height = self.screen_height + self.frame_pen_width / 2 - self.frame_y
            case HandlePosition.BOTTOM_MIDDLE:
                self.frame_height = event.y() - self.old_mouse_y + self.old_frame_height
                if self.frame_height < self.frame_min_height:
                    self.frame_height = self.frame_min_height
                if (self.frame_y + self.frame_height - self.frame_pen_width / 2) > self.screen_height:
                    self.frame_height = self.screen_height + self.frame_pen_width / 2 - self.frame_y
            case HandlePosition.BOTTOM_LEFT:
                self.frame_x = event.x() - self.mouse_delta_x
                self.frame_width = self.old_mouse_x - event.x() + self.old_frame_width
                self.frame_height = event.y() - self.old_mouse_y + self.old_frame_height

                if self.frame_width < self.frame_min_width:
                    self.frame_x = self.old_frame_x - self.frame_min_width
                    self.frame_width = self.frame_min_width
                if self.frame_height < self.frame_min_height:
                    self.frame_height = self.frame_min_height
                if self.frame_x <= 0 - self.frame_pen_width / 2:
                    self.frame_x = 0 - self.frame_pen_width / 2
                    self.frame_width = self.old_frame_x + self.frame_pen_width / 2
                if (self.frame_y + self.frame_height - self.frame_pen_width / 2) > self.screen_height:
                    self.frame_height = self.screen_height + self.frame_pen_width / 2 - self.frame_y
            case HandlePosition.MIDDLE_LEFT:
                self.frame_x = event.x() - self.mouse_delta_x
                self.frame_width = self.old_mouse_x - event.x() + self.old_frame_width

                if self.frame_width < self.frame_min_width:
                    self.frame_x = self.old_frame_x - self.frame_min_width
                    self.frame_width = self.frame_min_width
                if (self.frame_x <= 0 - self.frame_pen_width / 2):
                    self.frame_x = 0 - self.frame_pen_width / 2
                    self.frame_width = self.old_frame_x + self.frame_pen_width / 2
            case HandlePosition.MIDDLE:
                delta_x = (self.old_frame_x - self.frame_pen_width / 2 - self.frame_width / 2) - self.old_mouse_x
                delta_y = (self.old_frame_y - self.frame_pen_width / 2 - self.frame_height / 2) - self.old_mouse_y

                self.frame_x = event.x() - self.frame_width / 2 + self.frame_pen_width / 2 + delta_x
                self.frame_y = event.y() - self.frame_height / 2 + self.frame_pen_width / 2 + delta_y

                if self.frame_y <= 0 - self.frame_pen_width / 2:
                    self.frame_y = 0 - self.frame_pen_width /2 
                if self.frame_x <= 0 - self.frame_pen_width / 2:
                    self.frame_x = 0 - self.frame_pen_width / 2
                if (self.frame_x + self.frame_width - self.frame_pen_width / 2) > self.screen_width:
                    self.frame_x = self.screen_width - self.frame_width + self.frame_pen_width / 2
                if (self.frame_y + self.frame_height - self.frame_pen_width / 2) > self.screen_height:
                    self.frame_y = self.screen_height - self.frame_height + self.frame_pen_width / 2
        self.repaint()
        self.update()

        if self.handle_press != HandlePosition.NO_HANDLE:
            return
        
        regionToLeft = QRect(self.frame_x - self.radius - 1, self.frame_y - self.radius - 1, self.radius *2 + 2, self.radius *2 + 2)
        if regionToLeft.contains(event.pos()):
            self.setCursor(Qt.ClosedHandCursor)
            self.handle_under_mouse = HandlePosition.TOP_LEFT
            return
        
        regionTopMiddle = QRect(self.frame_x + self.frame_width / 2 - self.radius - 1, self.frame_y - self.radius - 1, self.radius *2 + 2, self.radius *2 + 2)
        if regionTopMiddle.contains(event.pos()):
            self.setCursor(Qt.ClosedHandCursor)
            self.handle_under_mouse = HandlePosition.TOP_MIDDLE
            return
        
        regionTopRight = QRect(self.frame_x + self.frame_width - self.radius - 1, self.frame_y - self.radius - 1, self.radius *2 + 2, self.radius *2 + 2)
        if regionTopRight.contains(event.pos()):
            self.setCursor(Qt.ClosedHandCursor)
            self.handle_under_mouse = HandlePosition.TOP_RIGHT
            return
        regionRightMiddle = QRect(self.frame_x + self.frame_width - self.radius - 1, self.frame_y + self.frame_height / 2 - self.radius - 1, self.radius *2 + 2, self.radius *2 + 2)
        if regionRightMiddle.contains(event.pos()):
            self.setCursor(Qt.ClosedHandCursor)
            self.handle_under_mouse = HandlePosition.MIDDLE_RIGHT
            return
        regionMiddle = QRect(self.frame_x + self.frame_width/ 2 - self.radius - self.pen_width / 2,
                            self.frame_y + self.frame_height/ 2 - self.radius - self.pen_width / 2,
                            self.radius *2 + self.pen_width, self.radius *2 + self.pen_width)
        if regionMiddle.contains(event.pos()):
            self.setCursor(Qt.ClosedHandCursor)
            self.handle_under_mouse = HandlePosition.MIDDLE
            return
        
        area_selector_button = ArrowButton()
        regionButtomRight = QRect(self.frame_x + self.frame_width - area_selector_button.get_width_half(), self.frame_y + self.frame_height - area_selector_button.get_width_half(), area_selector_button.get_width_half() * 2, area_selector_button.get_width_half() * 2)
        if regionButtomRight.contains(event.pos()):
            self.setCursor(Qt.ClosedHandCursor)
            self.handle_under_mouse = HandlePosition.BOTTOM_RIGHT
            return
        
        regionButtomMiddle = QRect(self.frame_x + self.frame_width / 2 - area_selector_button.get_width_half(), self.frame_y + self.frame_height - area_selector_button.get_width_half(), area_selector_button.get_width_half() * 2, area_selector_button.get_width_half() * 2)
        if regionButtomMiddle.contains(event.pos()):
            self.setCursor(Qt.ClosedHandCursor)
            self.handle_under_mouse = HandlePosition.BOTTOM_MIDDLE
            return
        
        regionButtomLeft = QRect(self.frame_x - area_selector_button.get_width_half(), self.frame_y + self.frame_height - area_selector_button.get_width_half(), area_selector_button.get_width_half() * 2, area_selector_button.get_width_half() * 2)
        if regionButtomLeft.contains(event.pos()):
            self.setCursor(Qt.ClosedHandCursor)
            self.handle_under_mouse = HandlePosition.BOTTOM_LEFT
            return
        
        regionLeftMiddle = QRect(self.frame_x - area_selector_button.get_width_half(), self.frame_y + self.frame_height / 2 - area_selector_button.get_width_half(), area_selector_button.get_width_half() * 2, area_selector_button.get_width_half() * 2)
        if regionLeftMiddle.contains(event.pos()):
            self.setCursor(Qt.ClosedHandCursor)
            self.handle_under_mouse = HandlePosition.MIDDLE_LEFT
            return
        
        region_ok_button = QRect(self.frame_x + self.frame_width / 2 - area_selector_button.get_width_half(), self.frame_y + self.frame_height + 2 * area_selector_button.get_width_half(), area_selector_button.get_width_half() * 2, area_selector_button.get_width_half() * 2)
        if region_ok_button.contains(event.pos()):
            self.setCursor(Qt.PointingHandCursor)
            self.handle_under_mouse = HandlePosition.OK_HANDLE
            return
        self.unsetCursor()
        self.handle_under_mouse = HandlePosition.NO_HANDLE


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.LeftButton:
            return
        self.handle_press = HandlePosition.NO_HANDLE
        self.update()

    def paintEvent(self, event: QPaintEvent):
        pixmap: QPixmap = QPixmap(self.screen_width, self.screen_height)
        pixmap.fill(Qt.transparent)
        painter_pixmap = QPainter()
        painter_pixmap.begin(pixmap)
        painter_pixmap.setRenderHint(QPainter.Antialiasing, True)

        if not self.detection_mode:
            painter_pixmap = self.handle_top_left(painter_pixmap)
            painter_pixmap = self.handle_top_middle(painter_pixmap)
            painter_pixmap = self.handle_top_right(painter_pixmap)
            painter_pixmap = self.handle_right_middle(painter_pixmap)
            painter_pixmap = self.handle_bottom_left(painter_pixmap)
            painter_pixmap = self.handle_bottom_middle(painter_pixmap)
            painter_pixmap = self.handle_bottom_right(painter_pixmap)
            painter_pixmap = self.handle_left_middle(painter_pixmap)
            painter_pixmap = self.handle_middle(painter_pixmap)
            painter_pixmap = self.handle_ok_button(painter_pixmap)

        painter_pixmap = self.draw_frame(painter_pixmap)
        painter_pixmap.end()
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(QPoint(0,0), pixmap)
        painter.end()
        self.setMask(pixmap.mask())

    def init(self):
        self.frame_screen = QGuiApplication.primaryScreen()
        self.resize(self.frame_screen.size().width(), self.frame_screen.size().height())
        self.screen_width = self.frame_screen.size().width()
        self.screen_height = self.frame_screen.size().height()

        self.move(self.frame_screen.geometry().x(), self.frame_screen.geometry().y())

        self.frame_width = self.frame_min_width
        self.frame_height = self.frame_min_height
        self.frame_x = (self.screen_width / 2 - self.frame_width / 2)- self.frame_pen_width / 2
        self.frame_y = (self.screen_height / 2 - self.frame_height / 2)- self.frame_pen_width / 2
    
    def draw_frame(self, painter: QPainter) -> QPainter:
        pen = QPen(self.frame_color, self.frame_pen_width)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        brush = QBrush(Qt.transparent, Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawRect(self.frame_x, self.frame_y, self.frame_width, self.frame_height)
        return painter

    
    def set_frame_color(color: QColor):
        pass

    def show_size(self, painter: QPainter):
        pass

    def handle_top_left(self, painter: QPainter) -> QPainter:
        button = ArrowButton()
        painter.drawPixmap(self.frame_x - self.radius, self.frame_y - self.radius, button.get_pixmap_handle(DegrePosition.TOP_LEFT))
        return painter

    def handle_top_middle(self, painter:  QPainter) -> QPainter:
        button = ArrowButton()
        painter.drawPixmap(self.frame_x + self.frame_width / 2 - button.get_width_half(), self.frame_y - button.get_width_half(), button.get_pixmap_handle(DegrePosition.TOP_MIDDLE))
        return painter

    def handle_top_right(self, painter:  QPainter) -> QPainter:
        button = ArrowButton()
        painter.drawPixmap(self.frame_x + self.frame_width - button.get_width_half(), self.frame_y - button.get_width_half(), button.get_pixmap_handle(DegrePosition.TOP_RIGHT))
        return painter

    def handle_bottom_left(self, painter:  QPainter) -> QPainter:
        button = ArrowButton()
        painter.drawPixmap(self.frame_x - button.get_width_half(), self.frame_y  + self.frame_height - button.get_width_half(), button.get_pixmap_handle(DegrePosition.BOTTOM_LEFT))
        return painter

    def handle_bottom_middle(self, painter:  QPainter) -> QPainter:
        button = ArrowButton()
        painter.drawPixmap(self.frame_x+ self.frame_width / 2 - button.get_width_half(), self.frame_y  + self.frame_height - button.get_width_half(), button.get_pixmap_handle(DegrePosition.BOTTOM_MIDDLE))
        return painter

    def handle_right_middle(self, painter:  QPainter) -> QPainter:
        button = ArrowButton()
        painter.drawPixmap(self.frame_x + self.frame_width - button.get_width_half(), self.frame_y + self.frame_height / 2 - button.get_width_half(), button.get_pixmap_handle(DegrePosition.MIDDLE_RIGHT))
        return painter
    
    def handle_left_middle(self, painter:  QPainter) -> QPainter:
        button = ArrowButton()
        painter.drawPixmap(self.frame_x - button.get_width_half(), self.frame_y + self.frame_height / 2 - button.get_width_half(), button.get_pixmap_handle(DegrePosition.MIDDLE_LEFT))
        return painter

    def handle_bottom_right(self, painter: QPainter) -> QPainter:
        button = ArrowButton()
        painter.drawPixmap(self.frame_x + self.frame_width - button.get_width_half(), self.frame_y + self.frame_height - button.get_width_half(), button.get_pixmap_handle(DegrePosition.BOTTOM_RIGHT))
        return painter

    def handle_middle(self, painter: QPainter) -> QPainter:
        button = ArrowButton()
        painter.drawPixmap(self.frame_x + self.frame_width / 2 - button.get_width_half(),
                       self.frame_y + self.frame_height / 2 - button.get_width_half(),
                       button.get_button());
        painter.drawPixmap(self.frame_x + self.frame_width / 2 - button.get_width_half(), self.frame_y + self.frame_height / 2 - button.get_width_half(), button.get_arrow(DegrePosition.TOP_MIDDLE))
        painter.drawPixmap(self.frame_x + self.frame_width / 2 - button.get_width_half(), self.frame_y + self.frame_height / 2 - button.get_width_half(), button.get_arrow(DegrePosition.MIDDLE_RIGHT))
        painter.drawPixmap(self.frame_x + self.frame_width / 2 - button.get_width_half(), self.frame_y + self.frame_height / 2 - button.get_width_half(), button.get_arrow(DegrePosition.BOTTOM_MIDDLE))
        painter.drawPixmap(self.frame_x + self.frame_width / 2 - button.get_width_half(), self.frame_y + self.frame_height / 2 - button.get_width_half(), button.get_arrow(DegrePosition.MIDDLE_LEFT))
        return painter
    
    def handle_ok_button(self, painter: QPainter) -> QPainter:
        button = ArrowButton()
        painter.drawPixmap(self.frame_x + self.frame_width / 2 - button.get_width_half(), self.frame_y + self.frame_height + 2 * button.get_width_half(), button.get_check_button())
        painter.drawText(self.frame_x + self.frame_width / 2 -  button.get_width_half() * 0.4 , self.frame_y + self.frame_height + 3.4 * self.radius,"OK")
        return painter
    
    def get_x(self):
        return self.frame_x 

    def get_y(self):
        return self.frame_y

    def get_width(self):
        return (self.frame_width - self.frame_pen_width) * self.frame_screen.devicePixelRatio()

    def get_height(self):
        return (self.frame_height - self.frame_pen_width) * self.frame_screen.devicePixelRatio()

    def get_react(self):
        return QRect(self.get_x(), self.get_y(), self.get_width(), self.get_height())

    def closeEvent(self, event: QCloseEvent):
        self.area_selected.emit(self.get_react())
        event.accept()