import sys

from PyQt5 import QtSql, QtCore
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from control.bookSystem import bookSystem
from control.register import register
from design.login import Ui_login



class Login(QMainWindow):
    #定义一个信号
    signal_1 = QtCore.pyqtSignal(QtSql.QSqlDatabase)

    def __init__(self):
        QMainWindow.__init__(self)
        self.UI = Ui_login()
        self.UI.setupUi(self)
        self.UI.btn_login.clicked.connect(lambda :self.login())
        self.UI.btn_register.clicked.connect(lambda :self.register())
        self.connectSqlite()
        self.createDb()

    #连接数据库
    def connectSqlite(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('./bookmanage.database')
        self.db.open()

    #创建表
    def createDb(self):
        query = QSqlQuery()
        query.exec_("CREATE TABLE if not exists people("
                    "id VARCHAR(255) PRIMARY KEY,"
                    "peopleName VARCHAR(255),"
                    "telephone VARCHAR(255),"
                    "PASSWORD VARCHAR(255))")
        query.exec_("CREATE TABLE if not exists book("
                    "bookId VARCHAR(255) PRIMARY KEY,"
                    "bookName VARCHAR(255),"
                    "author VARCHAR(255),"
                    "bookNum int)")
    #登录
    def login(self):
        query = QSqlQuery()
        peopleId = self.UI.line_Id.text()
        peopleName = self.UI.line_password.text()
        if len(peopleId) is 0 or len(peopleName) is 0:
            QMessageBox.information(self, '提示','工号或密码不能为空！',QMessageBox.Yes)
            return

        searchPeople = "select * from people where id=? and PASSWORD = ?"
        query.prepare(searchPeople)
        query.bindValue(0,peopleId)
        query.bindValue(1,peopleName)
        query.exec_()

        if query.next():
            # print("有这个人")
            bookSystemMain=bookSystem()
            self.signal_1.connect(bookSystemMain.getDatabase)
            self.signal_1.emit(self.db)
            self.close()
            bookSystemMain.exec_()
        else:
            print("账号或密码错误，请检查！")

    #注册
    def register(self):
        registerPeople=register()
        self.signal_1.connect(registerPeople.getDatabase)
        self.signal_1.emit(self.db)
        registerPeople.exec_()







if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Login()
    mainWindow.show()
    sys.exit(app.exec_())