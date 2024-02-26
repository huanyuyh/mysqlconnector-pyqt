import sys
import pymysql
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QApplication, \
    QTableWidget, QTableWidgetItem, QFormLayout
from PyQt6.QtGui import QDoubleValidator

class InsertDataDialog(QDialog):
    conn = pymysql.connect
    def __init__(self,conn):
        super().__init__()
        self.conn = conn  # 存储数据库连接
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # 课程成绩输入
        self.gradeInput = QLineEdit(self)
        layout.addWidget(QLabel("课程成绩:"))
        layout.addWidget(self.gradeInput)
        # 创建一个 QDoubleValidator 对象
        validator = QDoubleValidator()
        validator.setBottom(0.0)  # 设置最小值，例如0.0
        # 设置验证器到 QLineEdit
        self.gradeInput.setValidator(validator)

        # 课程名称输入
        self.nameInput = QLineEdit(self)
        layout.addWidget(QLabel("课程名称:"))
        layout.addWidget(self.nameInput)

        # class_id 下拉菜单
        self.classIdCombo = QComboBox(self)
        self.classIdCombo.currentIndexChanged.connect(self.handleselectedid)
        layout.addWidget(QLabel("class_id:"))
        layout.addWidget(self.classIdCombo)

        # student_id 下拉菜单
        self.studentIdCombo = QComboBox(self)
        layout.addWidget(QLabel("student_id:"))
        layout.addWidget(self.studentIdCombo)

        # 按钮
        buttonsLayout = QHBoxLayout()
        self.insertButton = QPushButton("插入", self)
        self.insertButton.clicked.connect(self.insertData)
        self.cancelButton = QPushButton("取消", self)
        self.cancelButton.clicked.connect(self.reject)  # QDialog的reject方法会关闭对话框
        buttonsLayout.addWidget(self.insertButton)
        buttonsLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonsLayout)

        # 设置对话框的布局
        self.setLayout(layout)
        self.setWindowTitle('插入数据')
    def handleselectedid(self):
        self.nameInput.setText(self.classIdCombo.currentText())
    def insertData(self):
        # 获取输入的数据
        grade = self.gradeInput.text()
        name = self.nameInput.text()
        class_id = self.classIdCombo.currentData()
        student_id = self.studentIdCombo.currentData()
        # 插入数据到数据库的逻辑
        self.insertIntoGrade(grade,name,class_id,student_id)
        print("插入数据:", grade, name, class_id, student_id)
        self.accept()  # 关闭对话框

    def insertIntoGrade(self, class_grade, class_name, class_id, student_id):
        try:
            with self.conn.cursor() as cursor:
                # 构造 SQL 插入语句
                query = "INSERT INTO t_grade (class_grade, class_name, class_id, student_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (class_grade, class_name, class_id, student_id))
                self.conn.commit()  # 提交事务
                print("数据插入成功")
        except Exception as e:
            print("插入数据失败:", e)
            self.conn.rollback()  # 发生错误时回滚事务

class StudentDepartmentDialog(QDialog):
    def __init__(self, data,conn):
        super().__init__()
        self.conn = conn
        self.initUI(data)

    def initUI(self, data):
        layout = QVBoxLayout(self)

        # 创建表格
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)  # 学生ID, 学生姓名, 系ID, 系名称
        self.tableWidget.setHorizontalHeaderLabels(["学生ID", "学生姓名", "系ID", "系名称"])
        # 填充数据
        self.tableWidget.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for column_index, item in enumerate(row_data):
                self.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(item)))

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)
        self.setWindowTitle('人数统计')
        self.resize(600, 600)

    # def onSelectionChanged(self):

class GradesDialog(QDialog):
    def __init__(self, data):
        super().__init__()
        self.initUI(data)

    def initUI(self, data):
        layout = QVBoxLayout(self)

        # 创建表格
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)  # 学生ID, 学生姓名, 课程ID, 课程名称, 成绩
        self.tableWidget.setHorizontalHeaderLabels(["学生ID", "学生姓名", "课程ID", "课程名称", "成绩"])

        # 填充数据
        self.tableWidget.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for column_index, item in enumerate(row_data):
                self.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(item)))

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)
        self.setWindowTitle('成绩统计')
        self.resize(600, 600)

class AverageGradesDialog(QDialog):
    def __init__(self, data):
        super().__init__()
        self.initUI(data)

    def initUI(self, data):
        layout = QVBoxLayout(self)

        # 创建表格
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)  # 课程ID, 课程名称, 平均成绩
        self.tableWidget.setHorizontalHeaderLabels(["课程ID", "课程名称", "平均成绩"])

        # 填充数据
        self.tableWidget.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for column_index, item in enumerate(row_data):
                self.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(item)))

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)
        self.setWindowTitle('平均成绩')
        self.resize(600, 600)

class NewStudentDialog(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.conn = db_connection
        self.initUI()

    def initUI(self):
        # 窗口设置
        self.setWindowTitle("插入学生信息")
        layout = QVBoxLayout(self)

        # 输入框
        self.nameEdit = QLineEdit(self)
        self.idEdit = QLineEdit(self)
        self.deptIdEdit = QLineEdit(self)

        layout.addWidget(QLabel("学生姓名"))
        layout.addWidget(self.nameEdit)
        layout.addWidget(QLabel("学生ID"))
        layout.addWidget(self.idEdit)
        layout.addWidget(QLabel("系ID"))
        layout.addWidget(self.deptIdEdit)

        # 按钮
        buttonsLayout = QHBoxLayout()
        self.okButton = QPushButton("确认")
        self.okButton.clicked.connect(self.on_accept)
        self.cancelButton = QPushButton("取消")
        self.cancelButton.clicked.connect(self.reject)

        buttonsLayout.addWidget(self.okButton)
        buttonsLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonsLayout)

    def on_accept(self):
        student_id = self.idEdit.text()
        student_name = self.nameEdit.text()
        department_id = self.deptIdEdit.text()
        try:
            with self.conn.cursor() as cursor:
                # 插入 t_student_info
                cursor.execute("INSERT INTO t_student_info (student_id, student_name) VALUES (%s, %s)",
                               (student_id, student_name))
                # 插入 t_studentrelation
                cursor.execute("INSERT INTO t_studentrelation (department_id, student_id) VALUES (%s, %s)",
                               (department_id, student_id))
                self.conn.commit()
                cursor.close()
                self.accept()
        except Exception as e:
            print("失败:", e)
class DeleteStudentDialog(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.initUI()

    def initUI(self):
        self.setWindowTitle("删除学生信息")
        layout = QVBoxLayout(self)

        # 输入框
        self.studentIdEdit = QLineEdit(self)
        layout.addWidget(QLabel("请输入要删除的学生ID"))
        layout.addWidget(self.studentIdEdit)

        # 按钮
        buttonsLayout = QHBoxLayout()
        self.deleteButton = QPushButton("删除")
        self.deleteButton.clicked.connect(self.on_delete)
        self.cancelButton = QPushButton("取消")
        self.cancelButton.clicked.connect(self.reject)

        buttonsLayout.addWidget(self.deleteButton)
        buttonsLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonsLayout)

    def on_delete(self):
        student_id = self.studentIdEdit.text()
        try:
            with self.db_connection.cursor() as cursor:
                # 首先从 t_studentrelation 表中删除
                cursor.execute("DELETE FROM t_studentrelation WHERE student_id = %s", (student_id,))

                # 然后从 t_student_info 表中删除
                cursor.execute("DELETE FROM t_student_info WHERE student_id = %s", (student_id,))

                self.db_connection.commit()
                cursor.close()
                self.accept()
        except Exception as e:
            print("失败:", e)
        finally:
            self.accept()


class UpdateStudentDialog(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.initUI()

    def initUI(self):
        self.setWindowTitle("更新学生信息")
        layout = QVBoxLayout(self)

        # 输入框
        self.studentIdEdit = QLineEdit(self)
        self.newNameEdit = QLineEdit(self)
        self.newDeptIdEdit = QLineEdit(self)

        layout.addWidget(QLabel("学生ID"))
        layout.addWidget(self.studentIdEdit)
        layout.addWidget(QLabel("新的学生姓名"))
        layout.addWidget(self.newNameEdit)
        layout.addWidget(QLabel("新的系ID"))
        layout.addWidget(self.newDeptIdEdit)

        # 按钮
        buttonsLayout = QHBoxLayout()
        self.updateButton = QPushButton("更新")
        self.updateButton.clicked.connect(self.on_update)
        self.cancelButton = QPushButton("取消")
        self.cancelButton.clicked.connect(self.reject)

        buttonsLayout.addWidget(self.updateButton)
        buttonsLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonsLayout)

    def on_update(self):
        student_id = self.studentIdEdit.text()
        new_name = self.newNameEdit.text()
        new_dept_id = self.newDeptIdEdit.text()
        try:
            with self.db_connection.cursor() as cursor:
                # 更新 t_student_info 表
                cursor.execute("UPDATE t_student_info SET student_name = %s WHERE student_id = %s",
                               (new_name, student_id))

                # 更新 t_studentrelation 表（如果需要）
                if new_dept_id:
                    cursor.execute("UPDATE t_studentrelation SET department_id = %s WHERE student_id = %s",
                                   (new_dept_id, student_id))

                self.db_connection.commit()
                cursor.close()
                self.accept()
        except Exception as e:
            print("失败:", e)
        finally:
            self.accept()
class AddDepartmentDialog(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.initUI()

    def initUI(self):
        self.setWindowTitle("增加系信息")
        layout = QVBoxLayout(self)

        self.deptIdEdit = QLineEdit(self)
        self.deptNameEdit = QLineEdit(self)

        layout.addWidget(QLabel("系ID"))
        layout.addWidget(self.deptIdEdit)
        layout.addWidget(QLabel("系名称"))
        layout.addWidget(self.deptNameEdit)

        self.addButton = QPushButton("添加")
        self.addButton.clicked.connect(self.on_add)
        self.cancelButton = QPushButton("取消")
        self.cancelButton.clicked.connect(self.reject)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.addButton)
        buttonsLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonsLayout)

    def on_add(self):
        dept_id = self.deptIdEdit.text()
        dept_name = self.deptNameEdit.text()
        cursor = self.db_connection.cursor()
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("INSERT INTO t_department (department_id, department_name) VALUES (%s, %s)",
                               (dept_id, dept_name))
                self.db_connection.commit()
                cursor.close()
                self.accept()
        except Exception as e:
            print("失败:", e)
        finally:
            self.accept()

# 使用示例
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = InsertDataDialog()
    if dialog.exec_():
        print("数据已插入")
    else:
        print("插入已取消")
