import requests
import json
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import pandas as pd
from tkinter import HORIZONTAL
import datetime

def format_thoi_gian(thoi_gian):
    # Chuyển đổi thời gian thành đối tượng datetime
    dt = datetime.datetime.strptime(thoi_gian, "%d-%b-%y")
    # Format thời gian theo định dạng mong muốn
    formatted_thoi_gian = dt.strftime("%d-%b-%y")
    return formatted_thoi_gian


def get_data():
    cong_to = cong_to_entry.get()
    thoi_gian = thoi_gian_entry.get()

    # Format thời gian
    formatted_thoi_gian = format_thoi_gian(thoi_gian)

    url = "http://192.168.30.252:5050/data"
    params = {
        "cong_to": cong_to,
        "thoi_gian": thoi_gian
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            json_data = response.text
            data = json.loads(json_data)

            # Phân tích chuỗi JSON thành DataFrame
            df = pd.DataFrame(data)

            # Xóa dữ liệu cũ trong Treeview
            tree.delete(*tree.get_children())

            # Thiết lập dữ liệu cho Treeview
            for index, row in df.iterrows():
                tree.insert("", tk.END, values=row.tolist())
        else:
            tree.delete(*tree.get_children())
            tree.insert("", tk.END, values=("Error: Unable to fetch data from the API.",))
    except requests.exceptions.RequestException as e:
        tree.delete(*tree.get_children())
        tree.insert("", tk.END, values=("Error: " + str(e),))

root = tk.Tk()
root.title("API Test")
root.geometry("800x400")

# Khung nhập thông tin
input_frame = ttk.LabelFrame(root, text="Thông tin")
input_frame.pack(pady=10)

cong_to_label = ttk.Label(input_frame, text="Nhập số công tơ:")
cong_to_label.grid(row=0, column=0, padx=10, pady=5)
cong_to_entry = ttk.Entry(input_frame)
cong_to_entry.grid(row=0, column=1, padx=10, pady=5)

thoi_gian_label = ttk.Label(input_frame, text="Nhập thời gian: theo dạng sau 09-MAR-23")
thoi_gian_label.grid(row=1, column=0, padx=10, pady=5)
thoi_gian_entry = ttk.Entry(input_frame)
thoi_gian_entry.grid(row=1, column=1, padx=10, pady=5)

get_data_button = ttk.Button(root, text="Get Data", command=get_data)
get_data_button.pack(pady=10)

# Khung hiển thị kết quả
result_frame = ttk.LabelFrame(root, text="Kết quả")
result_frame.pack(pady=10)

columns = ("MÃ_ĐIỂM_ĐO", "TENKHACHHANG", "NOCONGTO", "THOIGIANDCUTRADULIEU", "DIENHUUCONGCHIEUGIAO",
           "DIENHUUCONGCHIEUGIAO_BIEU1", "DIENHUUCONGCHIEUGIAO_BIEU2", "DIENHUUCONGCHIEUGIAO_BIEU3",
           "DIENHUUCONGCHIEUNHAN", "DIENHUUCONGCHIEUNHAN_BIEU1", "DIENHUUCONGCHIEUNHAN_BIEU2",
           "DIENHUUCONGCHIEUNHAN_BIEU3")

result_frame = tk.Frame(root)
result_frame.pack(fill=tk.BOTH, expand=True)

result_tree_yscrollbar = ttk.Scrollbar(result_frame, orient="vertical")
result_tree_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_tree_xscrollbar = ttk.Scrollbar(result_frame, orient="horizontal")
result_tree_xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

tree = ttk.Treeview(result_frame, columns=columns, show="headings",
                    yscrollcommand=result_tree_yscrollbar.set, xscrollcommand=result_tree_xscrollbar.set)

for column in columns:
    tree.heading(column, text=column)
    tree.column(column, width=100, anchor=tk.CENTER)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

result_tree_yscrollbar.configure(command=tree.yview)
result_tree_xscrollbar.configure(command=tree.xview)

tree.configure(yscrollcommand=result_tree_yscrollbar.set, xscrollcommand=result_tree_xscrollbar.set)

root.mainloop()
