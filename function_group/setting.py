import os
class data_link:
    __link_list= ["D:/my_data/yte/Data_base_AiMED_project_v1/Signal","D:/ppg_project/Data/Data_base_AiMED_project_v1/Signal"]
    def __init__(self) -> None:
        self.path = ""
        self.save_path = "G:/My Drive/paper_team/project/ppg/labeled"
        for item in self.__link_list:
            if os.path.exists(item):
                self.path = item
                break