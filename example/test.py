import os
import sys
sys.path.append(os.getcwd())

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QVBoxLayout, QWidget, QApplication
from pyqt_multi_checkbox_list_widget import MultiCheckBoxListWidget

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.filterConditions = {"gender": None, "education": None}  # 定义筛选条件的字典
        self.multiCheckBoxListWidget=None
        self.__initUi()
    

    def updateFilterConditions(self, gender=None, education=None):
        print("切换--",gender,"--",education)
        if gender is not None:
            self.filterConditions["gender"] = gender
        else:
            self.filterConditions["gender"] = None
        if education is not None:
            self.filterConditions["education"] = education
        else:
            self.filterConditions["education"] = None
        
        print("筛选字典 = ",self.filterConditions)
        # 应用当前的筛选条件
        self.multiCheckBoxListWidget.filterItems(gender=self.filterConditions["gender"],
                                             education=self.filterConditions["education"])
        
    def __initUi(self):
        # 全选复选框
        allCheckBox = QCheckBox('Check all')
        # 性别筛选复选框
        maleCheckBox = QCheckBox('Male')
        femaleCheckBox = QCheckBox('Female')
        # 学历筛选复选框
        collegeCheckBox = QCheckBox('College')
        highSchoolCheckBox = QCheckBox('High School')
        elementaryCheckBox = QCheckBox('Elementary')
        
        self.multiCheckBoxListWidget = MultiCheckBoxListWidget()
        # 假设这些是从某个JSON源获取的数据，并已添加了学历信息
        jsonData = [
            {"name": "小红", "gender": "女", "education": "大学"},
            {"name": "小明", "gender": "男", "education": "中学"},
            {"name": "小刚", "gender": "男", "education": "小学"},
            {"name": "小芳", "gender": "女", "education": "大学"},
            {"name": "小A", "gender": "女", "education": "中学"},
            {"name": "小B", "gender": "女", "education": "小学"},
            {"name": "小C", "gender": "男", "education": "大学"}
        ]
        self.multiCheckBoxListWidget.addItems(jsonData)
        
        # 连接全选复选框的状态变化信号到相应的槽函数
        allCheckBox.stateChanged.connect(lambda state: self.multiCheckBoxListWidget.toggleState(state))

        self.multiCheckBoxListWidget.getAllItems()
        
        # 为每个复选框连接一个新的处理函数，以更新筛选条件
        maleCheckBox.stateChanged.connect(lambda: self.updateFilterConditions(gender="男",education=self.filterConditions["education"]))
        femaleCheckBox.stateChanged.connect(lambda: self.updateFilterConditions(gender="女",education=self.filterConditions["education"]))
        collegeCheckBox.stateChanged.connect(lambda: self.updateFilterConditions(gender=self.filterConditions["gender"],education="大学"))
        highSchoolCheckBox.stateChanged.connect(lambda: self.updateFilterConditions(gender=self.filterConditions["gender"],education="中学"))
        elementaryCheckBox.stateChanged.connect(lambda: self.updateFilterConditions(gender=self.filterConditions["gender"],education="小学"))
        
        # 取消勾选时的逻辑处理
        maleCheckBox.stateChanged.connect(lambda state: self.updateFilterConditions(gender=None,education=self.filterConditions["education"]) if state == 0 else None)
        femaleCheckBox.stateChanged.connect(lambda state: self.updateFilterConditions(gender=None,education=self.filterConditions["education"]) if state == 0 else None)
        collegeCheckBox.stateChanged.connect(lambda state: self.updateFilterConditions(gender=self.filterConditions["gender"],education=None) if state == 0 else None)
        highSchoolCheckBox.stateChanged.connect(lambda state: self.updateFilterConditions(gender=self.filterConditions["gender"],education=None) if state == 0 else None)
        elementaryCheckBox.stateChanged.connect(lambda state: self.updateFilterConditions(gender=self.filterConditions["gender"],education=None) if state == 0 else None)

        
        # 布局设置
        lay = QVBoxLayout()
        lay.addWidget(allCheckBox)
        lay.addWidget(maleCheckBox)
        lay.addWidget(femaleCheckBox)
        lay.addWidget(collegeCheckBox)
        lay.addWidget(highSchoolCheckBox)
        lay.addWidget(elementaryCheckBox)
        lay.addWidget(self.multiCheckBoxListWidget)
        self.setLayout(lay)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    app.exec_()
