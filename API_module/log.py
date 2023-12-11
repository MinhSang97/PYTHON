import cx_Oracle
import datetime

# Thiết lập thông tin kết nối với cơ sở dữ liệu Oracle
dsn_tns = cx_Oracle.makedsn('118.69.35.119', '1521', service_name='hhm')
conn = cx_Oracle.connect(user='MiniMDM10', password='MiniMDM10', dsn=dsn_tns)

# Hàm lưu log
def save_log(token, cong_to, thoi_gian):
    current_time = datetime.datetime.now()
    
    insert_query = "INSERT INTO Logs (token, cong_to, thoi_gian, thoi_gian_hien_tai) VALUES (:token, :cong_to, :thoi_gian, :thoi_gian_hien_tai)"
    cursor = conn.cursor()
    cursor.execute(insert_query, token=token, cong_to=cong_to, thoi_gian=thoi_gian, thoi_gian_hien_tai=current_time)
    conn.commit()
    cursor.close()
