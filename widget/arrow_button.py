from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QPainter, QPainterPath, QPixmap, QPen, QBrush
from helper.enum import DegrePosition


class ArrowButton(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.pen_width = 2
        self.pen_width_half = self.pen_width / 2
        self.radius = 20
        self.diameter = self.radius * 2
        self.color = Qt.yellow
        self.color_selected = Qt.black

    def get_pixmap_handle(self, degree: DegrePosition) -> QPixmap:
        pixmap = QPixmap(self.diameter + self.pen_width, self.diameter + self.pen_width)
        pixmap.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        painter.setRenderHints(QPainter.Antialiasing, True)
        painter.drawPixmap(0, 0, self.get_button())
        painter.drawPixmap(0, 0, self.get_arrow(degree))
        painter.end()
        return pixmap
    
    def get_button(self) -> QPixmap:
        pixmap = QPixmap(self.diameter + self.pen_width, self.diameter + self.pen_width)
        pixmap.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        painter.setRenderHints(QPainter.Antialiasing, True)
        brush = QBrush()
        brush.setColor(self.color)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidthF(self.pen_width)
        painter.setPen(pen)
        painter.drawEllipse(self.pen_width_half, self.pen_width_half, self.diameter, self.diameter)
        painter.end()
        return pixmap
    
    def get_arrow(self, degree: DegrePosition) -> QPixmap:
        pixmap = QPixmap(self.diameter + self.pen_width, self.diameter+ self.pen_width)
        pixmap.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        painter.setRenderHints(QPainter.Antialiasing, True)
        painter.translate((self.diameter + self.pen_width) / 2, (self.diameter + self.pen_width)/ 2)
        painter.rotate(degree.value)
        pen = QPen()
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(self.color_selected)
        pen.setWidthF(self.pen_width)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        brush = QBrush()
        brush.setColor(self.color_selected)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        painter_path = QPainterPath()
        painter_path.moveTo(0, 0)
        painter_path.lineTo(  0, -self.radius + self.pen_width )
        painter_path.lineTo( -3, -self.radius + self.pen_width + 7 )
        painter_path.lineTo(  3, -self.radius + self.pen_width + 7 )
        painter_path.lineTo(  0, -self.radius + self.pen_width )
        painter.drawPath(painter_path)
        painter.end()
        return pixmap
    
    def get_width_half(self) -> int:
        return (self.diameter + self.pen_width )/ 2
