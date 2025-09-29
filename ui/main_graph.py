import os
import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QButtonGroup, QRadioButton, QPushButton


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.insert(0, parent_dir)

from utils import block

class main_graph(pg.PlotWidget):
    __roi_list = []
    __ecg_show = None
    __ppg_show = None
    label_list = []
    label_text = []
    label = 14
    indices = []
    current_label_index = None

    def __init__(self,GUI,data_buffer):
        self.GUI = GUI
        super(main_graph,self).__init__(self.GUI.signal_group)
        self.data_buffer = data_buffer
        self.setGeometry(10,15,940,380)
        self.setMenuEnabled(False)
        self.scene().sigMouseMoved.connect(self.mouse_moved)
        self.scene().sigMouseClicked.connect(self.mouse_clicked)

    #Callbacks
    def mouse_moved(self, pos):
        if len(self.__roi_list) != 0:
            if isinstance(self.__roi_list[0], pg.ROI):
                mouse_point = self.plotItem.vb.mapSceneToView(pos)
                self.__roi_list[0].setSize([mouse_point.x() - self.__roi_list[0].pos()[0], mouse_point.y() - self.__roi_list[0].pos()[1]])

                x_1  = self.__roi_list[0].pos()[0]
                x_2 = mouse_point.x()
                x_data = np.array(range(len(self.data_buffer.ECG_take())))
                
                if x_1 < x_2:
                    self.indices = np.where((x_data >= x_1) & (x_data <= x_2))
                elif x_1 > x_2:
                    self.indices = np.where((x_data <= x_1) & (x_data >= x_2))

    def mouse_clicked(self, event):
        if event.double():
            if len(self.__roi_list) == 0:
                mouse_point = self.plotItem.vb.mapSceneToView(event.pos())
                self.ROI_creator([mouse_point.x(),mouse_point.y()]) 
        
        if event.button() == pg.QtCore.Qt.LeftButton and not event.double():
            if len(self.__roi_list) != 0:
                if isinstance(self.__roi_list[0], pg.ROI):
                    self.removeItem(self.__roi_list[0])
                    self.__roi_list.clear() 
                    if len(self.indices[0]) > 1:
                        self. current_label_index = None
                        self.GUI.label_adjust_group.setEnabled(False)
                        self.label_option(event)
                        if self.label != 14:
                            self.data_buffer.change_current_label(self.indices[0][0],self.indices[0][-1],self.label)
                            self.add_label(self.label,self.indices[0][0],self.indices[0][-1])
                            self.label_remake_call()
    
    #Methods
    def main_graph_sketch(self):
        self.clear()
        self.__ecg_show = self.plot(self.data_buffer.ECG_take()+1)
        self.__pgg_show = self.plot(self.data_buffer.PPG_take())
        self.label_remake_call()
    
    def flush_label_graph(self):
        for item1,item2 in zip(self.label_list,self.label_text):
            self.removeItem(item1)
            self.removeItem(item2)
    
    def label_remake_call(self):
        self.flush_label_graph()
        self.label_decode(self.data_buffer.Label_take())
    
    def ROI_creator(self,pos): 
        roi = pg.RectROI(pos, pos, pen='r') 
        self.__roi_list.append(roi)
        self.addItem(self.__roi_list[0])
    
    def label_decode(self,label):
        for i in range(1,14):
            tem = np.array(label == i)
            tem1 = np.append(tem, 0)
            tem2 = np.insert(tem, 0, 0)
            index_list = np.where(np.abs(tem1-tem2) == 1)[0]
            if len(index_list) > 1:
                for idx in range(len(index_list)-1):
                    p1 = index_list[idx]
                    p2 = index_list[idx+1]
                    if tem[int((p1+p2)/2)] == 1:
                        self.data_buffer.change_current_label(p1,p2,i)
                        self.add_label(i,p1,p2)

                        
    def add_label(self,i,p1,p2):
        name = self.label_name(i)
        self.label_list.append(block(self.GUI,self.data_buffer,self,x = [p1,p1,p2,p2,p1], y = [0,2,2,0,0], pen = 'g'))
        self.label_text.append(pg.TextItem(text=name, color='r', anchor=(0.5, 0.5)))
        self.label_text[-1].setPos(int((p1+p2)/2), 2.1)
        self.addItem(self.label_list[-1])
        self.addItem(self.label_text[-1])
    
    def label_option(self,event):
        self.label = 14
        window = QDialog()
        window.setWindowTitle("Label Selection")
        global_position = event.screenPos()
        x = global_position.x()
        y = global_position.y()
        window.setGeometry(int(x), int(y), 100, 100)
        layout = QVBoxLayout()
        button_group = QButtonGroup(window)
        labels = ["AF","PAC","PVC",
                  "PAC-nhip-doi","PAC-cap-doi",
                  "PVC-nhip-doi","PVC-cap-doi",
                  "Block-AV-do-1",
                  "Block-AV-do-2-mobitz-1",
                  "Block-AV-do-2-mobitz-2",
                  "Block-AV-do-3",
                  "Noise",
                  "Other"]
        for label in labels:
            radio_button = QRadioButton(label)
            layout.addWidget(radio_button)
            button_group.addButton(radio_button)
        button = QPushButton("Local syn")
        layout.addWidget(button)
        window.setLayout(layout)
        
        def close_window():
            checked_button = button_group.checkedButton()
            if checked_button is not None:
                tem =  button_group.checkedButton()
                if tem.text() == "AF":
                    self.label = 1
                elif tem.text() == "PAC":
                    self.label = 2
                elif tem.text() == "PVC":
                    self.label = 3
                elif tem.text() == "PAC-nhip-doi":
                    self.label = 4
                elif tem.text() == "PAC-cap-doi":
                    self.label = 5
                elif tem.text() == "PVC-nhip-doi":
                    self.label = 6
                elif tem.text() == "PVC-cap-doi":
                    self.label = 7
                elif tem.text() == "Block-AV-do-1":
                    self.label = 8
                elif tem.text() == "Block-AV-do-2-mobitz-1":
                    self.label = 9
                elif tem.text() == "Block-AV-do-2-mobitz-2":
                    self.label = 10
                elif tem.text() == "Block-AV-do-3":
                    self.label = 11
                elif tem.text() == "Noise":
                    self.label = 12
                elif tem.text() == "Other":
                    self.label = 13
            else:
                self.label = 14
            window.close()

        def back_based_syn_call():
            ecg = self.data_buffer.ECG_take()
            ppg = self.data_buffer.PPG_take()
            label = self.data_buffer.Label_take()
            self.data_buffer.syn_signal(ecg,ppg[self.indices[0][0]:self.indices[0][-1]],label,60,60)
            self.GUI.change_range()
            self.main_graph_sketch()
            window.close()

        button_group.buttonClicked.connect(close_window)
        button.clicked.connect(back_based_syn_call)
        window.exec_()

    def label_name(self,i):
        if i == 1: 
            name = "AF"
        elif i == 2:
            name = "PAC"
        elif i == 3:
            name = "PVC"
        elif i == 4:
            name = "PAC-nhip-doi"
        elif i == 5:
            name = "PAC-cap-doi"
        elif i == 6:
            name = "PVC-nhip-doi"
        elif i == 7:
            name = "PVC-cap-doi"
        elif i == 8:
            name = "Block-AV-do-1"
        elif i == 9:
            name = "Block-AV-do-2-mobitz-1"
        elif i == 10:
            name = "Block-AV-do-2-mobitz-2"
        elif i == 11:
            name = "Block-AV-do-3"
        elif i == 12:
            name = "Noise"
        elif i == 13:
            name = "Other"
        return name