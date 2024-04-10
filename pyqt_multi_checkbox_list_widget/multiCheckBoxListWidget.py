from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QListWidget,QListWidgetItem

class MultiCheckBoxListWidget(QListWidget):
    checkedSignal = pyqtSignal(int, Qt.CheckState)

    def __init__(self):
        super().__init__()
        self.itemChanged.connect(self.__sendCheckedSignal)

    def __sendCheckedSignal(self, item):
        r_idx = self.row(item)
        state = item.checkState()
        self.checkedSignal.emit(r_idx, state)

    def addItems(self, items) -> None:
        for item in items:
            self.addItem(item)

    def addItem(self, item) -> None:
        # 如果传入的item是字符串类型
        if isinstance(item, str):
            # 创建一个QListWidgetItem对象，并将传入的字符串作为列表项的文本
            item = QListWidgetItem(item)
            # 设置列表项的属性，允许用户更改其选中状态
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            # 默认设置列表项的选中状态为未选中
            item.setCheckState(Qt.Unchecked)
        # 如果传入的item是字典类型（假设是处理JSON数据）
        elif isinstance(item, dict):
            # 从字典中获取"name"、"gender"和"education"键对应的值
            name = item.get("name", "")
            gender = item.get("gender", "")
            education = item.get("education", "")  # 处理新的学历字段
            # 格式化列表项的文本，显示为"姓名 (性别) - 学历"
            item_text = f"{name} ({gender}) - {education}"
            item = QListWidgetItem(item_text)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            # 将性别和学历信息存储为列表项的自定义数据
            item.setData(Qt.UserRole, {"name": name, "gender": gender, "education": education})
        super().addItem(item)

    # 定义切换列表项选中状态的方法，接收一个state参数
    def toggleState(self, state):
        # 遍历列表中的所有项
        for i in range(self.count()):
            item = self.item(i)
            # 如果列表项的当前选中状态不等于传入的state参数
            if item.checkState() != state:
                # 则改变该列表项的选中状态为传入的state
                item.setCheckState(state)

    # 允许根据性别和学历进行筛选
    def filterItems(self, gender=None, education=None):
        for i in range(self.count()):
            item = self.item(i)
            item_data = item.data(Qt.UserRole)  # 获取存储的性别和学历信息
            # 判断是否符合性别筛选条件
            match_gender = gender is None or item_data.get("gender") == gender
            # 判断是否符合学历筛选条件
            match_education = education is None or item_data.get("education") == education
            # 如果同时满足性别和学历的筛选条件，则显示列表项，否则隐藏
            item.setHidden(not (match_gender and match_education))

    def getAllItems(self):
        print("----------------------------------------")
        for i in range(self.count()):
            item = self.item(i)
            print(item.data(Qt.UserRole))
        print("----------------------------------------")

    # def getCheckedItemsData(self):
    #     checked_items_data = []
    #     for i in range(self.count()):
    #         item = self.item(i)
    #         if item.checkState() == Qt.Checked:
    #             # 获取项的文本或关联的自定义数据
    #             item_data = item.data(Qt.UserRole)  # 如果你存储了自定义数据
    #             checked_items_data.append(item_data or item.text())
    #     return checked_items_data

    def uncheckAllRows(self):
        for i in range(self.count()):
            item=self.item(i)
            item.setCheckState(Qt.Unchecked)

    def getCheckedRows(self):
        return self.__getFlagRows(Qt.Checked)

    def getUncheckedRows(self):
        return self.__getFlagRows(Qt.Unchecked)

    def __getFlagRows(self, flag: Qt.CheckState):
        flag_lst = []
        for i in range(self.count()):
            item = self.item(i)
            if item.checkState() == flag:
                flag_lst.append(i)

        return flag_lst

    def removeCheckedRows(self):
        self.__removeFlagRows(Qt.Checked)

    def removeUncheckedRows(self):
        self.__removeFlagRows(Qt.Unchecked)

    def __removeFlagRows(self, flag):
        flag_lst = self.__getFlagRows(flag)
        flag_lst = reversed(flag_lst)
        for i in flag_lst:
            self.takeItem(i)
