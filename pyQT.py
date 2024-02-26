import sys
import pymysql
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTableWidget, QTableWidgetItem, QMenuBar, QMessageBox, QCheckBox
import MyQDailog
from qt_material import apply_stylesheet
class DatabaseManager(QWidget):
    dataBaseUrl = ""
    dataBasePort = ""
    dataBaseName = ""
    username = ""
    password = ""
    conn = pymysql.connect
    isConnected = False
    selectedRows = None
    selectedColumns = None
    results = list
    newValues = []
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadCredentials()

    def initUI(self):
        # 垂直布局
        vLayout = QVBoxLayout()
        self.dataBaseUrlLabel = QLabel('数据库地址:')
        self.dataBaseUrlInput = QLineEdit()
        self.dataBaseUrlInput.textChanged.connect(self.ondataBaseUrlChanged)
        self.dataBasePortLabel = QLabel('数据库端口:')
        self.dataBasePortInput = QLineEdit()
        self.dataBasePortInput.textChanged.connect(self.ondataBasePortChanged)
        self.dataBaseNameLabel = QLabel('数据库名称:')
        self.dataBaseNameInput = QLineEdit()
        self.dataBaseNameInput.textChanged.connect(self.ondataBaseNameChanged)
        dateBaseBox = QHBoxLayout()
        dateBaseBox.addWidget(self.dataBaseUrlLabel)
        dateBaseBox.addWidget(self.dataBaseUrlInput)
        dateBaseBox.addWidget(self.dataBasePortLabel)
        dateBaseBox.addWidget(self.dataBasePortInput)
        dateBaseBox.addWidget(self.dataBaseNameLabel)
        dateBaseBox.addWidget(self.dataBaseNameInput)
        # 用户名和密码输入
        userBox = QHBoxLayout()
        hLayoutUser = QHBoxLayout()
        self.usernameLabel = QLabel('用户名:')
        self.usernameInput = QLineEdit()
        self.usernameInput.textChanged.connect(self.onUsernameChanged)
        hLayoutUser.addWidget(self.usernameLabel)
        hLayoutUser.addWidget(self.usernameInput)

        hLayoutPass = QHBoxLayout()
        self.passwordLabel = QLabel('密码:')
        self.passwordInput = QLineEdit()
        self.passwordInput.textChanged.connect(self.onPasswordChanged)
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password)
        hLayoutPass.addWidget(self.passwordLabel)
        hLayoutPass.addWidget(self.passwordInput)
        userBox.addLayout(hLayoutUser)
        userBox.addLayout(hLayoutPass)
        self.rememberCheckBox = QCheckBox('记住密码', self)
        self.rememberCheckBox.stateChanged.connect(self.handleRememberPassword)
        # 链接按钮
        self.connectButton = QPushButton('连接')
        self.connectButton.clicked.connect(self.connectToDatabase)

        # 数据查询按钮
        self.queryButton = QPushButton('查询数据')
        self.queryButton.clicked.connect(self.queryData)

        # 显示列表
        self.tableWidget = QTableWidget(self)
        self.tableWidget.cellChanged.connect(self.onCellChanged)
        # self.tableWidget.setSelectionMode(QTableWidget.SingleSelection)  # 如果您想要一次只选择一行
        self.tableWidget.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)  # 允许多行选择
        # 连接 selectionChanged 信号到槽函数
        selection_model = self.tableWidget.selectionModel()
        selection_model.selectionChanged.connect(self.onSelectionChanged)

        # 创建菜单栏
        self.menuBar = self.menuBar = QMenuBar(self)

        # 创建数据库菜单
        dbMenu = self.menuBar.addMenu("数据库")
        openDbAction = QAction("打开数据库", self)
        openDbAction.triggered.connect(self.openDatabase)
        dbMenu.addAction(openDbAction)

        closeDbAction = QAction("关闭数据库", self)
        closeDbAction.triggered.connect(self.closeDatabase)
        dbMenu.addAction(closeDbAction)

        # 创建表格处理菜单
        tableMenu = self.menuBar.addMenu("表格处理")
        insertAction = QAction("插入", self)
        insertAction.triggered.connect(self.insertData)
        tableMenu.addAction(insertAction)

        deleteAction = QAction("删除", self)
        deleteAction.triggered.connect(self.deleteData)
        tableMenu.addAction(deleteAction)

        modifyAction = QAction("修改", self)
        modifyAction.triggered.connect(self.modifyData)
        tableMenu.addAction(modifyAction)

        # 创建表格处理菜单
        stdentMenu = self.menuBar.addMenu("学生管理")
        insertAction = QAction("插入", self)
        insertAction.triggered.connect(self.insertStudentData)
        stdentMenu.addAction(insertAction)

        deleteAction = QAction("删除", self)
        deleteAction.triggered.connect(self.deleteStudentData)
        stdentMenu.addAction(deleteAction)

        modifyAction = QAction("修改", self)
        modifyAction.triggered.connect(self.UpdateStudentData)
        stdentMenu.addAction(modifyAction)



        statsMenu = self.menuBar.addMenu("统计")
        countAction = QAction("人数统计", self)
        countAction.triggered.connect(self.countStats)
        statsMenu.addAction(countAction)

        gradeAction = QAction("成绩统计", self)
        gradeAction.triggered.connect(self.gradeStats)
        statsMenu.addAction(gradeAction)

        averageAction = QAction("平均成绩", self)
        averageAction.triggered.connect(self.averageStats)
        statsMenu.addAction(averageAction)

        # 将菜单栏放置在窗口的顶部

        # 添加控件到布局
        vLayout.addLayout(dateBaseBox)
        # vLayout.addLayout(hLayoutUser)
        # vLayout.addLayout(hLayoutPass)
        vLayout.addLayout(userBox)
        vLayout.addWidget(self.rememberCheckBox)
        vLayout.addWidget(self.connectButton)
        vLayout.addWidget(self.queryButton)
        vLayout.addWidget(self.tableWidget)


        # 设置布局
        vLayout.setMenuBar(self.menuBar)
        self.setLayout(vLayout)
        self.setWindowTitle('数据库管理')
        self.resize(800, 600)
        # 菜单动作的处理方法
    def UpdateStudentData(self):
        print("更新学生")
        data = self.queryStudentsDepartmentInfo()  # 调用查询函数
        dialog = MyQDailog.UpdateStudentDialog(self.conn)
        dialog.exec()
    def deleteStudentData(self):
        print("删除学生")
        data = self.queryStudentsDepartmentInfo()  # 调用查询函数
        dialog = MyQDailog.DeleteStudentDialog(self.conn)
        dialog.exec()
    def insertStudentData(self):
        print("插入学生")
        data = self.queryStudentsDepartmentInfo()  # 调用查询函数
        dialog = MyQDailog.NewStudentDialog(self.conn)
        dialog.exec()
    def ondataBaseUrlChanged(self):
         self.dataBaseUrl = self.dataBaseUrlInput.text()
    def ondataBasePortChanged(self):
        self.dataBasePort = self.dataBasePortInput.text()
    def ondataBaseNameChanged(self):
        self.dataBaseName = self.dataBaseNameInput.text()
    def loadCredentials(self):
        # 加载凭据和复选框状态
        try:
            with open("credentials.txt", "r") as file:
                dataBaseUrl = file.readline().strip()
                dataBasePort = file.readline().strip()
                dataBaseName = file.readline().strip()
                username = file.readline().strip()
                password = file.readline().strip()
                remember = file.readline().strip() == 'True'
                self.dataBaseUrlInput.setText(dataBaseUrl)
                self.dataBasePortInput.setText(dataBasePort)
                self.dataBaseNameInput.setText(dataBaseName)
                self.usernameInput.setText(username)
                self.passwordInput.setText(password)
                self.rememberCheckBox.setChecked(remember)
        except FileNotFoundError:
            self.saveCredentials("127.0.0.1", "3306", "HUANYU", self.username, self.password,
                                 self.rememberCheckBox.isChecked())
            self.loadCredentials()
            # 文件不存在，不做任何事情
            pass
    def handleRememberPassword(self, state):
        # 处理记住密码
        if state == 2:  # 如果复选框被勾选

            self.saveCredentials(self.dataBaseUrl,self.dataBasePort,self.dataBaseName,self.username, self.password, self.rememberCheckBox.isChecked())
        else:
            self.deleteCredentials()

    def deleteCredentials(self):
        with open("credentials.txt", "w") as file:
            file.write( "\n")
            file.write( "\n")
    def saveCredentials(self, dataBaseUrl,dataBasePort,dataBaseName,username, password, remember):
        # 保存凭据到文件
        with open("credentials.txt", "w") as file:
            file.write(dataBaseUrl + "\n")
            file.write(dataBasePort + "\n")
            file.write(dataBaseName + "\n")
            file.write(username + "\n")
            file.write(password + "\n")
            file.write(str(remember))

    def read_credentials(filename="credentials.txt"):
        with open(filename, "r") as file:
            username = file.readline().strip()
            password = file.readline().strip()
            return username, password

    def showErrorDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Critical)
        msgBox.setText(message)
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()
    def onSelectionChanged(self, selected, deselected):
        selected_rows = set()
        selected_columns = set()
        for model_index in selected.indexes():
            selected_rows.add(model_index.row())
            selected_columns.add(model_index.column())

        for model_index in deselected.indexes():
            selected_rows.discard(model_index.row())
            selected_columns.discard(model_index.column())
        self.selectedRows = selected_rows
        self.selectedColumns = selected_columns
        print(selected_rows)
        print(selected_columns)
        # 处理选中的行
        for row in selected_rows:
            # 这里可以根据需要进一步处理选中行的数据
            print(f"选中的行: {row}")


    def openDatabase(self):
        try:
            self.conn = pymysql.connect(host=self.dataBaseUrl  # 连接名称，默认127.0.0.1
                                        , user=self.username  # 用户名
                                        , passwd=self.password  # 密码
                                        , port=int(self.dataBasePort)  # 端口，默认为3306
                                        , db=self.dataBaseName  # 数据库名称
                                        , charset='utf8'  # 字符编码
                                        )
            self.isConnected = True
        except pymysql.MySQLError as e:
            print("数据库打开出错：", e)
        print("打开数据库")

    def closeDatabase(self):
        try:
            self.conn.close()
            self.isConnected = False
        except pymysql.MySQLError as e:
            print("数据库关闭出错：", e)
        print("关闭数据库")

    def insertData(self):
        if(self.isConnected):
            studentMap = self.queryStudentInfo()
            classMap = self.queryClassInfo()
            dialog = MyQDailog.InsertDataDialog(self.conn)
            # 在这里可以初始化对话框中的下拉菜单项，例如使用数据库中的数据
            dialog.studentIdCombo.clear()
            for student_id, student_name in studentMap.items():
                dialog.studentIdCombo.addItem(student_name,student_id)
            dialog.classIdCombo.clear()
            for class_id, class_name in classMap.items():
                dialog.classIdCombo.addItem(class_name, class_id)
            # dialog.classIdCombo.addItems(...)
            # dialog.studentIdCombo.addItems(...)

            if dialog.exec():
                # 这里处理用户点击了“插入”按钮的情况
                self.queryData()
                print("数据插入操作已完成")
            else:
                # 这里处理用户点击了“取消”按钮的情况
                print("数据插入操作已取消")
            print("插入数据")
        else:
            self.showErrorDialog("请先链接数据库。")

    def queryStudentInfo(self):
        students_map = {}
        try:
            with self.conn.cursor() as cursor:
                query = "SELECT student_id, student_name FROM t_student_info"
                cursor.execute(query)
                for student_id, student_name in cursor.fetchall():
                    students_map[student_id] = student_name
        except Exception as e:
            print("查询学生信息失败:", e)
        return students_map
    def queryClassInfo(self):
        students_map = {}
        try:
            with self.conn.cursor() as cursor:
                query = "SELECT class_id, class_name FROM t_classinfo"
                cursor.execute(query)
                for class_id, class_name in cursor.fetchall():
                    students_map[class_id] = class_name
        except Exception as e:
            print("查询学生信息失败:", e)

        return students_map
    def deleteData(self):
        if (self.isConnected):
            if(not self.selectedRows is None):
                for row in self.selectedRows:
                    self.deleteGrade(self.results[row][2], self.results[row][3])
                    self.queryData()
                print("删除数据")
            else:
                self.showErrorDialog("请先选择数据。")
        else:
            self.showErrorDialog("请先链接数据库。")

    def modifyData(self):
        print("修改数据")
        for value,classId, studentId in self.newValues:
            self.updateDatabase(value,classId,studentId)



    def countStats(self):
        print("人数统计")
        data = self.queryStudentsDepartmentInfo()  # 调用查询函数
        dialog = MyQDailog.StudentDepartmentDialog(data,self.conn)
        dialog.exec()
    def gradeStats(self):
        print("成绩统计")
        data = self.queryGrades()  # 调用查询函数
        dialog = MyQDailog.GradesDialog(data)
        dialog.exec()

    def queryGrades(self):
        results = []
        try:
            with self.conn.cursor() as cursor:
                query = """
                SELECT t_student_info.student_id, t_student_info.student_name, 
                       t_grade.class_id, t_classinfo.class_name, t_grade.class_grade
                FROM t_student_info
                JOIN t_grade ON t_student_info.student_id = t_grade.student_id
                JOIN t_classinfo ON t_grade.class_id = t_classinfo.class_id
                """
                cursor.execute(query)
                results = cursor.fetchall()  # 获取所有查询结果
        except Exception as e:
            print("查询成绩时发生错误:", e)
        return results

    def averageStats(self):
        print("平均成绩统计")
        data = self.queryAverageGrades()  # 调用查询函数
        dialog = MyQDailog.AverageGradesDialog(data)
        dialog.exec()

    def queryAverageGrades(self):
        results = []
        try:
            with self.conn.cursor() as cursor:
                query = """
                SELECT t_classinfo.class_id, t_classinfo.class_name, AVG(t_grade.class_grade) AS average_grade
                FROM t_grade
                JOIN t_classinfo ON t_grade.class_id = t_classinfo.class_id
                GROUP BY t_classinfo.class_id, t_classinfo.class_name
                """
                cursor.execute(query)
                results = cursor.fetchall()  # 获取所有查询结果
        except Exception as e:
            print("查询平均成绩时发生错误:", e)
        return results

    def onCellChanged(self, row, column):
        newValue = self.tableWidget.item(row, column).text()
        # 假设第一列是课程成绩，第三列是课程ID
        if column == 0:  # 仅当课程成绩列被修改时更新数据库
            classId = self.tableWidget.item(row, 2).text()  # 获取课程ID
            studentId = self.tableWidget.item(row, 3).text()  # 获取课程ID
            dataTuple = (newValue, classId, studentId)
            self.newValues.append(dataTuple)

            # self.updateDatabase( newValue,classId,studentId)
            print("更新数据")

    def queryStudentsDepartmentInfo(self):
        results = []
        try:
            with self.conn.cursor() as cursor:
                query = """
                SELECT t_student_info.student_id, t_student_info.student_name, 
                       t_studentrelation.department_id, t_department.department_name
                FROM t_student_info
                JOIN t_studentrelation ON t_student_info.student_id = t_studentrelation.student_id
                JOIN t_department ON t_studentrelation.department_id = t_department.department_id
                """
                cursor.execute(query)
                results = cursor.fetchall()  # 获取所有查询结果
        except Exception as e:
            print("查询学生和系信息时发生错误:", e)
        return results

    def updateDatabase(self, newValue,classId, studentId):
        try:
            with self.conn.cursor() as cursor:
                query = "UPDATE t_grade SET class_grade = %s WHERE class_id = %s AND student_id = %s"
                cursor.execute(query, (newValue, classId, studentId))
                self.conn.commit()
                print("更新成功")
                self.queryData()
        except pymysql.MySQLError as e:
            print("数据库更新出错：", e)
        # finally:
            # self.conn.close()
    def deleteGrade(self, classId,studentId):
        try:
            with self.conn.cursor() as cursor:
                query = "DELETE FROM t_grade WHERE class_id = %s AND student_id = %s"
                cursor.execute(query, (classId, studentId))
                self.conn.commit()
                print("删除成功")
        except pymysql.MySQLError as e:
            print("数据库删除出错：", e)
        # finally:
            # self.conn.close()
    def onUsernameChanged(self,text):
        self.username = text
        print(text)

    def onPasswordChanged(self,text):
        self.password = text
        print(text)
    def connectToDatabase(self):
        if len(self.username)<1 or len(self.password)<1:
            self.showErrorDialog("用户名或密码不能为空")
            return
        # 数据库连接逻辑
        try:
            self.conn = pymysql.connect(host=self.dataBaseUrl  # 连接名称，默认127.0.0.1
                                   , user=self.username  # 用户名
                                   , passwd=self.password  # 密码
                                   , port=int(self.dataBasePort)  # 端口，默认为3306
                                   , db=self.dataBaseName  # 数据库名称
                                   , charset='utf8'  # 字符编码
                                   )
            self.isConnected = True
        except pymysql.err.OperationalError as e:
            # 捕获特定的 pymysql 错误
            if 'Access denied' in str(e):
                self.showErrorDialog("用户名或密码错误")
            else:
                self.showErrorDialog("数据库连接失败: " + str(e))
            self.isConnected = False
        except Exception as e:
            print("连接失败:", e)
            self.showErrorDialog("连接失败: " + str(e))
            self.isConnected = False
        print("连接数据库")

    def queryData(self):
        # 数据查询逻辑
        try:
            # 假设 self.conn 是一个有效的数据库连接
            cursor = self.conn.cursor()
            query = ("SELECT T_grade.class_grade,T_grade.class_name,T_grade.class_id,T_grade.student_id,"
                     "t_student_info.student_name,t_department.department_id,t_department.department_name FROM T_grade \n"
                     "JOIN t_student_info ON t_student_info.student_id = T_grade.student_id\n"
                     "JOIN t_studentrelation ON t_student_info.student_id = t_studentrelation.student_id \n"
                    "JOIN t_department ON t_studentrelation.department_id = t_department.department_id \n"
                    "ORDER BY student_id"
                     )
            cursor.execute(query)
            self.results = cursor.fetchall()  # 获取所有查询结果
            for i in self.results[:2]:  # 打印输出前2条数据
                print(i)
            print(len(self.results))
            # for row_index, row_data in enumerate(results):
            #     for column_index, item in enumerate(row_data):
            #         print(column_index)
            #         print(item)
            #     print(row_index)
            #     print(row_data)
            print("查询数据")
            self.populateTable(self.results)  # 将结果填充到表格中
        except Exception as e:
            print("查询失败:", e)
        finally:
            cursor.close()  # 确保无论如何都关闭游标

    def queryDataOld(self):
        # 数据查询逻辑
        try:
            # 假设 self.conn 是一个有效的数据库连接
            cursor = self.conn.cursor()
            query = ("SELECT * FROM T_grade ORDER BY student_id\n")
            cursor.execute(query)
            self.results = cursor.fetchall()  # 获取所有查询结果
            for i in self.results[:2]:  # 打印输出前2条数据
                print(i)
            print(len(self.results))
            # for row_index, row_data in enumerate(results):
            #     for column_index, item in enumerate(row_data):
            #         print(column_index)
            #         print(item)
            #     print(row_index)
            #     print(row_data)
            print("查询数据")
            self.populateTableOld(self.results)  # 将结果填充到表格中
        except Exception as e:
            print("查询失败:", e)
        finally:
            cursor.close()  # 确保无论如何都关闭游标
    def populateTableOld(self, data):
        self.clearAllRows()
        try:
            self.tableWidget.cellChanged.disconnect(self.onCellChanged)
        except TypeError:
            # 没有连接，无需断开
            pass

        self.tableWidget.setRowCount(len(data))  # 设置行数
        self.tableWidget.setColumnCount(4)  # 设置列数，假设有4列数据

        # 设置列标题（可选）
        self.tableWidget.setHorizontalHeaderLabels(["课程成绩", "课程名称", "课程ID", "学生ID"])
        # 填充数据
        for row_index, row_data in enumerate(data):
            if row_data is None:
                continue  # 跳过空行数据
            for column_index, item in enumerate(row_data):
                # print(f"设置单元格：行 {row_index}, 列 {column_index}, 值 {item}")
                if item is None:
                    item = ""  # 将 None 转换为空字符串
                self.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(item)))
        self.tableWidget.cellChanged.connect(self.onCellChanged)
    def clearAllRows(self):
        try:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
        except Exception as e:
            print("查询失败:", e)

    def populateTable(self, data):
        self.clearAllRows()
        try:
            self.tableWidget.cellChanged.disconnect(self.onCellChanged)
        except TypeError:
            # 没有连接，无需断开
            pass

        self.tableWidget.setRowCount(len(data))  # 设置行数
        self.tableWidget.setColumnCount(7)  # 设置列数，假设有4列数据

        # 设置列标题（可选）
        self.tableWidget.setHorizontalHeaderLabels(["课程成绩", "课程名称", "课程ID", "学生ID","学生姓名","系ID","系名"])
        # 填充数据
        for row_index, row_data in enumerate(data):
            if row_data is None:
                continue  # 跳过空行数据
            for column_index, item in enumerate(row_data):
                # print(f"设置单元格：行 {row_index}, 列 {column_index}, 值 {item}")
                if item is None:
                    item = ""  # 将 None 转换为空字符串
                self.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(item)))
        self.tableWidget.cellChanged.connect(self.onCellChanged)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue_500.xml')
    ex = DatabaseManager()
    ex.show()
    sys.exit(app.exec())
