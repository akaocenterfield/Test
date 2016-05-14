import pyodbc
import pandas.io.sql as psql
import datetime

cnxn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=server;Database=database;UID=user;PWD=123')
qry = "select top 10 * from database where id = 1234"
a = datetime.datetime.now()
df = psql.read_sql(qry, cnxn)
b = datetime.datetime.now()
print b - a
