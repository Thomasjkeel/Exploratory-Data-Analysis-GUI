from exdag import exdag
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QFileDialog, QVBoxLayout, QLabel, QComboBox, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
import pandas
import time

def main():
    app = QApplication(sys.argv)
    ex = exdag.App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
