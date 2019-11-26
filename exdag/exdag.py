## useful references:
# http://www.science.smith.edu/dftwiki/index.php/PyQt5_Tutorial:_A_Window_Application_with_File_IO
# https://stackoverflow.com/questions/35951988/pyqt-and-progress-bar-during-long-process
# https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable
# https://realpython.com/pyinstaller-python/

## Used file name
# input location "/Users/thomaskeel/Dev/misc_company_projects/Keel Toys/python_gui/test.csv/Users/thomaskeel/Dev/misc_company_projects/Keel Toys/python_gui/test.csv/Users/thomaskeel/Dev/misc_company_projects/Keel Toys/python_gui/test.csv"
# output location: "/Users/thomaskeel/Dev/misc_company_projects/Keel Toys/python_gui/new_test.csv"

import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QFileDialog, QVBoxLayout, QLabel, QComboBox, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
import pandas
import time

TIME_LIMIT = 100

# Translate asset paths to useable format for PyInstaller
def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath('.'), relative_path)



def testAnalysis(data):
    new_data = data.sum()
    return new_data


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = ' Main Window – Keel Toys Data Transformation'
        self.left = 10
        self.top = 100
        self.width = 600
        self.height = 200
        self.initUI()
    
    def loadFile(self):
        """
            * Check the file exists and is a csv
            * Maybe use: os.path.normcase
        """
        fileName =  self.textbox.text()
        print(fileName[-4:])
        fileName = fileName.replace("\\ ", " ") # replace backslash with spaces
        try:
            assert fileName[-4:] == '.csv'
        except Exception as e:
            QMessageBox.question(self, 'Unknown File – Keel Toys Data Transformation App', "Please enter a file that exists and ends in \'.csv\'", QMessageBox.Ok, QMessageBox.Ok)
            print("Please enter a file that exists and ends in \'.csv\'")
            return
            # sys.exit()
        try:
            # set timeout
            self.data = pandas.read_csv(fileName)
            QMessageBox.question(self, 'Please Wait – Keel Toys Data Transformation App', "Starting \'%s\', please wait" % (self.comboBox.currentText()), QMessageBox.Ok, QMessageBox.Ok)
            print(self.data.head())
        except Exception as e:
            QMessageBox.question(self, 'Unknown File - Keel Toys Data Transformation App', "File doesn't exist", QMessageBox.Ok, QMessageBox.Ok)
            return
        return 


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.inputLabel = QLabel(self)
        self.outputLabel = QLabel(self)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(120, 20)
        self.textbox.resize(200,20)
        self.inputLabel.setText("Input file path:")
        self.inputLabel.move(10, 15)
        
        self.output_box = QLineEdit(self)
        self.output_box.move(120, 80)
        self.output_box.resize(200,20)
        self.outputLabel.setText("Output file path:")
        self.outputLabel.move(10, 75)

        # Create a button in the window
        self.button = QPushButton('Start Process', self)
        self.button.resize(130,30)
        self.button.move(320,16)
        # self.button.clicked.connect(self.processProgress)
        
        # create a dropdown box for functionality:
        self.comboBox = QComboBox(self)
        self.comboBox.addItem(" ")
        self.comboBox.addItem("Process 1")
        self.comboBox.addItem("Process 2")
        self.comboBox.addItem("Process 3")
        self.comboBox.addItem("Process 4")
        self.comboBox.addItem("Process 5")
        self.comboBox.move(450, 17)

        # create a progress bar
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 150, 250, 20)
        self.progress.setMaximum(100)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        # textboxValue = self.textbox.text()
        ## check that the output box exists
        # load file 
        print("TO REMOVE: Process ==", self.comboBox.currentText())
        if self.comboBox.currentText() != " ":
            self.calc = External()  ## set up progress bar
            self.calc.countChanged.connect(self.onCountChanged)
            self.calc.start()
            self.loadFile()
        else:
            QMessageBox.question(self, 'Error – Keel Toys Data Transformation App', "Please select a process", QMessageBox.Ok, QMessageBox.Ok)
            return
        
        try:
            assert len(self.output_box.text()) > 0
        except:
            QMessageBox.question(self, 'Error – Keel Toys Data Transformation App', "Please enter a path for the output file", QMessageBox.Ok, QMessageBox.Ok)

        print("TO REMOVE: carrying out analysis:")
        try:
            if self.comboBox.currentText() == "Process 1":
                self.new_data = testAnalysis(self.data)
            else:
                self.new_data = pandas.DataFrame([])
        except Exception as e:
            print(e)

        print("TO REMOVE: save the file")
        self.saveFile()
        # self.textbox.setText("") # reset back to normal

    def onCountChanged(self, value):
        self.progress.setValue(value)
        

    def saveFile(self):
        """
            * To save the csv file
        """
        output_filename = self.output_box.text()
        try:
            assert output_filename[-4:] == '.csv'
        except Exception as e:
            QMessageBox.question(self, 'Incorrect output – Keel Toys Data Transformation App', "Please enter an output file location that ends in \'.csv\'", QMessageBox.Ok, QMessageBox.Ok)
            print("TO REMOVE: output file error")
            return
        # name = QFileDialog.getSaveFileName(self, 'Save File',"Comma-seperated values (*.csv)")
        # name.setNameFilters(["*.csv"])
        # name.selectNameFilter("Comma-seperated values (*.csv)")
        try:
            self.new_data.to_csv(output_filename)
            QMessageBox.question(self, 'Operation complete – Keel Toys Data Transformation App', "Operation Complete!", QMessageBox.Ok, QMessageBox.Ok)
        except Exception as e:
            print(e)
            QMessageBox.question(self, 'Incorrect output – Keel Toys Data Transformation App', "Unable to create new file", QMessageBox.Ok, QMessageBox.Ok)
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
            count +=1
            time.sleep(.1)
            self.countChanged.emit(count)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


