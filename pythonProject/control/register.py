from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog, QMessageBox

from design.register import Ui_registerPeople


class register(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.UI = Ui_registerPeople()
        self.UI.setupUi(self)
        self.UI.btn_register.clicked.connect(lambda: self.register())


    def getDatabase(self,val):
        self.db=val
        print(self.db.open())

    def register(self):
        peopleId=self.UI.line_id.text()
        peopleName=self.UI.line_name.text()
        peoplePhone=self.UI.line_phone.text()
        peoplePassword=self.UI.line_password.text()

        if len(peopleId) is 0 or len(peopleName) is 0 or len(peoplePhone) is 0 or len(peoplePassword) is 0:
            QMessageBox.information(self, '提示','信息填写不完整，请检查！',QMessageBox.Yes)
            return

        query = QSqlQuery()

        sql_register = "insert into people values(?,?,?,?)"
        query.prepare(sql_register)
        query.bindValue(0,peopleId)
        query.bindValue(1,peopleName)
        query.bindValue(2,peoplePhone)
        query.bindValue(3,peoplePassword)
        print(peopleId)
        print(peopleName)
        print(peoplePhone)
        print(peoplePassword)

        if query.exec_():
            self.close()
            QMessageBox.information(self, '提示', '注册成功', QMessageBox.Yes)
        else:
            QMessageBox.information(self, '提示', '注册失败', QMessageBox.Yes)
