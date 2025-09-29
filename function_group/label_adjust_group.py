
class label_adjust:
    def __init__(self,GUI,data_buffer,main_graph):
        self.GUI = GUI
        self.data_buffer = data_buffer
        self.main_graph = main_graph
        self.GUI.x1_adjust.valueChanged.connect(self.x_adjust_changed)
        self.GUI.x2_adjust.valueChanged.connect(self.x_adjust_changed)
        self.GUI.cancel_adjusting.clicked.connect(self.cancel_adjusting_call)
        self.GUI.end_adjusting.clicked.connect(self.end_adjusting_call)

    def x_adjust_changed(self):
        index = self.main_graph.current_label_index
        if index == None:
            self.label_adjust_group.setEnabled(False)
        else:
            x1 = self.GUI.x1_adjust.value()
            x2 = self.GUI.x2_adjust.value()
            self.main_graph.label_list[index].setData([x1,x1,x2,x2,x1],[0,2,2,0,0])
            self.main_graph.label_text[index].setPos(int((x1+x2)/2), 2.1)

    def cancel_adjusting_call(self):
        index = self.main_graph.current_label_index
        if index == None:
            self.label_adjust_group.setEnabled(False)
        else:
            self.main_graph.label_list[index].redo_block()
        self.GUI.label_adjust_group.setEnabled(False)

    def end_adjusting_call(self):
        index = self.main_graph.current_label_index
        if index == None:
            self.label_adjust_group.setEnabled(False)
        else:
            old_x1 = self.main_graph.label_list[index].old_x1
            old_x2 = self.main_graph.label_list[index].old_x2
            if  old_x1 > old_x2:
                tem = old_x1
                old_x1 = old_x2
                old_x2 = tem
            label = self.data_buffer.take_current_label(int((old_x1+old_x2)/2))
            self.main_graph.data_buffer.change_current_label(old_x1,old_x2,0)
            new_x,_ = self.main_graph.label_list[index].getData()
            if  new_x[1] > new_x[2]:
                tem = new_x[1]
                new_x[1] = new_x[2]
                new_x[2] = tem
            self.data_buffer.change_current_label(new_x[1],new_x[2],label)
            self.main_graph.label_remake_call()
            self.GUI.label_adjust_group.setEnabled(False)