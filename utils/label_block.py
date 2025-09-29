import pyqtgraph as pg
from functools import partial
from pyqtgraph import PlotCurveItem
from PyQt5.QtWidgets import QMenu
#Custum library

class block(PlotCurveItem):
    def __init__(self,GUI,data_buffer,main_graph,*args, **kwargs): 
        super(block,self).__init__(*args, **kwargs)
        self.GUI = GUI
        self.data_buffer = data_buffer
        self.main_graph = main_graph
        x,_ = self.getData()
        self.old_x1 = x[1]
        self.old_x2 = x[2]

    def mouseClickEvent(self, event):
        if event.button() == pg.QtCore.Qt.RightButton:
            self.action(event)
            event.accept()  
        else:
            event.ignore() 
    
    def action(self,event):
        self.GUI.label_adjust_group.setEnabled(False)
        self.redo_block()
        action_menu = QMenu()
        action_menu.setGeometry(100, 100, 100, 100)
        delete_action = action_menu.addAction("Delete")
        change_pos_action = action_menu.addAction("Change Position")
        change_label_action = action_menu.addAction("Change Label")
        delete_action.triggered.connect(self.delete)
        change_pos_action.triggered.connect(self.change_pos)
        change_label_action.triggered.connect(partial(self.change_label,event))
        global_position = event.screenPos()
        action_menu.exec_(global_position.toPoint())

    def delete(self):
        index = self.main_graph.label_list.index(self)
        self.main_graph.removeItem(self.main_graph.label_text[index])
        self.main_graph.removeItem(self)
        x,_ = self.getData()
        self.data_buffer.change_current_label(x[1],x[2],0)
        self.main_graph.label_text.remove(self.main_graph.label_text[index])
        self.main_graph.label_list.remove(self)
        self.main_graph.current_label_index == None
        self.GUI.label_adjust_group.setEnabled(False)

    def change_pos(self):
        self.main_graph.current_label_index = self.main_graph.label_list.index(self)
        x,_ = self.getData()
        self.old_x1 = x[1]
        self.old_x2 = x[2]
        self.GUI.x1_adjust.setValue(self.old_x1)
        self.GUI.x2_adjust.setValue(self.old_x2)
        self.GUI.label_adjust_group.setEnabled(True)

    def change_label(self,event):
        self.main_graph.label_option(event)
        index = self.main_graph.label_list.index(self)
        self.main_graph.label_text[index].setText(self.main_graph.label_name(self.main_graph.label))
        x,_ = self.getData()
        self.GUI.data_buffer.change_current_label(x[1],x[2],self.main_graph.label)

    def redo_block(self):
        index = self.main_graph.current_label_index
        if index != None:
            x1 = self.main_graph.label_list[index].old_x1
            x2 = self.main_graph.label_list[index].old_x2
            x,_ = self.main_graph.label_list[index].getData()
            if x1 != x[1] or x2 != x[2]:
                self.main_graph.label_list[index].setData([x1,x1,x2,x2,x1],[0,2,2,0,0])
                self.main_graph.label_text[index].setPos(int((x1+x2)/2), 2.1)
                self.GUI.x1_adjust.setValue(x1)
                self.GUI.x2_adjust.setValue(x2)