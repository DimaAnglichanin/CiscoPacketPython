import sys
from PyQt5.QtWidgets import QApplication, QGraphicsSceneMouseEvent, QMainWindow, QDesktopWidget, QPushButton, QGraphicsScene, QGraphicsView, \
    QTableWidget, QTableWidgetItem, QInputDialog, QGraphicsRectItem,QLabel,QLineEdit,QVBoxLayout,QDialog,QComboBox
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QPointF, QRectF,pyqtSignal,QTimer,pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem

from dialogs import RouterDialog, PCDialog, SwitchDialog


class Object(QGraphicsRectItem): 
    def __init__(self,rect : QRectF, pen : QPen, brush : QBrush):
        super().__init__(rect)
        self.setFlag(self.ItemIsMovable)
        self.setPen(pen)
        self.setBrush(brush)
    def get_type(self) -> str:
        return self.type

class Router(Object):
    def __init__(self):
        super().__init__(QRectF(QPointF(0, 0), QPointF(30, 30)),QPen(Qt.black),QBrush(Qt.gray))       
        self.dialog = RouterDialog()
        self.type = "router"
    def mouseDoubleClickEvent(self,event):
        self.dialog.exec()
class Switch(Object):
    def __init__(self):
        super().__init__(QRectF(QPointF(0, 0), QPointF(50, 30)),QPen(Qt.black),QBrush(Qt.white)   )     
        self.type = "switch"
        self.dialog = SwitchDialog()
    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.dialog.exec()
class PC(Object):
    def __init__(self):
        super().__init__(QRectF(QPointF(0, 0), QPointF(30, 30)),QPen(Qt.black),QBrush(Qt.gray))
        self.dialog = PCDialog()
        self.type = "pc"
    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.dialog.exec()
def create_object_of_type(type : str) -> Object:
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
        
        # Создаем список объектов
        self.objects = []

        self.show()

    def add_object(self, object_type):
        obj = create_object_of_type(object_type)
        self.scene.addItem(obj)
        self.objects.append(obj)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())