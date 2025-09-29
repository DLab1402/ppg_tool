import os
import sys
import json
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.insert(0, parent_dir)

from ui import gui_gen
from utils import syn

class properties:
    ppg_fre = 60
    ecg_fre = 1000
    __para = None

    def __init__(self):
        self.__ppg = []
        self.__ecg = []
        self.__or_ppg = []
        self.__or_ecg = []
        self.__or_label = []
        self.__label = []
        self.__new_label = []
        self.valid = False
    
    def set_para(self,GUI):
        self.__para = GUI

    def set_data(self,data, option = "Show saved"):
        self.__or_ppg = np.array(data['PPG'])
        self.__or_ecg = np.array(data['ECG'])
        self.__or_label = np.array(data['Label'])
        self.valid = "Valid" in data
        if self.valid == True:
            self.__ppg = np.array(data['Syn_PPG'])
            self.__ecg = np.array(data['Syn_ECG'])
            self.__label = np.array(data['Syn_Label'])
        
        self.syn_option(option)

    def syn_option(self,option):
        if option == "Show saved" and self.valid == True:
            self.syn_signal(self.__ecg,self.__ppg,self.__label,60,60)
        elif option == "Show origin" or self.valid == False:
            self.syn_signal(self.__or_ecg,self.__or_ppg,self.__or_label,self.ecg_fre,self.ppg_fre)

    def syn_signal(self,ecg,ppg,label,f1,f2):
        if isinstance(self.__para,gui_gen):
            flag = self.__para.syn_flag.value()
            ref = self.__para.syn_ref.currentText()
        cal = syn(ecg,ppg,label,flag_custum=flag,syn_ref=ref)
        cal.ppg_fre = f2
        cal.ecg_fre = f1
        self.__ecg, self.__ppg, self.__label = cal.process()
        self.__ecg = (self.__ecg-np.min(self.__ecg))/(np.max(self.__ecg)-np.min(self.__ecg))
        self.__ppg = (self.__ppg-np.min(self.__ppg))/(np.max(self.__ppg)-np.min(self.__ppg))
        self.__new_label = self.__label.copy()

    def take_data(self):
        return {'PPG':self.__ppg, 'ECG':self.__ecg, 'Label':self.__new_label}
    
    def ECG_take(self):
        return self.__ecg
    
    def PPG_take(self):
        return self.__ppg
    
    def Label_take(self):
        return self.__new_label
    
    def set_new_label(self,new_label):
        self.__new_label = new_label

    def change_current_label(self,p1,p2,value):
        self.__new_label[p1:p2] = value

    def restore(self):
        self.__new_label = self.__label.copy()

    def take_current_label(self,x):
        return self.__new_label[x]
    
    def save_data(self,file_path,valid):
        save_data = {'PPG':self.__or_ppg.tolist(),
                     'ECG':self.__or_ecg.tolist(),
                     'Label': self.__or_label.tolist(),
                     'Valid': valid,
                     'Syn_Label':self.__new_label.tolist(),
                     'Syn_PPG':self.__ppg.tolist(),
                     'Syn_ECG':self.__ecg.tolist()}
        with open(file_path, "w") as json_file:
            json.dump(save_data, json_file)