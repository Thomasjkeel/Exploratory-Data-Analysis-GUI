## useful references:
# http://www.science.smith.edu/dftwiki/index.php/PyQt5_Tutorial:_A_Window_Application_with_File_IO
# https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable
# https://realpython.com/pyinstaller-python/

import os
import sys
from pathlib import Path
import time

# for developing the PyQt5 app
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QFileDialog, QVBoxLayout, QLabel, QComboBox, QProgressBar, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, Qt

# for the Exploratory Data Analysis
import pandas
import processes # location with the apps processes



TIME_LIMIT = 100


def resource_path(relative_path):
    # Translate asset paths to useable format for PyInstaller
  if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath('.'), relative_path)


class App(QMainWindow):
    def __init__(self):
        # testing run == 'will automatically fill the inputs'
        super().__init__()
        self.title = 'Simple Exploratory Data Analysis GUI'
        self.left = 10
        self.top = 100
        self.width = 700
        self.height = 200
        self.save_the_file = False

        try:
            assert sys.argv[1]
            # will automatically fill in the inputs for testing
            self.testing_run = sys.argv[1]
        except:
            self.testing_run = ""
        self.initUI()

    def loadFile(self):
        """
            * Check the file exists and is a csv
            * Maybe use: os.path.normcase
        """
        fileName = self.textbox.text()
        print(fileName[-4:])
        # replace backslash with spaces
        fileName = fileName.replace("\\ ", " ")
        try:
            assert fileName[-4:] == '.csv'
        except Exception as e:
            QMessageBox.question(self, 'Unknown File',
                                 "Please enter a file that exists and ends in \'.csv\'", QMessageBox.Ok, QMessageBox.Ok)
            return False
            # sys.exit()
        try:
            assert len(self.output_box.text()) > 0
        except:
            QMessageBox.question(self, 'Error',
                                 "Please enter a path for the output folder", QMessageBox.Ok, QMessageBox.Ok)
            return False

        try:
            # set timeout
            self.data = pandas.read_csv(fileName)  # ,parse_dates=['DocDate']
            QMessageBox.question(self, 'Please Wait', "Starting \'%s\', please wait" % (self.comboBox.currentText()), QMessageBox.Ok, QMessageBox.Ok)
            print(self.data.head())
        except Exception as e:
            QMessageBox.question(self, 'Unknown File', "File doesn't exist", QMessageBox.Ok, QMessageBox.Ok)
            return False
        return True

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.inputLabel = QLabel(self)
        self.outputLabel = QLabel(self)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(120, 20)
        self.textbox.resize(200, 20)
        self.textbox.setReadOnly(True)
        self.inputLabel.setText("Input file path:")
        self.inputLabel.move(10, 15)

        self.output_box = QLineEdit(self)
        self.output_box.move(120, 80)
        self.output_box.resize(200, 20)
        self.output_box.setReadOnly(True)
        self.outputLabel.setText("Output folder:")
        self.outputLabel.move(10, 75)

        if self.testing_run == 'test':  # TODO: remove for full version
            self.textbox.setText("test.csv")
            self.output_box.setText("test_output_folder")

        # Create a button in the window
        self.button = QPushButton('Start Process', self)
        self.button.resize(130, 35)
        self.button.move(360, 17)
        # self.button.clicked.connect(self.processProgress)

        # FILE EXPLORER button
        self.fileExplore = QPushButton('...', self)
        self.fileExplore.resize(35, 30)
        self.fileExplore.move(325, 20)

        self.outputDialog = QPushButton('...', self)
        self.outputDialog.resize(35, 30)
        self.outputDialog.move(325, 80)

        # create a dropdown box for functionality:
        self.comboBox = QComboBox(self)
        self.comboBox.addItem(" ")
        self.comboBox.addItem("Process 1")
        self.comboBox.addItem("Process 2")
        self.comboBox.addItem("Process 3")
        self.comboBox.addItem("Process 4")
        self.comboBox.resize(150, 30)
        self.comboBox.move(510, 17)

        # create a progress bar
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 150, 250, 20)
        self.progress.setMaximum(100)

        # create checkbox for opening file after complete
        self.open_in_web = QCheckBox("Open file?", self)
        self.open_in_web.stateChanged.connect(self.clickBox)
        self.open_in_web.move(520, 70)
        self.open_in_web.resize(300, 40)

        # create checkbox for multiple plots or not
        self.multiple = QCheckBox("Allow interactivity?", self)
        self.multiple.stateChanged.connect(self.clickBox)
        self.multiple.move(370, 70)
        self.multiple.resize(150, 40)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.fileExplore.clicked.connect(self.chooseFile)
        self.outputDialog.clicked.connect(self.openDirectoryDialog)
        self.show()

    def clickBox(self, state):
        if state == Qt.Checked:
            pass
        else:
            pass

    @pyqtSlot()
    def chooseFile(self):
        # TODO: move to seperate func
        self.textbox.setText(self.openFileNameDialog())

    @pyqtSlot()
    def on_click(self):
        # make sure file is not going to be saved by app unless specified
        self.save_the_file = False
        # textboxValue = self.textbox.text()
        ## check that the output box exists
        # load file

        print("TO REMOVE: Process ==", self.comboBox.currentText())
        if self.comboBox.currentText() != " ":
            self.calc = External()  # set up progress bar
            self.calc.start()
        else:
            QMessageBox.question(self, 'Error!',"Please select a process", QMessageBox.Ok, QMessageBox.Ok)
            return
        try:
            assert self.loadFile()
        except:
            print("Unable to load file")
            return

        ## Specific Processes
        if self.comboBox.currentText() == "Process 1":
            self.save_the_file = True
            try:
                self.calc.countChanged.connect(self.onCountChanged)
                self.new_data = processes.testAnalysis(self.data)
            except Exception as e:
                QMessageBox.information(self, 'Operation Failed',"Operation Failed!", QMessageBox.Ok, QMessageBox.Ok)
                self.new_data = pandas.DataFrame([])
                return

        elif self.comboBox.currentText() == "Process 1":
            self.save_the_file = True
            try:
                self.calc.countChanged.connect(self.onCountChanged)
                self.new_data = processes.testAnalysis(self.data)
            except Exception as e:
                QMessageBox.information(
                    self, 'Operation Failed', "Operation Failed!", QMessageBox.Ok, QMessageBox.Ok)
                self.new_data = pandas.DataFrame([])
                return

        elif self.comboBox.currentText() == "Process 1":
            self.save_the_file = True
            try:
                self.calc.countChanged.connect(self.onCountChanged)
                self.new_data = processes.testAnalysis(self.data)
            except Exception as e:
                QMessageBox.information(
                    self, 'Operation Failed', "Operation Failed!", QMessageBox.Ok, QMessageBox.Ok)
                self.new_data = pandas.DataFrame([])
                return

        elif self.comboBox.currentText() == "Process 4":
            self.save_the_file = True
            try:
                self.calc.countChanged.connect(self.onCountChanged)
                self.new_data = processes.testAnalysis(self.data)
            except Exception as e:
                QMessageBox.information(
                    self, 'Operation Failed', "Operation Failed!", QMessageBox.Ok, QMessageBox.Ok)
                self.new_data = pandas.DataFrame([])
                return

        if self.save_the_file:
            self.saveFile()

    def onCountChanged(self, value):
        self.progress.setValue(value)

    def openDirectoryDialog(self):
        directory_chosen = str(
            QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.output_box.setText(directory_chosen)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*);;CSV files (*.csv)", options=options)
        if fileName:
            return fileName

    def saveFile(self):
        """
            * To save the csv file
        """
        print("TO REMOVE: SAVING FILE...")

        output_dir = Path(self.output_box.text())

        try:
            self.new_data.to_csv(str(output_dir / 'output.csv'))
            QMessageBox.question(self, 'Operation complete – ExDag',
                                 "Operation Complete!", QMessageBox.Ok, QMessageBox.Ok)
        except Exception as e:
            QMessageBox.question(self, 'Incorrect output – ExDag',
                                 "Unable to create new file", QMessageBox.Ok, QMessageBox.Ok)
            return


class External(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)
    # fix multiple progress bars

    def run(self):
        count = 0
        while count < TIME_LIMIT:
            count += 1
            time.sleep(.1)
            self.countChanged.emit(count)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()
    sys.exit(app.exec_())
