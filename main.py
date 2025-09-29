import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from ui import gui_gen, main_graph, properties   
from function_group import data, signal_view, control, first_setting, label_adjust

class main():
    def __init__(self):
        self.properties = properties()
        self.gui = gui_gen(self.properties)
        self.properties.set_para(self.gui)
        self.main_graph = main_graph(self.gui,self.properties)
        
        #function group
        self.data_group = data(self.gui,self.properties,self.main_graph)
        self.signal_view = signal_view(self.gui,self.properties,self.main_graph)
        self.control = control(self.gui,self.properties,self.main_graph)
        self.first_setting = first_setting(self.gui,self.properties,self.main_graph)
        self.label_adjust = label_adjust(self.gui,self.properties,self.main_graph)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    actor = main()
    widget = QtWidgets.QStackedWidget()
    widget.setFixedWidth(1155)
    widget.setFixedHeight(645)
    widget.addWidget(actor.gui)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting") 