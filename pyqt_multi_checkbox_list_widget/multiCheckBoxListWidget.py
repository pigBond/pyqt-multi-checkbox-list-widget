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
        # 如果传入的item是字典类型（处理JSON数据）
        if isinstance(item, dict):
            # 从字典中获取必要的信息
            model = item.get("model", "")
            algorithm = item.get("algorithm", "")
            environment = item.get("environment", "")
            task = item.get("task", "")
            
            # 格式化列表项的文本
            item_text = f"{model}:  {algorithm} - {environment} - {task}"
            
            item = QListWidgetItem(item_text)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            
            # 将模型、算法、环境和任务信息存储为列表项的自定义数据
            item.setData(Qt.UserRole, {
                "model": model,
                "algorithm": algorithm,
                "environment": environment,
                "task": task
            })
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

    def filterItems(self, algorithm=None, environment=None, task=None):
        for i in range(self.count()):
            item = self.item(i)
            item_data = item.data(Qt.UserRole)
            
            match_algorithm = algorithm is None or item_data.get("algorithm") in algorithm
            match_environment = environment is None or item_data.get("environment") in environment
            match_task = task is None or item_data.get("task") in task
            
            item.setHidden(not (match_algorithm and match_environment and match_task))


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
