
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTableView,  QDesktopWidget,
                             QHBoxLayout, QLabel, QPushButton, )
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtSql import *


#соединение с базой данных
server = 'ELINAAPTINE2EB8\SQLEXPRESS'
database = 'KG'

WIDTH = 480
HEIGHT = 360

def createConnection():
    connString = 'DRIVER={ODBC Driver 17 for SQL Server}; \
                                           SERVER=' + server + '; \
                                            DATABASE=' + database + '; \
                                            Trusted_connection=yes;'
    global db
    db = QSqlDatabase.addDatabase('QODBC')
    db.setDatabaseName(connString)
    if db.open():
        print('connected successfully')
        return True
    else:
        print('fail')
        return False

def displayData(sqlStat):
    print('wait..')
    qry = QSqlQuery(db)
    qry.prepare(sqlStat)
    qry.exec()

    model= QSqlQueryModel()
    model.setQuery(qry)

    view= QTableView()
    view.setModel(model)
    return view

class Kinder_garden(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.btn1.clicked.connect(self.show_children)
        self.btn2.clicked.connect(self.show_educators)
        self.btn3.clicked.connect(self.show_attendance)
        self.btn4.clicked.connect(self.show_marks)
        self.btn5.clicked.connect(self.show_classes)

    def initUI(self):
        hbox = QHBoxLayout(self) #создание фоновой картинки
        pixmap = QPixmap("//Mac/Home/Pictures/kinder.png")
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.btn1 = QPushButton("Дети", self)
        self.btn1.resize(90, 50)
        self.btn1.move(90, 90)

        self.btn2 = QPushButton("Воспитатели", self)
        self.btn2.resize(90, 50)
        self.btn2.move(90, 150)

        self.btn3 = QPushButton("Посещение", self)
        self.btn3.resize(90, 50)
        self.btn3.move(90, 210)

        self.btn4 = QPushButton("Оценки", self)
        self.btn4.resize(90, 50)
        self.btn4.move(300, 90)

        self.btn5 = QPushButton("Доп. \n занятия", self)
        self.btn5.resize(90, 50)
        self.btn5.move(300, 150)

        self.btn6 = QPushButton("Выход", self)
        self.btn6.clicked.connect(QCoreApplication.instance().quit)
        self.btn6.resize(90, 50)
        self.btn6.move(300, 210)


        self.resize(WIDTH, HEIGHT)
        self.center()  # по центру экрана
        self.setWindowTitle('Детский сад') #название окна
        self.show()

    def center(self):  # Выводит окно в центр экрана
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

    def show_children(self):
        self.ch = Children()

    def show_educators(self):
        self.educators = Educator()

    def show_marks(self):
        self.marks = Marks()

    def show_attendance(self):
        self.attend = Attendance()

    def show_classes(self):
        self.classe = Classes()



class Children(QWidget):
    def __init__(self):
        super(Children, self).__init__()
        if createConnection():
            self.Sql_stat = '''select
            Child.Child_Surname as 'Фамилия_ребенка',
            Child.Child_Name as 'Имя_ребенка',
            [Group].Group_name as 'Название_группы'
            from [Group]
            join Child on [Group].Group_id = Child.Group_id'''
            self.dataView = displayData(self.Sql_stat)
            self.dataView.show()
            self.dataView.setWindowTitle('Дети')
            self.dataView.resize(400, 600)


class Educator(QWidget):
    def __init__(self):
        super(Educator, self).__init__()

        if createConnection():
            self.Sql_stat = '''select
            Educator.Educator_Surname as 'Фамилия',
            Educator.Educator_Name as 'Имя'
            from Educator'''
            self.dataView = displayData(self.Sql_stat)
            self.dataView.show()
            self.dataView.setWindowTitle('Воспитатели')
            self.dataView.resize(250, 350)

class Attendance(QWidget):
    def __init__(self):
        super(Attendance, self).__init__()

        if createConnection():
            self.Sql_stat = '''select
            Child.Child_Surname as 'Фамилия_ребенка',
            Child.Child_Name as 'Имя_ребенка'
            from Child
            join Child_Time on Child_Time.Child_id = Child.Child_id
            where Child_Time.Date = '2020-05-21' '''
            self.dataView = displayData(self.Sql_stat)
            self.dataView.show()
            self.dataView.setWindowTitle('Посещение')
            self.dataView.resize(300, 300)

class Marks(QWidget):
    def __init__(self):
        super(Marks, self).__init__()

        if createConnection():
            self.Sql_stat = '''select
            Child.Child_Surname as 'Фамилия_ребенка',
            Child.Child_Name as 'Имя_ребенка',
            Mark.Grade as 'Оценка',
            (select AVG(Mark.Grade) from Mark) as 'Сред. оценка'
            from Mark
            join Child on Mark.Child_id = Child.Child_id
            order by Mark.Grade desc '''
            self.dataView = displayData(self.Sql_stat)
            self.dataView.show()
            self.dataView.setWindowTitle('Оценки')
            self.dataView.resize(430, 510)

class Classes(QWidget):
    def __init__(self):
        super(Classes, self).__init__()

        if createConnection():
            self.Sql_stat = '''select
            Educator.Educator_Surname as 'Фамилия',
            Educator.Educator_Name as 'Имя',
            Schedule.Class_name as 'Занятие'
            from Educator
            join Schedule on Schedule.Class_id = Educator.Class_id '''

            self.dataView = displayData(self.Sql_stat)
            self.dataView.show()
            self.dataView.setWindowTitle('Доп.занятия')
            self.dataView.resize(350, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Kinder_garden()
    sys.exit(app.exec_())


