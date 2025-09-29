import numpy as np

class signal_view:
    def __init__(self,GUI,data_buffer,main_graph):
        self.GUI = GUI
        self.data_buffer = data_buffer
        self.main_graph = main_graph
        self.GUI.local_view.clicked.connect(self.local_call)
        self.GUI.back.clicked.connect(self.signal_back_call)
        self.GUI.next.clicked.connect(self.signal_next_call)

    def local_call(self):
        if isinstance(self.data_buffer.PPG_take(), np.ndarray):
            s = self.GUI.start_point.value()
            e = self.GUI.end_point.value()
            if s < e:
                self.main_graph.setRange(xRange=(s, e),yRange=(0,2))
            else:
                self.GUI.start_point.setValue(0)
                self.GUI.end_point.setValue(len(self.data_buffer.PPG_take()))

    def signal_back_call(self):
        self.GUI.start_point.setValue(self.GUI.start_point.value()-self.GUI.step.value())
        self.GUI.end_point.setValue(self.GUI.end_point.value()-self.GUI.step.value())
        self.local_call()

    def signal_next_call(self):
        self.GUI.start_point.setValue(self.GUI.start_point.value()+self.GUI.step.value())
        self.GUI.end_point.setValue(self.GUI.end_point.value()+self.GUI.step.value())
        self.local_call()