import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QMouseEvent
from PyQt5.QtCore import Qt, QPoint

class WarningPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dragging = False

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Warning')
        self.setGeometry(100, 100, 800, 300)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window header
        self.setStyleSheet('background-color: #262626;')

        layout = QVBoxLayout()

        close_button_layout = QHBoxLayout()
        close_button_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        close_button = QPushButton('X', self)
        close_button.setFont(QFont('Arial', 10, QFont.Bold))
        close_button.setStyleSheet('color: #FF5656; border: none; background: none;')
        close_button.setFixedSize(30, 30)
        close_button.setFlat(True)
        close_button.clicked.connect(self.okAction)
        close_button_layout.addWidget(close_button, alignment=Qt.AlignRight)
        layout.addLayout(close_button_layout)

        warning_label = QLabel('ERROR:', self)
        warning_label.setFont(QFont('Arial', 14, QFont.Bold))
        warning_label.setStyleSheet('color: #FF5656')
        warning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning_label, alignment=Qt.AlignCenter)

        message_label = QLabel(
            'The file you have selected is not recognized as a memory dump.<br>'
            'Please select a valid memory dump!<br><br>'
            '<span style="font-weight: 50; color: #E3E0E0; font-size: 20px;">Enable super user to use other file formats</span>'
            , self)
        message_label.setFont(QFont('Arial', 12))
        message_label.setStyleSheet('color: white; font-weight: 500;')
        message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(message_label, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        ok_button = QPushButton('OK', self)
        ok_button.setFont(QFont('Arial', 12))
        ok_button.setFlat(True)
        ok_button.setStyleSheet('background-color: #FF8956; border: none; color: black; font-weight: 500;')
        ok_button.setFixedSize(100, 40)
        ok_button.clicked.connect(self.okAction)
        button_layout.addWidget(ok_button, alignment=Qt.AlignRight)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def okAction(self):
        print('Confirmed error message')
        self.close()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WarningPopup()
    ex.show()
    sys.exit(app.exec_())


