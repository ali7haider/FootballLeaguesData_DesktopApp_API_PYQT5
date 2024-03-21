# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 02:49:00 2024

@author: Digital Zone
"""

import sys
import os
sys.path.append("api")
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QTableWidgetItem,QFileDialog
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QMouseEvent
from main_ui import Ui_MainWindow  # Import the generated class
from loadingScreen import LoadingScreen  # Import the generated class
from api.main import main
import datetime
import csv


DATA_PATH = "data"


class TableWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, currentUser):
        super(TableWindow, self).__init__()
        self.setupUi(self)
        self.currentUser = currentUser
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.maximizeRestoreAppBtn.clicked.connect(self.maximize_window)
        self.stackedWidget.setCurrentIndex(0)

        self.closeAppBtn.clicked.connect(self.close)
        self.minimizeAppBtn.clicked.connect(self.showMinimized)
        self.load_countries()
        self.btnBack.clicked.connect(lambda: self.change_page(0))
        self.btnExportCSV.clicked.connect(self.export_csv)  # Connect the button to the export_csv function

        
        self.massdm.clicked.connect(self.on_btnLoad_clicked) 
    def export_csv(self):
        try:
            # Get the file path to save the CSV file
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")

            if file_path:
                # Get the data from the table
                data = []

                # Extract header labels
                header = []
                for column in range(self.footballTable.columnCount()):
                    header.append(self.footballTable.horizontalHeaderItem(column).text())
                data.append(header)

                # Extract data rows
                for row in range(self.footballTable.rowCount()):
                    row_data = []
                    for column in range(self.footballTable.columnCount()):
                        item = self.footballTable.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append("")
                    data.append(row_data)

                # Write the data to the CSV file with UTF-8 encoding
                with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(data)

                QMessageBox.information(self, "Success", "Data exported to CSV successfully.")

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    def change_page(self, index):
        self.stackedWidget.setCurrentIndex(index)
    def on_btnLoad_clicked(self):
        try:
            # Step 1: Retrieve selected values from combo boxes
            selectedCountry = self.cmbxCountry.currentText()
            selectedLeague = self.cmbxLeague.currentText()
            key = self.get_key(selectedCountry, selectedLeague)
    
            # Check if key is found
            if key:
                self.lblLoad.setText('Loading...Please Wait!')
                QApplication.processEvents()  # Process pending events to update GUI

                main(selectedCountry ,selectedLeague, key)
                # Load the CSV data into the footballTable
                csv_filename = f"{selectedCountry}_{selectedLeague}_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv"
                df = pd.read_csv(os.path.join(DATA_PATH, csv_filename))
                self.load_data_to_table(df)
                self.stackedWidget.setCurrentIndex(1)  # Change to page2 


            else:
                QMessageBox.warning(self, "Key not found", f"No key found for {selectedCountry} - {selectedLeague}")

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    def load_data_to_table(self, df):
        """
        Load data from a DataFrame to the footballTable.
        """
        # Clear existing data from the table
        self.footballTable.setRowCount(0)
        self.footballTable.setColumnCount(0)
        self.footballTable.horizontalHeader().setVisible(True)
        self.footballTable.verticalHeader().setVisible(True)

        # Set table column headers
        self.footballTable.setColumnCount(len(df.columns))
        self.footballTable.setHorizontalHeaderLabels(df.columns)

        # Populate the table with data
        for row in range(df.shape[0]):
            self.footballTable.insertRow(row)
            for col in range(df.shape[1]):
                self.footballTable.setItem(row, col, QTableWidgetItem(str(df.iloc[row, col])))

        # Resize columns to content
        self.footballTable.resizeColumnsToContents()
        

    def get_key(self, country, league):
        try:
            csv_file = os.path.join("data", "championshipsWithCode.csv")
            
            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file, encoding='latin1')
            
            # Search for the corresponding key based on the selected country and league
            key = df[(df['Country'] == country) & (df['League'] == league)]['Key'].values.tolist()
    
            # Return the key if found
            if key:
                return key[0]
            else:
                return None
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


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
            # QTimer.singleShot(3000, self.close_loading_screen)
    
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
