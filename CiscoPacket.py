import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QPushButton, QGraphicsScene, QGraphicsView, \
    QTableWidget, QTableWidgetItem, QInputDialog, QGraphicsRectItem,QLabel,QLineEdit,QVBoxLayout,QDialog,QComboBox
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QPointF, QRectF,pyqtSignal,QTimer,pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem


class InputDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Внесите данные маршрутизатора')
        self.layout = QVBoxLayout()

        self.ipLabel = QLabel('IP-адрес:', self)
        self.ipLineEdit = QLineEdit(self)
        self.layout.addWidget(self.ipLabel)
        self.layout.addWidget(self.ipLineEdit)

        self.dnsLabel = QLabel('DNS-имя:', self)
        self.dnsLineEdit = QLineEdit(self)
        self.layout.addWidget(self.dnsLabel)
        self.layout.addWidget(self.dnsLineEdit)

        self.portLabel = QLabel('Количество портов:', self)
        self.portComboBox = QComboBox(self)
        self.portComboBox.addItems(['4', '8', '16'])
        self.layout.addWidget(self.portLabel)
        self.layout.addWidget(self.portComboBox)

        self.okButton = QPushButton('OK', self)
        self.okButton.clicked.connect(self.acceptDialog)
        self.layout.addWidget(self.okButton)

        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.clicked.connect(self.rejectDialog)
        self.layout.addWidget(self.cancelButton)

        self.setLayout(self.layout)

    def acceptDialog(self):
        self.accept()

    def rejectDialog(self):
        self.reject()

class Object(QGraphicsRectItem): 
    def __init__(self,rect : QRectF, pen : QPen, brush : QBrush):
        super().__init__(rect)
        self.setFlag(self.ItemIsMovable)
        self.setPen(pen)
        self.setBrush(brush)
        self.dialog = InputDialog()
    def get_type(self) -> str:
        return self.type

    def mouseDoubleClickEvent(self,event):
        self.dialog.exec()

class Router(Object):
    def __init__(self):
        super().__init__(QRectF(QPointF(0, 0), QPointF(30, 30)),QPen(Qt.black),QBrush(Qt.gray))       
        self.type = "router"
    def mouseDoubleClickEvent(self,event):
        print("Данная обработка не поддерживается")
class Switch(Object):
    def __init__(self):
        super().__init__(QRectF(QPointF(0, 0), QPointF(50, 30)),QPen(Qt.black),QBrush(Qt.white)   )     
        self.type = "switch"
class PC(Object):
    def __init__(self):
        super().__init__(QRectF(QPointF(0, 0), QPointF(30, 30)),QPen(Qt.black),QBrush(Qt.gray))
        self.type = "pc"

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
        self.dialog = InputDialog()
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