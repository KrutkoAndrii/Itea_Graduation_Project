from PyQt5 import QtWidgets
from database.db_tools import connect_to_db,\
                              is_sql_no_result, sql_result


class ShowUsers(QtWidgets.QDialog):
    # Window for showing all users in base and banned /renew his access
    def __init__(self, db_login, db_password, db_location, parent=None):
        super(ShowUsers, self).__init__(parent)
        self.db_login = db_login
        self.db_password = db_password
        self.db_location = db_location
        self.table_users = QtWidgets.QTableWidget(self)
        self.table_users.setRowCount(0)
        self.table_users.setColumnCount(2)
        self.table_users.setObjectName("table_users")
        self.button_ban = QtWidgets.QPushButton('Ban', self)
        self.button_ban.clicked.connect(self.ban)
        self.button_renew = QtWidgets.QPushButton('Renew', self)
        self.button_renew.clicked.connect(self.renew)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table_users)
        layout.addWidget(self.button_ban)
        layout.addWidget(self.button_renew)
        self.draw_table()

    def draw_table(self):
        # Pull all users to table
        conn = connect_to_db('things', self.db_login, self.db_password,
                             self.db_location)
        sql_text = "select rolname from pg_catalog.pg_roles where" \
                   " rolcanlogin = TRUE"
        data_in = sql_result(conn, sql_text)
        self.table_users.setRowCount(len(data_in))
        self.table_users.setColumnCount(1)
        row = 0
        for items_line in data_in:
            item_value = str(items_line[0])
            self.table_users.setItem(row, 0,
                                     QtWidgets.QTableWidgetItem(item_value))
            row += 1
        self.table_users.setHorizontalHeaderLabels(['Name'])

    def renew(self):
        # rollbak access to user
        if not self.table_users.currentRow() == -1:
            current_user = self.table_users.item(
                           self.table_users.currentRow(),
                           0).text()
            conn = connect_to_db('things', self.db_login, self.db_password,
                                 self.db_location)
            sql_text = "ALTER ROLE {} VALID UNTIL '01/01/3000';". \
                       format(current_user)
            if not is_sql_no_result(conn, sql_text):
                QtWidgets.QMessageBox.warning(self, 'Error', 'Don`t renew!')
            else:
                self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Choose a user!')

    def ban(self):
        # Ban users
        if not self.table_users.currentRow() == -1:
            current_user = self.table_users.item(
                                            self.table_users.currentRow(),
                                            0).text()
            conn = connect_to_db('things', self.db_login, self.db_password,
                                 self.db_location)
            sql_text = "ALTER ROLE {} VALID UNTIL '01/01/1000';".\
                       format(current_user)
            if not is_sql_no_result(conn, sql_text):
                QtWidgets.QMessageBox.warning(self, 'Error', 'Don`t ban!')
            else:
                self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Choose a user!')


if __name__ == "__main__":
    print(" This module not for running!")
