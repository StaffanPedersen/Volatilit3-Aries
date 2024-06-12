import sys
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QMouseEvent
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, \
    QSizePolicy, QDialog


class WarningPopup(QDialog):
    confirm_signal = pyqtSignal()
    exit_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.dragging = False
        self.flash_timer = QTimer(self)
        self.flash_timer.timeout.connect(self.toggle_flash)
        self.is_flashing_red = False

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Warning')
        self.setGeometry(100, 100, 800, 300)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet('background-color: #262626;')
        self.setModal(True)

        layout = QVBoxLayout()

        close_button_layout = QHBoxLayout()
        close_button_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        close_button = QPushButton('X', self)
        close_button.setFont(QFont('Arial', 10, QFont.Bold))
        close_button.setStyleSheet('color: #FF5656; border: none; background: none;')
        close_button.setFixedSize(30, 30)
        close_button.setFlat(True)
        close_button.clicked.connect(self.on_exit)
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

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        confirm_button = QPushButton('Confirm', self)
        confirm_button.setFont(QFont('Arial', 12))
        confirm_button.setStyleSheet('background-color: #FF8956; border: none; color: black')
        confirm_button.setFlat(True)
        confirm_button.setFixedSize(100, 40)
        confirm_button.clicked.connect(self.on_confirm)
        button_layout.addWidget(confirm_button)

        exit_button = QPushButton('EXIT', self)
        exit_button.setFont(QFont('Arial', 12))
        exit_button.setStyleSheet('background-color: #FF5656; border: none; color: black')
        exit_button.setFlat(True)
        exit_button.setFixedSize(100, 40)
        exit_button.clicked.connect(self.on_exit)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_confirm(self):
        self.confirm_signal.emit()
        self.close()

    def on_exit(self):
        self.exit_signal.emit()
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

    def flash_background(self):
        self.flash_timer.start(500)

    def toggle_flash(self):
        if self.is_flashing_red:
            self.setStyleSheet('background-color: #262626;')
        else:
            self.setStyleSheet('background-color: #FF0000;')
        self.is_flashing_red = not self.is_flashing_red

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WarningPopup()
    ex.show()
    sys.exit(app.exec_())
