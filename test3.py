import pyodbc
import pandas as pd
#from tkinter import *
import tkinter as ttk
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Kết nối đến SQL Server")
        self.master.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        # Tạo các label và entry để nhập thông tin kết nối
        self.label_user = tk.Label(self.master, text="User:")
        self.label_user.grid(row=0, column=0, padx=10, pady=10)
        self.entry_user = tk.Entry(self.master)
        self.entry_user.grid(row=0, column=1, padx=10, pady=10)

        self.label_password = tk.Label(self.master, text="Password:")
        self.label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password = tk.Entry(self.master, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.label_server = tk.Label(self.master, text="Server:")
        self.label_server.grid(row=2, column=0, padx=10, pady=10)
        self.entry_server = tk.Entry(self.master)
        self.entry_server.grid(row=2, column=1, padx=10, pady=10)

        self.label_database = tk.Label(self.master, text="Database:")
        self.label_database.grid(row=3, column=0, padx=10, pady=10)
        self.entry_database = tk.Entry(self.master)
        self.entry_database.grid(row=3, column=1, padx=10, pady=10)

        # Tạo nút kết nối
        self.button_connect = tk.Button(self.master, text="Kết nối", command=self.connect_to_database)
        self.button_connect.grid(row=4, column=0, padx=10, pady=10)

        # Tạo label và entry để nhập lệnh truy vấn
        self.label_query = tk.Label(self.master, text="Lệnh truy vấn:")
        self.label_query.grid(row=5, column=0, padx=10, pady=10)
        self.entry_query = tk.Entry(self.master)
        self.entry_query.grid(row=5, column=1, padx=10, pady=10)

        # Tạo nút truy vấn và nút xuất file Excel
        self.button_query = tk.Button(self.master, text="Truy vấn", command=self.execute_query)
        self.button_query.grid(row=6, column=0, padx=10, pady=10)
        self.button_export = tk.Button(self.master, text="Xuất Excel", command=self.export_to_excel)
        self.button_export.grid(row=6, column=1, padx=10, pady=10)
    def connect_to_database(self):
        user = self.entry_user.get()
        password = self.entry_password.get()
        server = self.entry_server.get()
        database = self.entry_database.get()

        # Kết nối đến SQL Server
        connection_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password};"
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()

        print("Đã kết nối đến SQL Server")

    def execute_query(self):
        query = self.entry_query.get()

        # Thực thi lệnh truy vấn
        self.cursor.execute(query)

        # Lấy kết quả truy vấn
        result = self.cursor.fetchall()

        # Hiển thị kết quả trên console
        for row in result:
            print(row)

    def export_to_excel(self):
        # Chọn vị trí lưu file Excel
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

        query = self.entry_query.get()

        # Thực thi lệnh truy vấn
        self.cursor.execute(query)

        # Lấy kết quả truy vấn
        result = self.cursor.fetchall()

        # Tạo DataFrame từ kết quả truy vấn
        df = pd.DataFrame(result)

        # Ghi DataFrame vào file Excel
        df.to_excel(file_path, index=False)

        print("Đã xuất dữ liệu ra file Excel")

