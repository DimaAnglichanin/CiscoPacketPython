from PyQt5.QtWidgets import QDialog,QLineEdit,QLabel,QLayout,QVBoxLayout,QPushButton,QComboBox
class RouterDialog(QDialog):

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



class PCDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Внесите данные ПК')
        self.layout = QVBoxLayout()

        self.ipLabel = QLabel('IP-адрес:', self)
        self.ipLineEdit = QLineEdit(self)
        self.layout.addWidget(self.ipLabel)
        self.layout.addWidget(self.ipLineEdit)

        self.maskLabel = QLabel('Маска:', self)
        self.maskLineEdit = QLineEdit(self)
        self.layout.addWidget(self.maskLabel)
        self.layout.addWidget(self.maskLineEdit)

        self.gatewayLabel = QLabel('Шлюз:', self)
        self.gatewayLineEdit = QLineEdit(self)
        self.layout.addWidget(self.gatewayLabel)
        self.layout.addWidget(self.gatewayLineEdit)


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
class SwitchDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Внесите данные SWITCH')
        self.layout = QVBoxLayout()

        self.ipLabel = QLabel('IP-адрес:', self)
        self.ipLineEdit = QLineEdit(self)
        self.layout.addWidget(self.ipLabel)
        self.layout.addWidget(self.ipLineEdit)

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