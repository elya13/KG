from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QVBoxLayout, QTableView, QTableWidget, QTableWidgetItem
import sys
server = 'ELINAAPTINE2EB8\SQLEXPRESS'
database = 'KG'

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if createConnection():
        Sql_stat = '''select
Child.Child_Surname,
Child.Child_Name,
[Group].Group_name
from [Group]
join Child on [Group].Group_id = Child.Group_id'''
        dataView = displayData(Sql_stat)
        dataView.show()

    app.exit()
    sys.exit(app.exec_())
