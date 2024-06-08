import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QMouseEvent
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

class WarningPopup(QWidget):
    confirm_signal = pyqtSignal()

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
        close_button.clicked.connect(self.exitAction)
        close_button_layout.addWidget(close_button, alignment=Qt.AlignRight)
        layout.addLayout(close_button_layout)

        warning_label = QLabel('WARNING:', self)
        warning_label.setFont(QFont('Arial', 14, QFont.Bold))
        warning_label.setStyleSheet('color: #FF5656')
        warning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning_label, alignment=Qt.AlignCenter)

        message_label = QLabel(
            '<br>The file you have selected is not recognized as a memory dump!<br>'
            'If you still wish to use the file then press <span style="color: #FF8956;">confirm</span><br>', self)
        message_label.setFont(QFont('Arial', 12))
        message_label.setStyleSheet('color: white; font-weight: 500;')
        message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(message_label, alignment=Qt.AlignCenter)

        # Add a spacer to push the buttons to the bottom
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        confirm_button = QPushButton('Confirm', self)
        confirm_button.setFont(QFont('Arial', 12))
        confirm_button.setStyleSheet('background-color: #FF8956; border: none; color: black')
        confirm_button.setFlat(True)
        confirm_button.setFixedSize(100, 40)
        confirm_button.clicked.connect(self.confirmAction)
        button_layout.addWidget(confirm_button)

        exit_button = QPushButton('EXIT', self)
        exit_button.setFont(QFont('Arial', 12))
        exit_button.setStyleSheet('background-color: #FF5656; border: none; color: black')
        exit_button.setFlat(True)
        exit_button.setFixedSize(100, 40)
        exit_button.clicked.connect(self.exitAction)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def confirmAction(self):
        print('Confirmed warning message')
        self.confirm_signal.emit()
        self.close()

    def exitAction(self):
        print('Exit warning message')
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
