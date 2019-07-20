import sys
# Импорт numpy
import numpy
# Импорт интерфейса
from PyQt5 import QtCore, QtGui, QtWidgets

# Массив значений
mass = numpy.array(
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]], float)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    NpTable = QtWidgets.QTableView()

    NpTable.show()
    sys.exit(app.exec_())