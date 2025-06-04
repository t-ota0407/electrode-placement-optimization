import sys
from PyQt5.QtWidgets import QApplication
from vispy import app
from views.main_window import MainWindow

app.use_app('pyqt5')

if __name__ == '__main__':
    _app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(_app.exec_())
