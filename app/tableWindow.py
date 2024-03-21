# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 02:49:00 2024

@author: Digital Zone
"""

import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from main_ui import Ui_MainWindow  # Import the generated class

class TableWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, currentUser):
        super(TableWindow, self).__init__()
        self.setupUi(self)
        self.currentUser = currentUser
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.maximizeRestoreAppBtn.clicked.connect(self.maximize_window)
        self.closeAppBtn.clicked.connect(self.close)
        self.minimizeAppBtn.clicked.connect(self.showMinimized)
        self.load_countries()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    def maximize_window(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()



    def load_countries(self):
        try:
            # Read championship data from CSV file
            data_folder = "data"
            csv_file = os.path.join(data_folder, "championshipsWithCode.csv")
            if not os.path.exists(csv_file):
                raise FileNotFoundError("CSV file not found")
                    
            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file, encoding='latin1')
                
            # Extract unique country names and sort them alphabetically
            unique_countries = sorted(set(df['Country']))
                
            # Populate the country combo box
            self.cmbxCountry.addItems(unique_countries)
                
            # Connect the country combo box signal to the method to load leagues
            self.cmbxCountry.currentIndexChanged.connect(self.load_leagues)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    
    def load_leagues(self):
        try:
            selected_country = self.cmbxCountry.currentText()
            csv_file = os.path.join("data", "championshipsWithCode.csv")
            
            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file, encoding='latin1')
            
            # Extract leagues associated with the selected country
            selected_country_leagues = df[df['Country'] == selected_country]['League']
            
            # Populate the league combo box
            self.cmbxLeague.clear()  # Clear previous items
            self.cmbxLeague.addItems(selected_country_leagues)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableWindow("User")
    window.show()
    sys.exit(app.exec_())
