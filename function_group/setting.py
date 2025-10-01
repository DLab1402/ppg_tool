import os
class data_link:
    __link_list= ["G:/My Drive/paper_team/project/ppg/data/Data_base_AiMED_project_v0/Signal",""]
    def __init__(self) -> None:
        self.path = ""
        for item in self.__link_list:
            if os.path.exists(item):
                self.path = item
                break