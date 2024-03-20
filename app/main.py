# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 20:03:57 2024

@author: Digital Zone
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from login_ui import Ui_MainWindow  # Import the generated class
from tableWindow import TableWindow  # Import the generated class

class LoginWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        # Set up the user interface from the generated class
        self.setupUi(self)

        # Set flags to remove the default title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Connect the maximizeRestoreAppBtn button to the maximize_window method
        self.maximizeRestoreAppBtn.clicked.connect(self.maximize_window)

        # Connect the closeAppBtn button to the close method
        self.closeAppBtn.clicked.connect(self.close)

        # Connect the minimizeAppBtn button to the showMinimized method
        self.minimizeAppBtn.clicked.connect(self.showMinimized)
        
        self.btnLogin.clicked.connect(self.login)
    def login(self):
        email = self.txtEmail.text()
        key = self.txtAPIKey.text()
        user={
            "Email":email,
            "Key":key
            }
        
        if(email == "a" and key=="1"):
            # if(adminDL().searchAdmin(login)):
            self.close()
            self.newq = TableWindow(user)
            self.newq.show()

    # Define the mousePressEvent method to handle mouse button press events
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    def maximize_window(self):
        # If the window is already maximized, restore it
        if self.isMaximized():
            self.showNormal()
        # Otherwise, maximize it
        else:
            self.showMaximized()

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
