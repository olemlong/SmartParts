import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class messageBox(QWidget):

    def __init__(self, message):
        super().__init__()
        #self.left = 10
        #self.top = 10
        #self.width = 320
        #self.height = 200
        self.initUI(message)

    def initUI(self, message):
        #self.setWindowTitle(message)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        QMessageBox.warning(QWidget(), message, message)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = messageBox("STOP RIGHT NOW, tnx!" )
