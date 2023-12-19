from authenticate import authenticate
from login import login
import pyodbc

def create_row():

    authenticate.cursor()

    try:
        authenticate.cursor()

        # Lấy giá trị user_name và password từ người dùng
        user_name = login.entry_performer.get()


        # Kiểm tra xem người dùng đã nhập đủ thông tin hay chưa
        if user_name and passAPI:
            # Thực hiện câu truy vấn SQL để chèn dữ liệu
            insert_query = "INSERT INTO Tokens (user_name, password) VALUES (:user_name, :password)"
            authenticate.cursor.execute(insert_query, {'user_name': user_name, 'password': passAPI})

            authenticate.cursor.commit()
            messagebox.showinfo("Create Row", f'''User and Password created successfully.
User: {user_name}  Pass: {passAPI}''')
        else:
            messagebox.showwarning("Incomplete Information", "Please enter both user_name and password.")

    except cx_Oracle.Error as error:
        messagebox.showerror("Error", f"Error: {error}")
    finally:
        if conn:
            conn.close()