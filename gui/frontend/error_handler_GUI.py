from PyQt5.QtWidgets import QMessageBox


# display an error message in a QMessageBox
def show_error_message(parent, title, message):
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()
