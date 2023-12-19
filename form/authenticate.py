import pyodbc

def authenticate(username, password):
    # Kết nối đến cơ sở dữ liệu
    connection_string = "DRIVER={SQL Server};SERVER=192.168.40.253;DATABASE=TASK;UID=amr;PWD=123456"
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Thực hiện truy vấn kiểm tra tên người dùng và mật khẩu
    query = f"SELECT * FROM Users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    # Đóng kết nối
    cursor.close()
    connection.close()

    return user