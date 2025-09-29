import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi

class gui_gen(QtWidgets.QWidget):
    main_graph = None
    def __init__(self,data_buffer):
        super(gui_gen,self).__init__() 
        self.data_buffer = data_buffer
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "label_process.ui")
        loadUi(ui_path,self)
        self.label_adjust_group.setEnabled(False)
        self.data_list.setHeaderHidden(True)
        self.enable_function_group(False)
        self.total_files = 0
        self.total_adjusted_files = 0
        self.total_valid_files = 0

    def change_range(self):
        L = len(self.data_buffer.PPG_take())
        self.start_point.setMaximum(L)
        self.end_point.setMaximum(L)
        self.end_point.setValue(L)
        self.x1_adjust.setMaximum(L)
        self.x2_adjust.setMaximum(L)
        self.step.setValue(int(L/10))
    
    def enable_function_group(self,isEna: bool):
        self.signal_group.setEnabled(isEna)
        self.data_list.setEnabled(isEna)
        self.control_group.setEnabled(isEna)
        self.first_setting_group.setEnabled(isEna)
        self.signal_view_group.setEnabled(isEna)

    def message_box(self,mess):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Error")
        error_box.setText(mess)
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()

    def total_file_inc(self,value):
        self.total_files = value
        self.total_file.setText(str(value))

    def total_adjusted_file_inc(self,value):
        self.total_adjusted_files = value
        self.total_adjusted_file.setText(str(value))

    def total_valid_file_inc(self,value):
        self.total_valid_files = value
        self.total_valid_file.setText(str(value))