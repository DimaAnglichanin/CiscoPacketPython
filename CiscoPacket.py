import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QPushButton, QGraphicsScene, QGraphicsView, \
    QTableWidget, QTableWidgetItem, QInputDialog, QGraphicsRectItem,QLabel,QLineEdit,QVBoxLayout,QDialog,QComboBox
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QPointF, QRectF


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

class Object:

    def get_type(self) -> str:
        return self.type

    def get_rect(self) -> QGraphicsRectItem:
        return self.rect

class Router(Object):
    def __init__(self):
        self.rect = QGraphicsRectItem(QRectF(QPointF(0, 0), QPointF(30, 30)))
        self.rect.setFlag(self.rect.ItemIsMovable)
        self.rect.setPen(QPen(Qt.black))
        self.rect.setBrush(QBrush(Qt.gray))
        
        self.type = "router"
class Switch(Object):
    def __init__(self):
        self.rect = QGraphicsRectItem(QRectF(QPointF(0, 0), QPointF(50, 30)))
        self.rect.setFlag(self.rect.ItemIsMovable)
        self.rect.setPen(QPen(Qt.black))
        self.rect.setBrush(QBrush(Qt.white))

        
        self.type = "switch"
class PC(Object):
    def __init__(self):
        self.rect = QGraphicsRectItem(QRectF(QPointF(0, 0), QPointF(30, 30)))
        self.rect.setFlag(self.rect.ItemIsMovable)
        self.rect.setPen(QPen(Qt.black))
        self.rect.setBrush(QBrush(Qt.gray))
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

        self.add_pc_button = QPushButton('ДBFKJU', self)
        self.add_pc_button.clicked.connect(lambda: self.dialog.exec())
        self.add_pc_button.setGeometry(10, 200, 150, 30)
        
        # Создаем список объектов
        self.objects = []

        self.show()

    def add_object(self, object_type):
        obj = create_object_of_type(object_type)
        self.scene.addItem(obj.get_rect())
        self.objects.append(obj)
    def open_table(self, obj):
    # Create a dialog to get the IP address from the user
        ip, ok = QInputDialog.getText(self, 'Enter IP Address', 'IP Address:', text=obj.data(0))
        if ok:
            # If the user clicks "OK", set the IP address as the object's data and update the table
            obj.setData(0, ip)
            self.update_table()

    def update_table(self):
    # Implement code to update the table with the data from the objects
    # You can use the "self.objects" list to get the data for each object
        pass
    def show_ip_table(self, obj):
        self.ip_table = QTableWidget(self)
        self.ip_table.setGeometry(0, 0, 300, 200)
        self.ip_table.setRowCount(1)
        self.ip_table.setColumnCount(2)
        self.ip_table.setHorizontalHeaderLabels(['Interface', 'IP address'])
        self.ip_table.setItem(0, 0, QTableWidgetItem('Ethernet 0'))
        self.ip_table.setItem(0, 1, QTableWidgetItem(''))
        self.ip_table.cellChanged.connect(lambda row, column: self.update)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())