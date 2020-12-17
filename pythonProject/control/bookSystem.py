from PyQt5 import QtCore, QtSql
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QMessageBox

from control.book import book
from design.bookSystem import Ui_bookSystemMain


class bookSystem(QDialog):
    # 定义一个信号
    signal_1 = QtCore.pyqtSignal(QtSql.QSqlDatabase)
    signal_2 = QtCore.pyqtSignal(QtSql.QSqlDatabase,list)
    model =QStandardItemModel(0, 4)
    model.setHorizontalHeaderLabels(['编号', '书名','作者','库存'])

    def __init__(self):
        QDialog.__init__(self)
        self.UI = Ui_bookSystemMain()
        self.UI.setupUi(self)
        self.UI.btn_addBook.clicked.connect(lambda:self.addbook())
        self.UI.btn_delBook.clicked.connect(lambda:self.delBook())
        self.UI.btn_reviseBook.clicked.connect(lambda:self.reviseBook())
        self.UI.btn_search.clicked.connect(lambda:self.searchBook())
        self.UI.btn_exit.clicked.connect(lambda:self.exitSystem())

        self.UI.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers);
        self.UI.tableView.setSelectionBehavior(QAbstractItemView.SelectRows);

        self.updateTableView()

    def exitSystem(self):
        self.close()

    def getDatabase(self,val):
        self.db=val
        print(self.db.open())


    #添加书本
    def addbook(self):
        addBook = book()
        self.signal_1.connect(addBook.getDatabase)
        self.signal_1.emit(self.db)
        addBook.exec_()
        self.updateTableView()

    #删除书本
    def delBook(self):
        list = self.UI.tableView.selectionModel().selectedRows()

        query = QSqlQuery()
        count=0
        sql_delBook="delete from book where bookId=?"
        for index in list:
            count=count+1
            print(self.model.item(index.row(),0).text())
            query.prepare(sql_delBook)
            query.bindValue(0,self.model.item(index.row(),0).text())
            query.exec_()
        if count:
            self.updateTableView()
            QMessageBox.information(self, '提示', '已删除成功%d个记录'%(count), QMessageBox.Yes)
    #修改书本
    def reviseBook(self):
        index = self.UI.tableView.selectionModel().currentIndex();
        oldBook=[]
        oldBook.append(self.model.item(index.row(),0).text())
        oldBook.append(self.model.item(index.row(),1).text())
        oldBook.append(self.model.item(index.row(),2).text())
        oldBook.append(self.model.item(index.row(),3).text())

        addBook = book()
        self.signal_2.connect(addBook.getOldBook)
        self.signal_2.emit(self.db,oldBook)
        addBook.exec_()
        self.updateTableView()

    def searchBook(self):
        index = self.UI.comboBox.currentIndex()

        searchText = self.UI.line_context.text()
        if len(searchText) is 0:
            QMessageBox.information(self, '提示', '请输入要搜索的内容！', QMessageBox.Yes)
            return



        query = QSqlQuery()

        sql_searchAll ="select * from book"
        sql_searchBookId="select * from book where bookId =?"
        sql_searchBookName="select * from book where bookName =?"
        sql_searchBookAuthor="select * from book where author =?"
        print(index)
        print(searchText)
        if index==1:
            query.prepare(sql_searchAll)
            query.exec_()
        if index==2:
            query.prepare(sql_searchBookId)
            query.bindValue(0, searchText)
            query.exec_()
        if index==3:
            query.prepare(sql_searchBookName)
            query.bindValue(0, searchText)
            query.exec_()
        if index == 4:
            query.prepare(sql_searchBookAuthor)
            query.bindValue(0, searchText)
            query.exec_()

        if query.next():

            self.model.clear()
            self.model.setColumnCount(4)
            self.model.setHorizontalHeaderLabels(['编号', '书名', '作者', '库存'])

            for column in range(4):
                item = QStandardItem("%s" % (query.value(column)))
                # 设置每个位置的文本值
                self.model.setItem(0, column, item)

            row =1

            while query.next():
                for column in range(4):
                    item = QStandardItem("%s" % (query.value(column)))
                    # 设置每个位置的文本值
                    self.model.setItem(row, column, item)
                row=row+1

        else:
            QMessageBox.information(self, '提示', '查询不到内容！', QMessageBox.Yes)

    #更新tableView
    def updateTableView(self):
        query = QSqlQuery()

        sql_getBookCount = "select count(*) from book"
        query.exec_(sql_getBookCount)
        query.next()
        bookCount = query.value(0)

        if bookCount:
            self.model.setRowCount(bookCount)

            sql_getBook = "select * from book order by bookId"
            query.exec_(sql_getBook)

            for row in range(bookCount):
                query.next()
                for column in range(4):
                    item = QStandardItem("%s"%(query.value(column)))
                    # 设置每个位置的文本值
                    self.model.setItem(row, column, item)

            self.UI.tableView.setModel(self.model)
        else:
            for column in range(4):
                item = QStandardItem("")
                # 设置每个位置的文本值
                self.model.setItem(0, column, item)
            self.UI.tableView.setModel(self.model)