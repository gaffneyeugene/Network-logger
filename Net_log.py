#-------------------------------------------------------------------------------
# Name:        Logging application
# Purpose:
#
# Author:      egaffney
#
# Created:     30/06/2023
# Copyright:   (c) egaffney 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import subprocess
import time
import sys
import os
import psutil
import multiprocessing
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QComboBox, QLineEdit, QGroupBox, QHBoxLayout
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QCheckBox, QLabel, QLineEdit, QFileDialog, QSizePolicy
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtGui import QColor, QIcon, QPainter, QBrush
from PyQt5.QtCore import Qt, QSize, QThread


class CircularButton(QPushButton):
    def __init__(self, text, color, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.color = color
        self.setFixedSize(120, 120)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(self.color)))
        painter.drawEllipse(0, 0, self.width(), self.height())
        painter.setPen(Qt.white)
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())




class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logging Application 0.1")
        self.setFixedSize(800, 400)

        # Create start and stop logging buttons
        self.start_button = CircularButton("Start Logging", "green")
        self.start_button.clicked.connect(self.start_logging)

        self.stop_button = CircularButton("Stop Logging", "red")
        self.stop_button.clicked.connect(self.stop_logging)
        self.stop_button.setEnabled(False)

        # Create file location label and button layout
        file_location_layout = QVBoxLayout()
        self.file_location_button = QPushButton("Select Directory", self)
        self.file_location_button.setFixedWidth(200)
        self.file_location_button.clicked.connect(self.select_directory)
        self.file_location_label = QLabel(self)
        # Create network adapter label
        self.network_adapter_label = QLabel(self)

        # Create network adapter dropdown
        self.network_adapter_dropdown = QComboBox(self)
        self.network_adapter_dropdown.setFixedWidth(200)
        self.network_adapter_dropdown.currentIndexChanged.connect(self.update_adapter_label)
        self.populate_network_adapters()
        self.selected_adapter = self.network_adapter_dropdown.currentText()

        self.name_file_location_label = QLabel(self)
        self.name_network_adapter_label = QLabel(self)
        self.name_ip_label = QLabel(self)

        # Create checkbox for using NET/REC
        self.use_net_rec_checkbox = QCheckBox("Log to NET/REC", self)

        self.use_net_rec_checkbox.stateChanged.connect(self.toggle_ip_widgets)



        # Create IP address label and text box
        self.ip_label = QLabel("Rec ip:", self)
        self.ip_label.setFixedWidth(200)
        self.ip_label.move(100, 50)

        self.ip_text_box = QLineEdit(self)
        self.ip_text_box.setFixedWidth(200)
        self.ip_text_box.textChanged.connect(self.update_ip_label)

        # Create layout for config widgets
        configuration_groupbox = QGroupBox("Configuration")
        configuration_groupbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        cfg_layout = QGridLayout()
        cfg_layout.setColumnMinimumWidth(0, 150)
        cfg_layout.addWidget(self.use_net_rec_checkbox,0,0)
        cfg_layout.addWidget(self.file_location_label,1,1)
        cfg_layout.addWidget(self.file_location_button,1,0)
        cfg_layout.addWidget(self.network_adapter_dropdown,2,0)
        cfg_layout.addWidget(self.network_adapter_label,2,1)
        cfg_layout.addWidget(self.ip_label,3,1)
        cfg_layout.addWidget(self.ip_text_box,3,0)

        self.ip_label.hide()
        self.ip_text_box.hide()

        # Create group box for file location and network adapter widgets
        file_location_group_box = QGroupBox("Configuration Settings")
        file_location_group_box.setLayout(cfg_layout)

        # Create layout for start and stop buttons
        button_layout = QHBoxLayout()
        button_layout = QGridLayout()
        button_layout.addWidget(self.start_button,0,0)
        button_layout.addWidget(self.stop_button,1,0)

        # Create group box for start and stop buttons
        button_group_box = QGroupBox("Logging Controls")
        button_group_box.setLayout(button_layout)

        # Create main layout and add group boxes
        main_layout = QHBoxLayout()
        main_layout.addWidget(file_location_group_box)
        main_layout.addWidget(button_group_box)
        self.setLayout(main_layout)






    def populate_network_adapters(self):
        adapters = psutil.net_if_addrs()
        for adapter in adapters:
            self.network_adapter_dropdown.addItem(adapter)

    def update_adapter_label(self):
        self.selected_adapter = self.network_adapter_dropdown.currentText()
        self.network_adapter_label.setText(f"Selected Adapter: {self.selected_adapter}")

    def toggle_ip_widgets(self):
        if self.use_net_rec_checkbox.isChecked():
            self.ip_label.show()
            self.ip_text_box.show()
        else:
            self.ip_label.hide()
            self.ip_text_box.hide()


    def update_ip_label(self):
        rec_ip = self.ip_text_box.text()
        self.ip_label.setText(f"NET/REC ip: {rec_ip}")




    def run_cmd_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            print (command)
            return output

        except subprocess.CalledProcessError as e:
            # If the command returns a non-zero exit status
            return print(e.output)

    def start_net_rec(self):

        if self.ip_text_box.text():
            rec_ip = self.ip_text_box.text()
        else:
            rec_ip = "192.168.28.1"
         # Open a command prompt window and run a command
        cmd_1 =(f"C:\\apps\\Net-SNMP\\bin\\snmpset -v2c -c public {rec_ip} .1.3.6.1.4.1.33698.10.21.0 i 1")
        cmd_2 =(f"C:\\apps\\Net-SNMP\\bin\\snmpset -v2c -c public {rec_ip} .1.3.6.1.4.1.33698.10.20.0 i 1")


        if self.use_net_rec_checkbox.isChecked():
            self.run_cmd_command(cmd_1)
            time.sleep(0.5)
            self.run_cmd_command(cmd_2)

    def stop_net_rec(self):
        rec_ip = self.ip_text_box.text()
        cmd_1 =(f"C:\\apps\\Net-SNMP\\bin\\snmpset -v2c -c public {rec_ip} .1.3.6.1.4.1.33698.10.21.0 i 2")
        cmd_2 =(f"C:\\apps\\Net-SNMP\\bin\\snmpset -v2c -c public {rec_ip} .1.3.6.1.4.1.33698.10.20.0 i 0")

        if self.use_net_rec_checkbox.isChecked():
            self.run_cmd_command(cmd_1)
            time.sleep(0.5)
            self.run_cmd_command(cmd_2)



    def start_logging(self):
        # Get the selected directory path
        directory_path = self.file_location_label.text()
        directory_path = directory_path.replace("/","\\")


        selected_adapter = self.network_adapter_dropdown.currentText()

        directory_path = self.file_location_label.text()
        self.directory_path = directory_path


        self.file_path = (f"C:\\Program Files\\Wireshark\\dumpcap.exe -i {self.selected_adapter} -s 1518 -P -w {self.directory_path}\\ -b filesize:16384 -b files:256")
        self.start_net_rec()
        self.process_thread = ProcessThread(self.file_path)
        self.process_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_logging(self):
        # Get the selected directory path
        directory_path = self.file_location_label.text()
        rec_ip = self.ip_text_box.text()
        self.stop_net_rec()



        # Enable start button and disable stop button
        if self.process_thread is not None:
            self.process_thread.terminate()
            self.process_thread.wait()
            self.process_thread = None
            print ("Stop Button pressed!")
            os.system("taskkill /f /im dumpcap.exe")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def select_directory(self):
        # Open a file dialog to select a directory
        self.directory_path = QFileDialog.getExistingDirectory(self, "Select Directory")

        # Update the file location label with the selected directory path
        self.file_location_label.setText(self.directory_path)


class ProcessThread(QThread):
    def __init__(self,file_path,parent=None):
        self.filepath = file_path
        super().__init__(parent)

    def run(self):
        dumpcap = subprocess.call(self.filepath, creationflags = subprocess.CREATE_NEW_CONSOLE)
        dumpcap_process = multiprocessing.Process(target = dumpcap, args=file_path)
        dumpcap_process.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
