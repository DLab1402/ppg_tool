#library import
import os
import sys
import json
import numpy as np
import pandas as pd
import pyqtgraph as pg
import neurokit2 as nk
import openpyxl

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import xml.etree.ElementTree as ET
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QApplication,QTreeWidgetItem,QDialog, QVBoxLayout, QButtonGroup, QRadioButton, QFileDialog
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

class control:
    __folder_path = None

    def __init__(self,GUI,data_buffer,main_graph):
        self.GUI = GUI
        self.data_buffer = data_buffer
        self.main_graph = main_graph
        self.GUI.browse.clicked.connect(self.browse_call)
        self.GUI.save.clicked.connect(self.save_call)
        self.GUI.restore.clicked.connect(self.restore_call)
        self.GUI.packaging.clicked.connect(self.packaging_call)
        self.GUI.flush.clicked.connect(self.flush_call)
    
    def browse_call(self):
        self.__folder_path = QFileDialog.getExistingDirectory(self.GUI, "Select Folder")
        if self.__folder_path != None:
            self.GUI.save_link.setText(self.__folder_path)
        pass

    def save_call(self):
        if self.__folder_path != None:
            name = self.__folder_path +"//"+self.GUI.data_list.currentItem().text(0)
        else:
            name = parent_dir+"/data/"+self.GUI.data_list.currentItem().text(0)
        self.data_buffer.save_data(name,self.GUI.valid.isChecked())
        if self.GUI.valid.isChecked() == True:
            color = "green"
        else:
            color = "red" 
        self.GUI.total_adjusted_files = self.GUI.total_adjusted_files+1
        self.GUI.total_adjusted_file_inc(self.GUI.total_adjusted_files)
        self.GUI.data_list.currentItem().setBackground(0, QBrush(QColor(color)))

    def restore_call(self):
        self.data_buffer.restore()
        self.main_graph.label_remake_call()
        
    def packaging_call(self):
        pass

    def flush_call(self):
        label = np.zeros(len(self.data_buffer.Label_take()))
        self.data_buffer.set_new_label(label)
        self.main_graph.flush_label_graph()