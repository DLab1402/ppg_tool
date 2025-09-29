import numpy as np
import neurokit2 as nk
import scipy.signal as signal

class syn:
    ppg_fre = 60
    ecg_fre = 1000

    def __init__(self,ecg,ppg,label,flag_custum=0,syn_ref = "Peak"):
        self.ecg = ecg
        self.ppg = ppg
        self.label = label
        self.flag_custum = flag_custum
        self.syn_ref = syn_ref
    
    def process(self):
        intersect,time = self.cross_correlation()
        if intersect != None:
            return self.ecg[intersect[0]-time:intersect[1]-time], self.ppg[intersect[0]:intersect[1]], self.label[intersect[0]-time:intersect[1]-time]
        else:
            return self.ecg, self.ppg, self.label
        
    def cross_correlation(self):
        intersect = None
        if self.ppg_fre != self.ecg_fre:
            self.ecg = signal.resample(self.ecg,int(np.floor(self.ppg_fre/np.array(self.ecg_fre)*len(self.ecg))))
            self.label = self.label_resample(np.zeros(len(self.ecg)))

        if self.syn_ref == "Foot":
            tem = np.abs(-1*self.ppg)
            print(1)
            tem = (tem-np.min(tem))/(np.max(tem)-np.min(tem))
        else:
            tem = self.ppg

        ppg_peaks = self.ppg_peak(tem)
        ecg_peaks = self.ecg_peak(self.ecg)
        
        cross_corr_1 = np.correlate(ppg_peaks, ecg_peaks, mode='full')
        flag = np.argmax(cross_corr_1)+self.flag_custum
        intersect, time = self.over_lap_find(flag,len(self.ppg),len(self.ecg))    

        return intersect, time
    
    def ppg_peak(self,ppg):
        _, results = nk.ppg_peaks(ppg, sampling_rate = self.ppg_fre)
        ppg_peaks = np.zeros(len(ppg))
        ppg_peaks[results["PPG_Peaks"]] = 1
        return ppg_peaks

    def ecg_peak(self,ecg):
        _, results = nk.ecg_peaks(ecg, sampling_rate = self.ppg_fre)
        ecg_peaks = np.zeros(len(ecg))
        ecg_peaks[results["ECG_R_Peaks"]] = 1
        return ecg_peaks
    
    def over_lap_find(self, flag,L1,L2):
        time = flag - L2 + 1 
        if flag >= L1-1:
            if time <= 0:
                intersect = [0,L1-1]
            elif time < L1-1:
                intersect = [time,L1-1]
            else:
                intersect = None
        elif (flag > 0) and (flag < L1-1):
            if time <= 0:
                intersect = [0,flag]
            else:
                intersect = [time,flag]
        else:
            intersect = None
        return intersect, time
    
    def label_resample(self,zeros_array):
        new_label = zeros_array
        for i in range(1,14):
            tem = np.array(self.label == i)
            tem1 = np.append(tem, 0)
            tem2 = np.insert(tem, 0, 0)
            index_list = np.where(np.abs(tem1-tem2) == 1)[0]
            if len(index_list) > 1:
                for idx in range(len(index_list)-1):
                    p1 = index_list[idx]
                    p2 = index_list[idx+1]-1
                    if tem[int((p1+p2)/2)] == 1:
                        scale_p1 = int(p1*self.ppg_fre/self.ecg_fre)+1
                        scale_p2 = int(p2*self.ppg_fre/self.ecg_fre)-1
                        new_label[scale_p1:scale_p2] = i
        return new_label