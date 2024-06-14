import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, \
    QSizePolicy, QDialog
from PyQt5.QtGui import QFont, QMouseEvent
from PyQt5.QtCore import Qt, pyqtSignal, QTimer


class ErrorNotSelected(QDialog):
    ok_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dragging = False
        self.flash_timer = QTimer(self)
        self.flash_timer.timeout.connect(self.toggle_flash)
        self.is_flashing_red = False

    def initUI(self):
        self.setWindowTitle('Error')
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
        close_button.clicked.connect(self.okAction)
        close_button_layout.addWidget(close_button, alignment=Qt.AlignRight)
        layout.addLayout(close_button_layout)

        warning_label = QLabel('ERROR:', self)
        warning_label.setFont(QFont('Arial', 14, QFont.Bold))
        warning_label.setStyleSheet('color: #FF5656')
        warning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning_label, alignment=Qt.AlignCenter)

        message_label = QLabel(
            '<br>File or plugin not selected<br>'
            '<span style="font-weight: 50; color: #E3E0E0; font-size: 20px;">Hint: Try uploading a file or select a plugin to run</span><br>'
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

        self.ok_signal.emit()
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
    ex = ErrorNotSelected()
    ex.show()
    sys.exit(app.exec_())