

import pyodbc
from tabulate import tabulate
driver = 'ODBC Driver 17 for SQL Server'
server = '192.168.40.253'
db1 = 'SPC'
tcon = 'yes'
uname = 'amr'
pword = '123456'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.40.253;DATABASE=SPC;UID=amr;PWD=123456')
cursor = cnxn.cursor()
cursor.execute("select t.fcDcuAddr,t.fcMeterAddr,t.dnngay, t.fiFn, c.fcMa_Khang madiemdo4 , c.fcTen_Khang tenkh , c.fcDia_Chi from  (select b.fcSaleID, a.fcDcuAddr, a.fcMeterAddr, a.fcEnergy dnngay, a.fiFn from FreezeData a inner join Meter b on a.fcMeterAddr=b.fcMeterAddr and a.ftReadTime>='20230401' and a.ftReadTime<'20230402' and a.fifn>='219') t  inner join Meter c on c.fcMeterAddr=t.fcMeterAddr")
rows = cursor.fetchall()
for row in rows:
  col_names= ["no dcu", "no công tơ", "csdn", "fifn", "madiemdo", "tenkh","diachi"]

print(tabulate(rows, headers=col_names, tablefmt="fancy_grip", showindex="always"))