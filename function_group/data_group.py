import os
import json
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QTreeWidgetItem
from .setting import data_link
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

class data:
    path = data_link()
    link = path.path
    data_store_link = parent_dir+"/data"

    def __init__(self,GUI = None,data_buffer = None,main_graph = None):
        self.GUI = GUI
        self.main_graph = main_graph
        self.data_buffer = data_buffer
        self.current_label = 0

        self.GUI.loaddata.clicked.connect(self.data_load)
        self.GUI.data_list.itemClicked.connect(self.data_select)
        self.GUI.syn_flag.valueChanged.connect(self.syn_change_call)
        self.GUI.syn_ref.currentIndexChanged.connect(self.syn_change_call)
        self.GUI.data_show.currentIndexChanged.connect(self.data_select)

    def data_load(self):
        self.GUI.enable_function_group(False)
        self.GUI.data_list.clear()
        count_file = 0
        count_adjusted_file = 0
        count_valid_file = 0
        link = self.link
        
        if len(os.listdir(self.data_store_link)) != 0:
            link = self.data_store_link
            file_list = os.listdir(link)
            for sub_file in file_list:
                with open(link+'/'+sub_file, 'r') as file:
                    subitem = QTreeWidgetItem(self.GUI.data_list,[sub_file])
                    data= json.load(file)
                    count_file = count_file + 1
                    if "Valid" in data:
                        if data["Valid"] == True:
                            color = "green"
                        else:
                            color = "red"
                        subitem.setBackground(0, QBrush(QColor(color)))
                        count_adjusted_file = count_adjusted_file + 1
        else:
            folder = os.listdir(self.link)
            for item in folder:
                try:
                    file_list = os.listdir(link+'/'+item+'/ECG_Label')
                    for sub_file in file_list:
                        with open(link+'/'+item+'/ECG_Label/'+sub_file, 'r') as file:
                            subitem = QTreeWidgetItem(self.GUI.data_list,[sub_file])
                            data= json.load(file)
                            count_file = count_file+1
                            with open(self.data_store_link+'/'+sub_file, "w") as json_file:
                                json.dump(data, json_file)
                            if "Valid" in data:
                                if data["Valid"] == True:
                                    color = "green"
                                else:
                                    color = "red"
                                subitem.setBackground(0, QBrush(QColor(color)))
                                count_adjusted_file = count_adjusted_file + 1

                except Exception as e:
                    # self.GUI.message_box(e)
                    print(e)
                    pass

        first_item = self.GUI.data_list.topLevelItem(0)
        if first_item:
            self.GUI.data_list.setCurrentItem(first_item)
            self.data_select()
            self.GUI.enable_function_group(True)
            self.GUI.total_file_inc(count_file)
            self.GUI.total_adjusted_file_inc(count_adjusted_file)
        else:
            self.GUI.message_box("There is no any data file.")

    def data_select(self):
        self.GUI.label_adjust_group.setEnabled(False)
        labeled_file = self.GUI.data_list.currentItem().text(0)
        with open(self.data_store_link+'/'+labeled_file, 'r') as file:
            data= json.load(file)
            self.data_buffer.set_data(data,self.GUI.data_show.currentText())
            self.GUI.change_range()
            self.main_graph.main_graph_sketch()
    
    def syn_change_call(self):
        self.data_buffer.syn_option(self.GUI.data_show.currentText())
        self.GUI.change_range()
        self.main_graph.main_graph_sketch()  