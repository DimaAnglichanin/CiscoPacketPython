import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QPushButton, QGraphicsScene, QGraphicsView, \
    QTableWidget, QTableWidgetItem, QInputDialog, QGraphicsRectItem
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QPointF, QRectF




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