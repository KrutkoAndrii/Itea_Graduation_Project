''' Main form application '''
from PyQt5 import QtWidgets, QtGui
from visualisation.mframe import Ui_MainWindow
from database.db_tools import connect_to_db, sql_result, is_sql_no_result
from visualisation.add_users import CreateUser
from visualisation.show_all_users import ShowUsers
from visualisation.add_properties import AddAttribute, AddColor
from visualisation.add_goods import AddItem


class TheMainForm(QtWidgets.QMainWindow, Ui_MainWindow):
    # Main form application
    def __init__(self, db_login, db_password, db_location):
        super().__init__()
        self.__labels = ['', 'Good', 'Color', 'Density', 'Width']
        self.__labels_attributes = ['', '', 'Name', 'Value']
        self.db_login = db_login
        self.db_password = db_password
        self.db_location = db_location
        self.setupUi(self)
        self.actionCreate_user.triggered.connect(self.create_user)
        self.actionColor.triggered.connect(self.add_color)
        self.pB_Find.clicked.connect(self.filter_goods)
        self.pB_Insert.clicked.connect(self.add_item)
        self.pB_Delete.clicked.connect(self.del_item)
        self.pB_Update.clicked.connect(self.update_item)
        self.tableWidget.setHorizontalHeaderLabels(self.__labels)
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.cellClicked[int, int].connect(self.clickedRowColumn)
        self.pB_fich_insert.clicked.connect(self.add_attribute)
        self.pB_fish_delete.clicked.connect(self.del_attribute)
        self.actionAll_user.triggered.connect(self.show_all_user)
        self.renew_item()

    def filter_goods(self):
        self.renew_item(True)

    def update_item(self):
        # a
        if not self.tableWidget.currentRow() == -1:
            window_add_item = AddItem(self.db_login, self.db_password,
                                      self.db_location,
                                      self.tableWidget.item(self.tableWidget.
                                                            currentRow(),
                                                            0).text())
            window_add_item.exec_()
            self.renew_item()

    def add_color(self):
        # Adding new color
        window_add_item = AddColor(self.db_login, self.db_password, self.
                                   db_location)
        window_add_item.exec_()
        self.renew_item()

    def del_attribute(self):
        # Delete current attribute
        if not self.tableWidget_2.currentRow() == -1:
            conn = connect_to_db('things', self.db_login, self.db_password,
                                 self.db_location)
            sql_text = "DELETE FROM \"attributes\" WHERE \"id\" = {};".format(
                self.tableWidget_2.item(self.tableWidget_2.
                                        currentRow(), 0).text())
            if not is_sql_no_result(conn, sql_text):
                QtWidgets.QMessageBox.warning(self, 'Error', 'Data don`t '
                                              ' delete!')
            else:
                self.renew_item()
                QtWidgets.QMessageBox.warning(self, 'Information', 'OK!')
                self.renew_attributes()
        else:
            QtWidgets.QMessageBox.warning(self, 'Information', 'Select '
                                          'attribute!')

    def add_attribute(self):
        # Show windows fo adding new attributes for good
        if not self.tableWidget.currentRow() == -1:
            window_add_item = AddAttribute(self.db_login,
                                           self.db_password,
                                           self.db_location,
                                           self.tableWidget.item(self.
                                                                 tableWidget.
                                                                 currentRow(),
                                                                 0).text())
            window_add_item.exec_()
            self.renew_item()
            self.renew_attributes()
        else:
            QtWidgets.QMessageBox.warning(self, 'Information', 'Select '
                                                               ' good!')

    def renew_attributes(self):
        # Select attributes for good when user clicked to cells
        if not self.tableWidget.currentRow() == -1:
            current_good = self.tableWidget.item(
                                            self.tableWidget.currentRow(),
                                            0).text()
            conn = connect_to_db('things', self.db_login, self.db_password,
                                 self.db_location)
            sql_text = "SELECT g.Id, g.goods,g.name, g.value FROM\
                        attributes as g WHERE g.goods = {}".\
                       format(current_good)
            data_in = sql_result(conn, sql_text)
            self.tableWidget_2.setRowCount(len(data_in))
            self.tableWidget_2.setColumnCount(4)
            row = 0
            for items_line in data_in:
                for col in range(0, 4):
                    item_value = str(items_line[col])
                    self.tableWidget_2.setItem(row, col,
                                               QtWidgets.
                                               QTableWidgetItem(item_value))
                row += 1
            self.tableWidget_2.setColumnHidden(0, True)
            self.tableWidget_2.setColumnHidden(1, True)
            self.tableWidget_2.setHorizontalHeaderLabels(self.
                                                         __labels_attributes)
        else:
            QtWidgets.QMessageBox.warning(self, 'Information', 'Select '
                                          ' good!')

    def del_item(self):
        # Delete current good and its attributes
        if not self.tableWidget.currentRow() == -1:
            conn = connect_to_db('things', self.db_login, self.db_password,
                                 self.db_location)
            sql_text = "DELETE FROM \"goods\" WHERE \"id\" = {};".format(
                   self.tableWidget.item(self.tableWidget.
                                         currentRow(), 0).text())
            if not is_sql_no_result(conn, sql_text):
                QtWidgets.QMessageBox.warning(self, 'Error', 'Data don`t '
                                              ' delete!')
            else:
                self.renew_item()
                QtWidgets.QMessageBox.warning(self, 'Information', 'OK!')
        else:
            QtWidgets.QMessageBox.warning(self, 'Information', 'Select '
                                          ' good!')

    def clickedRowColumn(self, r, c):
        # Pull data for serching
        self.lineEdit.setText(self.tableWidget.item(r, c).text())
        self.renew_attributes()

    def add_item(self):
        # Call window for adding new good
        window_add_item = AddItem(self.db_login,
                                  self.db_password,
                                  self.db_location)
        window_add_item.exec_()
        self.renew_item()

    def show_all_user(self):
        window_add_item = ShowUsers(self.db_login,
                                    self.db_password,
                                    self.db_location)
        window_add_item.exec_()
        self.renew_item()

    def renew_item(self, filtered=False):
        conn = connect_to_db('things', self.db_login, self.db_password,
                             self.db_location)
        sql_text = "SELECT g.Id, g.name,c.name, g.density, g.width \
                    FROM goods as g left join color c on g.color = c.id "
        if self.lineEdit.text() and not self.tableWidget.currentRow() == -1 \
                and filtered:
            field_name = {1: "g.name", 2: "c.name", 3: "g.density",
                          4: "g.width"}
            sql_text += "WHERE {} = '{}'".format(
                         field_name[self.tableWidget.currentColumn()],
                         self.lineEdit.text())
        data_in = sql_result(conn, sql_text)
        self.tableWidget.setRowCount(len(data_in))
        self.tableWidget.setColumnCount(5)
        row = 0
        for items_line in data_in:
            for col in range(0, 5):
                item_value = str(items_line[col])
                self.tableWidget.setItem(row, col,
                                         QtWidgets.
                                         QTableWidgetItem(item_value))
            row += 1
        self.tableWidget.setColumnHidden(0, True)
        self.tableWidget.setHorizontalHeaderLabels(self.__labels)

    def create_user(self):
        # Call window for creating user
        window_create_user = CreateUser(self.db_login,
                                        self.db_password,
                                        self.db_location)
        window_create_user.exec_()


if __name__ == "__main__":
    print(" This module not for running!")
