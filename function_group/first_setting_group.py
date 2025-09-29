class first_setting:
    __hr = None
    __spectrum = None
    
    def __init__(self,GUI,data_buffer,main_graph):
        self.GUI = GUI
        self.data_buffer = data_buffer
        self.main_graph = main_graph

        self.GUI.label_on.clicked.connect(self.label_on_call)

    def label_on_call(self):
        if self.GUI.label_on.isChecked() == True:
            for item1, item2 in zip(self.main_graph.label_list,self.main_graph.label_text):
                item1.show()
                item2.show()
        else:
            for item1, item2 in zip(self.main_graph.label_list,self.main_graph.label_text):
                item1.hide()
                item2.hide()