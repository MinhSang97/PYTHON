import cx_Oracle
import hashlib
import tkinter as tk
from tkinter import messagebox

# Kết nối tới cơ sở dữ liệu Oracle
dsn_tns = cx_Oracle.makedsn('118.69.35.119', '1521', service_name='hhm')
conn = cx_Oracle.connect(user='MiniMDM10', password='MiniMDM10', dsn=dsn_tns)

def check_token():
    # Lấy giá trị token từ người dùng nhập vào
    token_to_check = entry_token.get()

    # Thực hiện truy vấn để lấy danh sách các token trong cơ sở dữ liệu
    select_query = "SELECT token FROM Tokens"
    cursor = conn.cursor()
    cursor.execute(select_query)
    db_tokens = [row[0] for row in cursor.fetchall()]
    cursor.close()

    # Kiểm tra từng token trong cơ sở dữ liệu
    for db_token in db_tokens:
        if len(db_token) == len(token_to_check) and all(a == b for a, b in zip(db_token, token_to_check)):
            messagebox.showinfo('Kết quả', 'Token hợp lệ!')
            return

    messagebox.showinfo('Kết quả', 'Token không hợp lệ!')

# Tạo giao diện WinForm sử dụng thư viện tkinter
window = tk.Tk()
window.title('Kiểm tra tính hợp lệ của token')

label_token = tk.Label(window, text='Nhập token cần kiểm tra:')
label_token.pack()

entry_token = tk.Entry(window)
entry_token.pack()

button_check = tk.Button(window, text='Kiểm tra', command=check_token)
button_check.pack()

window.mainloop()
