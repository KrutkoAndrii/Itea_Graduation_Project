''' form  for creating/ updating goods '''
from PyQt5 import QtWidgets
from database.db_tools import connect_to_db, is_sql_no_result, sql_result


class AddItem(QtWidgets.QDialog):
    # Create window for adding/ updating goods
    def __init__(self, db_login, db_password, db_location, id_good=None,
                 parent=None):
        super(AddItem, self).__init__(parent)
        self.db_login = db_login
        self.db_password = db_password
        self.db_location = db_location
        self.id_good = id_good
        self.setWindowTitle('Add item')
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText('Name')
        self.label_density = QtWidgets.QLabel(self)
        self.label_density.setText('density')
        self.label_width = QtWidgets.QLabel(self)
        self.label_width.setText('width')
        self.label_color = QtWidgets.QLabel(self)
        self.label_color.setText('Color')
        self.textName = QtWidgets.QLineEdit(self)
        self.text_density = QtWidgets.QLineEdit(self)
        self.text_width = QtWidgets.QLineEdit(self)
        self.combo = QtWidgets.QComboBox(self)
        self.combo.setEditable(False)
        conn = connect_to_db('things', self.db_login, self.db_password,
                             self.db_location)
        sql_text = "SELECT c.name FROM color c"
        data_in = sql_result(conn, sql_text)
        items_for_combo = [i[0] for i in data_in]
        self.combo.addItems(items_for_combo)
        if self.id_good:
            self.button_create = QtWidgets.QPushButton('Update', self)
        else:
            self.button_create = QtWidgets.QPushButton('Add', self)
        self.button_create.clicked.connect(self.push_create)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label_name)
        layout.addWidget(self.textName)
        layout.addWidget(self.label_color)
        layout.addWidget(self.combo)
        layout.addWidget(self.label_density)
        layout.addWidget(self.text_density)
        layout.addWidget(self.label_width)
        layout.addWidget(self.text_width)
        layout.addWidget(self.button_create)
        if self.id_good:
            self.select_item()

    def select_item(self):
        # set value to window for changing
        conn = connect_to_db('things', self.db_login, self.db_password,
                             self.db_location)
        sql_text = "SELECT g.Id, g.name,c.name, g.density, g.width \
                   FROM goods as g left join color c on g.color = c.id WHERE \
                   g.id = {};".format(self.id_good)
        data_in = sql_result(conn, sql_text)
        self.textName.setText(data_in[0][1])
        index = self.combo.findText(data_in[0][2])
        if index >= 0:
            self.combo.setCurrentIndex(index)
        self.text_density.setText(str(data_in[0][3]))
        self.text_width.setText(str(data_in[0][4]))

    def push_create(self):
        # For creating/ updating item in database
        if self.id_good:
            conn = connect_to_db('things', self.db_login, self.db_password,
                                 self.db_location)
            sql_text = "SELECT c.Id FROM color c WHERE c.NAME = '{}';".format(
                self.combo.currentText())
            color_id = [i[0] for i in sql_result(conn, sql_text)]
            conn = connect_to_db('things', self.db_login, self.db_password,
                                 self.db_location)
            sql_text = "UPDATE \"goods\" SET \"name\" = '{}', \"color\" = {},\
                        \"density\" = {},  \"width\" = {} WHERE \"id\" = {}".\
                       format(
                              self.textName.text(),
                              color_id[0],
                              self.text_density.text(),
                              self.text_width.text(),
                              self.id_good)
            if not is_sql_no_result(conn, sql_text):
                QtWidgets.QMessageBox.warning(self, 'Error', 'Data don`t '
                                                             ' insert!')
            self.accept()
        else:
            conn = connect_to_db('things', self.db_login, self.db_password,
                                 self.db_location)
            sql_text = "SELECT c.Id FROM color c WHERE c.NAME = '{}';".format(
                   self.combo.currentText())
            color_id = [i[0] for i in sql_result(conn, sql_text)]
            conn = connect_to_db('things', self.db_login, self.db_password,
                                 self.db_location)
            sql_text = "INSERT INTO goods (\"id\", \"name\", \"color\",  \
                   \"density\",\"width\") VALUES (DEFAULT, \
                   '{}', {}, {},{} );".format(
                   self.textName.text(),
                   color_id[0],
                   self.text_density.text(),
                   self.text_width.text())
            if not is_sql_no_result(conn, sql_text):
                QtWidgets.QMessageBox.warning(self, 'Error', 'Data don`t '
                                              ' insert!')
            else:
                self.accept()


if __name__ == "__main__":
    print(" This module not for running!")
