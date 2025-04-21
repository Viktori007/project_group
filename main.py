import sys

from PyQt6 import QtGui, QtWidgets, uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel, QMessageBox

from db import Database
from project_selector import ProjectSelector

application_window: QtWidgets.QMainWindow = None


class AuthUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(AuthUi, self).__init__()
        self.label_icon: QLabel = None
        self.auth_btn: QPushButton = None
        self.login_edit: QLineEdit = None
        self.password_edit: QLineEdit = None
        self.resize(700, 700)

        uic.loadUi('UI/auth.ui', self)

        self.auth_btn.clicked.connect(self.auth)
        self.login_edit.returnPressed.connect(self.auth)
        self.password_edit.returnPressed.connect(self.auth)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.label_icon.setPixmap(QtGui.QPixmap("ui/images/logo-02.jpg"))
        self.label_icon.setScaledContents(True)
        self.setWindowIcon(QIcon("ui/images/logo-02.jpg"))
        self.setWindowTitle("Авторизация")

    def auth(self):
        login = self.login_edit.text().strip()
        password = self.password_edit.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите данные!")
            return

        user = Database.auth(login, password)

        if user is None:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
            return

        if user["role"] != "Дизайнер":
            QMessageBox.warning(self, "Ошибка", "Нет доступа")
            return
        self.pr_win = ProjectSelector(self)
        self.pr_win.show()
        self.hide()


if __name__ == "__main__":
    sys.argv += ['-platform', 'windows:darkmode=1']

    app = QtWidgets.QApplication(sys.argv)
    Database()
    application_window = AuthUi()
    application_window.show()
    sys.exit(app.exec())
