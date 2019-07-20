
from PyQt5 import QtWidgets
from database.db_tools import connect_to_db
from database.users_toos import is_add_user


class CreateUser(QtWidgets.QDialog):
    # Create new users and set them role
    def __init__(self, db_login, db_password, db_location, parent=None):
        super(CreateUser, self).__init__(parent)
        self.db_login = db_login
        self.db_password = db_password
        self.db_location = db_location
        self.setWindowTitle('Create user')
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText('Name')
        self.label_password = QtWidgets.QLabel(self)
        self.label_password.setText('Password')
        self.label_password2 = QtWidgets.QLabel(self)
        self.label_password2.setText('Confirm password')
        self.label_role = QtWidgets.QLabel(self)
        self.label_role.setText('Role')
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass2 = QtWidgets.QLineEdit(self)
        self.combo = QtWidgets.QComboBox(self)
        self.combo.setEditable(False)
        self.combo.addItems([u"SuperAdmin", u"Admin", u"User"])
        self.button_create = QtWidgets.QPushButton('Create', self)
        self.button_create.clicked.connect(self.push_create)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label_name)
        layout.addWidget(self.textName)
        layout.addWidget(self.label_password)
        layout.addWidget(self.textPass)
        layout.addWidget(self.label_password2)
        layout.addWidget(self.textPass2)
        layout.addWidget(self.label_role)
        layout.addWidget(self.combo)
        layout.addWidget(self.button_create)

    def push_create(self):
        # Create user and check permission for this
        if self.textPass.text() == self.textPass2.text():
            conn = connect_to_db('things', self.db_login, self.db_password,
                                 self.db_location)
            if not is_add_user(conn, self.textName.text(),
                               self.textPass.text(),
                               self.combo.currentText()):
                QtWidgets.QMessageBox.warning(self, 'Error', 'You don`t have'
                                              ' permission!')
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self,
                                          'Error', 'Password not equal')


if __name__ == "__main__":
    print(" This module not for running!")
