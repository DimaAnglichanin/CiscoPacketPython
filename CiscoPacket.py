import sys
from PyQt5.QtWidgets import QApplication, QGraphicsSceneMouseEvent, QMainWindow, QDesktopWidget, QPushButton, QGraphicsScene, QGraphicsView, \
    QTableWidget, QTableWidgetItem, QInputDialog, QGraphicsRectItem, QLabel, QLineEdit, QVBoxLayout, QDialog, QComboBox
from PyQt5.QtGui import QColor, QBrush, QPen, QPainter
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal, QTimer, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsLineItem

from dialogs import RouterDialog, PCDialog, SwitchDialog


class Object(QGraphicsRectItem):
    def __init__(self, rect: QRectF, pen: QPen, brush: QBrush):
        super().__init__(rect)
        self.setFlag(self.ItemIsMovable)
        self.setPen(pen)
        self.setBrush(brush)
        self.connections = []

    def get_type(self) -> str:
        return self.type

    def add_connection(self, connection):
        self.connections.append(connection)

    def remove_connection(self, connection):
        self.connections.remove(connection)

    def update_connections(self):
        for connection in self.connections:
            connection.update()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.update_connections()
        return super().itemChange(change, value)


class Connection(QGraphicsLineItem):
    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.start_item.add_connection(self)
        self.end_item.add_connection(self)
        self.update()

    def update(self):
        start_pos = self.start_item.pos() + QPointF(self.start_item.rect().width() / 2,
                                                    self.start_item.rect().height() / 2)
        end_pos = self.end_item.pos() + QPointF(self.end_item.rect().width() / 2,
                                                self.end_item.rect().height() / 2)
        self.setLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())


class Router(Object):
    def __init__(self):
        super().__init__(QRectF(QPointF(0, 0), QPointF(30, 30)), QPen(Qt.black), QBrush(Qt.gray))
        self.dialog = RouterDialog()
        self.type = "router"

    def mouseDoubleClickEvent(self, event):
        self.dialog.exec()


class Switch(Object):
    def __init__(self):
        super().__init__(QRectF(QPointF(0, 0), QPointF(50, 30)), QPen(Qt.yellow), QBrush(Qt.white))
        self.type = "switch"
        self.dialog = SwitchDialog()

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        self.dialog.exec()


class PC(Object):
    def __init__(self):
        super().__init__(QRectF(QPointF(0, 0), QPointF(30, 30)), QPen(Qt.black), QBrush(Qt.yellow))
        self.dialog = PCDialog()
        self.type = "pc"

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        self.dialog.exec()


def create_object_of_type(type: str) -> Object:
    if type == 'switch':
        obj = Switch()
    elif type == 'router':
        obj = Router()
    elif type == 'pc':
        obj = PC()
    return obj


class MyView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if isinstance(item, Object):
                item.setFlag(QGraphicsItem.ItemIsMovable, True)
                item.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if isinstance(item, Object):
                item.setFlag(QGraphicsItem.ItemIsMovable, False)
                item.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, False)

        super().mouseReleaseEvent(event)


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
        self.view = MyView(self.scene, self)
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

        # Создаем список объектов
        self.objects = []

        self.connections = []
        self.current_connection = None

        self.show()

    def add_object(self, object_type):
        obj = create_object_of_type(object_type)
        self.scene.addItem(obj)
        self.objects.append(obj)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            obj = self.scene.itemAt(event.pos(), self.view.transform())
            if isinstance(obj, Object):
                self.current_connection = Connection(obj, None)
                self.connections.append(self.current_connection)

    def mouseMoveEvent(self, event):
        if self.current_connection:
            self.current_connection.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            obj = self.scene.itemAt(event.pos(), self.view.transform())
            if isinstance(obj, Object) and self.current_connection:
                self.current_connection.end_item = obj
                self.current_connection.update()
                self.current_connection = None
            elif self.current_connection in self.connections:
                self.scene.removeItem(self.current_connection)
                self.current_connection.start_item.remove_connection(self.current_connection)
                self.current_connection.end_item.remove_connection(self.current_connection)
                self.connections.remove(self.current_connection)
                self.current_connection = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())
