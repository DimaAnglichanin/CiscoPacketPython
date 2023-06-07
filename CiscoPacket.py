import sys
from PyQt5.QtWidgets import QApplication, QGraphicsSceneMouseEvent, QMainWindow, QDesktopWidget, QPushButton, QGraphicsScene, QGraphicsView, \
    QTableWidget, QTableWidgetItem, QInputDialog, QGraphicsRectItem, QLabel, QLineEdit, QVBoxLayout, QDialog
from PyQt5.QtGui import QColor, QBrush, QPen, QPainter, QMouseEvent
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal


class Object(QGraphicsRectItem):
    def __init__(self, rect: QRectF, pen: QPen, brush: QBrush):
        super().__init__(rect)
        self.setFlag(self.ItemIsMovable)
        self.setPen(pen)
        self.setBrush(brush)

    def get_type(self) -> str:
        return self.type


class Router(Object):
    def __init__(self):
        super().__init__(QRectF(QPointF(0, 0), QPointF(30, 30)), QPen(Qt.black), QBrush(Qt.gray))
        self.dialog = QDialog()
        self.type = "router"
        self.label = QLabel("Router Dialog")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.dialog.setLayout(layout)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.dialog.exec()


class Switch(Object):
    def __init__(self):
        super().__init__(QRectF(QPointF(0, 0), QPointF(50, 30)), QPen(Qt.yellow), QBrush(Qt.white))
        self.type = "switch"
        self.dialog = QDialog()
        self.label = QLabel("Switch Dialog")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.dialog.setLayout(layout)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.dialog.exec()


class PC(Object):
    def __init__(self):
        super().__init__(QRectF(QPointF(0, 0), QPointF(30, 30)), QPen(Qt.black), QBrush(Qt.yellow))
        self.dialog = QDialog()
        self.type = "pc"
        self.label = QLabel("PC Dialog")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.dialog.setLayout(layout)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.dialog.exec()


class Connection(QGraphicsRectItem):
    def __init__(self, start_item, end_item):
        super().__init__(QRectF())
        self.start_item = start_item
        self.end_item = end_item
        self.setZValue(-1)  # Установка z-позиции ниже объектов
        self.pen = QPen(Qt.red)
        self.pen.setWidth(2)
        self.setPen(self.pen)

    def update(self):
        start_pos = self.start_item.pos() + QPointF(self.start_item.rect().width() / 2, self.start_item.rect().height() / 2)
        end_pos = self.end_item.pos() + QPointF(self.end_item.rect().width() / 2, self.end_item.rect().height() / 2)
        self.setRect(QRectF(start_pos, end_pos))

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        super().paint(painter, option, widget)


def create_object_of_type(type: str) -> Object:
    if type == 'switch':
        obj = Switch()
    elif type == 'router':
        obj = Router()
    elif type == 'pc':
        obj = PC()
    return obj


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Определяем размеры экрана пользователя
        screen = QDesktopWidget().screenGeometry()
        width, height = screen.width(), screen.height()
        # Устанавливаем размеры окна
        self.setGeometry(0, 0, width, height)

        self.setWindowTitle('My Application')
        self.setStyleSheet("background-color: #4d4dff;")

        # Создаем сцену для отрисовки объектов
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, width, height)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setBackgroundBrush(QBrush(QColor(220, 220, 220)))

        # Добавляем кнопки
        self.add_switch_button = QPushButton('Добавить SWITCH', self)
        self.add_switch_button.clicked.connect(lambda: self.add_object('switch'))
        self.add_switch_button.setGeometry(10, 50, 150, 30)

        self.add_router_button = QPushButton('Добавить маршрутизатор', self)
        self.add_router_button.clicked.connect(lambda: self.add_object('router'))
        self.add_router_button.setGeometry(10, 100, 150, 30)

        self.add_pc_button = QPushButton('Добавить PC', self)
        self.add_pc_button.clicked.connect(lambda: self.add_object('pc'))
        self.add_pc_button.setGeometry(10, 150, 150, 30)

        # Создаем список объектов и связей
        self.objects = []
        self.connections = []
        self.current_connection = None

        self.show()

    def add_object(self, object_type):
        obj = create_object_of_type(object_type)
        self.scene.addItem(obj)
        self.objects.append(obj)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            obj = self.scene.itemAt(event.pos(), self.view.transform())
            if isinstance(obj, Object):
                if self.current_connection is None:
                    # Если нет активной связи, выбираем объект начала связи
                    obj.setFlag(QGraphicsRectItem.ItemIsMovable, False)
                    self.current_connection = Connection(obj, None)
                    self.connections.append(self.current_connection)
                    self.scene.addItem(self.current_connection)
                else:
                    # Если уже выбран объект начала связи, выбираем объект конца связи
                    self.current_connection.end_item = obj
                    self.current_connection.update()
                    self.current_connection = None
                    obj.setFlag(QGraphicsRectItem.ItemIsMovable, True)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self.current_connection is not None:
            # Если связь была начата, но не завершена при отпускании кнопки мыши, удаляем связь
            self.scene.removeItem(self.current_connection)
            self.current_connection.start_item.setFlag(QGraphicsRectItem.ItemIsMovable, True)
            self.connections.remove(self.current_connection)
            self.current_connection = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())
