''' Class for logining form '''
from PyQt5 import QtWidgets
from database.users_toos import is_check_db_password


class LoginUser(QtWidgets.QDialog):
    # Form for logining
    db_login = ''
    db_password = ''

    def __init__(self, location, parent=None):
        super(LoginUser, self).__init__(parent)
        self.location = location
        self.setWindowTitle('Connect')
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText('Name')
        self.label_password = QtWidgets.QLabel(self)
        self.label_password.setText('Password')
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.push_login)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label_name)
        layout.addWidget(self.textName)
        layout.addWidget(self.label_password)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def push_login(self):
        # Try to connect to database
        if is_check_db_password("things", self.textName.text(),
                                self.textPass.text(), self.location):
            self.db_login = self.textName.text()
            self.db_password = self.textPass.text()
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self,
                                          'Error', 'Bad user or password')


if __name__ == "__main__":
    print(" This module not for running!")
