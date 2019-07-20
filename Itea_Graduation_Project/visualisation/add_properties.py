''' Classes for creating attributes goods '''
from PyQt5 import QtWidgets
from database.db_tools import connect_to_db, is_sql_no_result


class AddColor(QtWidgets.QDialog):
    # Window for adding new color to dictionary
    def __init__(self, db_login, db_password, db_location, parent=None):
        super(AddColor, self).__init__(parent)
        self.db_login = db_login
        self.db_password = db_password
        self.db_location = db_location
        self.setWindowTitle('Add color')
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText('Name')
        self.textName = QtWidgets.QLineEdit(self)
        self.button_create = QtWidgets.QPushButton('Add', self)
        self.button_create.clicked.connect(self.push_create)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label_name)
        layout.addWidget(self.textName)
        layout.addWidget(self.button_create)

    def push_create(self):
        # Action creating color
        conn = connect_to_db('things', self.db_login, self.db_password,
                             self.db_location)
        sql_text = "INSERT INTO color (\"id\", \"name\") VALUES \
                 (DEFAULT, '{}')".format(self.textName.text())
        if not is_sql_no_result(conn, sql_text):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Data don`t '
                                          ' insert!')
        else:
            self.accept()


class AddAttribute(QtWidgets.QDialog):
    # Windows for creating new attribute
    def __init__(self, db_login, db_password, db_location, id_goods,
                 parent=None):
        super(AddAttribute, self).__init__(parent)
        self.db_login = db_login
        self.db_password = db_password
        self.db_location = db_location
        self.id_goods = id_goods
        self.setWindowTitle('Add attribute')
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText('Name')
        self.label_value = QtWidgets.QLabel(self)
        self.label_value.setText('value')
        self.text_name = QtWidgets.QLineEdit(self)
        self.text_value = QtWidgets.QLineEdit(self)
        self.button_create = QtWidgets.QPushButton('Add', self)
        self.button_create.clicked.connect(self.push_create)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label_name)
        layout.addWidget(self.text_name)
        layout.addWidget(self.label_value)
        layout.addWidget(self.text_value)
        layout.addWidget(self.button_create)

    def push_create(self):
        # Action for creating
        conn = connect_to_db('things', self.db_login, self.db_password,
                             self.db_location)
        sql_text = "INSERT INTO attributes (\"id\", \"name\", \"value\", \
                   \"goods\") VALUES (DEFAULT, '{}', {}, {});".format(
                   self.text_name.text(),
                   self.text_value.text(),
                   self.id_goods)
        if not is_sql_no_result(conn, sql_text):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Data don`t '
                                                         ' insert!')
        else:
            self.accept()


if __name__ == "__main__":
    print(" This module not for running!")
