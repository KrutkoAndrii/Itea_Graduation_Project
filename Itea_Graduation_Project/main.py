''' In this file main form for aplication'''
import sys
from PyQt5 import QtWidgets
from database.db_tools import get_ini_file, is_check_db_instance, create_db
from visualisation.logining import LoginUser
from visualisation.main_form import TheMainForm


class Message(QtWidgets.QDialog):
    # Show yes/no dialog
    def is_chose_message(self, title, message='None', ):
        reply = QtWidgets.QMessageBox.question(self, title, message,
                                               QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False

    def message_ok(self, title, message='None', ):
        QtWidgets.QMessageBox.question(self, title, message,
                                       QtWidgets.QMessageBox.Ok,
                                       QtWidgets.QMessageBox.Ok)


def main():
    app = QtWidgets.QApplication(sys.argv)
    db_name, db_user, db_password, db_location = get_ini_file()

    exist = is_check_db_instance(db_name, db_user, db_password, db_location)
    message = Message()
    if not exist:
        if message.is_chose_message('Question', 'Main DB doesn`t exist.\n'
                                    'Do you wont create the base?'):
            create_db(db_name, db_user, db_password, db_location)
        else:
            message.message_ok("Warning!", "Its cant work!\n Bye!")
            exit(1)
    login = LoginUser(db_location)
    if login.exec_() == QtWidgets.QDialog.Accepted:
        login_user = login.db_login
        password_user = login.db_password
        window = TheMainForm(login_user, password_user, db_location)
        window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
