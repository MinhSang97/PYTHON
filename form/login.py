import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from authenticate import authenticate



def login(username, password, root):
    # Xác thực thông tin đăng nhập
    user = authenticate(username, password)

    if user:
         afterlogin(root)

    else:
        # Đăng nhập thất bại, hiển thị thông báo
        messagebox.showerror("Đăng nhập thất bại", "Tên người dùng hoặc mật khẩu không đúng")


def afterlogin(root):
        
        # Đăng nhập thành công, ẩn giao diện đăng nhập và hiển thị giao diện chính
        root.withdraw()  # Ẩn giao diện đăng nhập

        # Tạo giao diện chính
        main_root = tk.Tk()
        main_root.title("SAVE LOG TASK")

        # getting screen width and height of display
        width = main_root.winfo_screenwidth()
        height = main_root.winfo_screenheight()
        main_root.geometry("%dx%d" % (width, height))
        main_root.geometry("420x380")

         # Khi nhấn nút X trên cửa sổ chính
        main_root.protocol("WM_DELETE_WINDOW", lambda: on_closing(main_root))

        # Tạo frame để chứa label và entry fields cho thông tin kết nối
        connection_frame = tk.Frame(main_root)
        connection_frame.pack(anchor=tk.W)

        # Label và Entry cho Người thực hiện
        label_performer = tk.Label(connection_frame, text="Người thực hiện:")
        label_performer.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
     

        entry_performer = tk.Entry(connection_frame)
        entry_performer.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    

        # Label và Entry cho Nội dung
        label_content = tk.Label(connection_frame, text="Nội dung:")
        label_content.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        # Sử dụng Text widget thay vì Entry để có thể xuống dòng tự động
        text_content = tk.Text(connection_frame, wrap=tk.WORD, height=4)
        text_content.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        label_performer = tk.Label(connection_frame, text="Mức quan trọng:")
        label_performer.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        entry_performer = tk.Entry(connection_frame)
        entry_performer.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
                    
        # Tạo Frame để chứa Treeview và thanh trượt
        result_frame = tk.Frame(root)
        result_frame.pack(fill=tk.BOTH, expand=True)

        # Tạo thanh trượt dọc
        result_tree_yscrollbar = ttk.Scrollbar(result_frame, orient="vertical")
        result_tree_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Tạo thanh trượt ngang
        result_tree_xscrollbar = ttk.Scrollbar(result_frame, orient="horizontal")
        result_tree_xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Tạo Treeview và kết nối với thanh trượt ngang và thanh trượt dọc
        result_tree = ttk.Treeview(result_frame, yscrollcommand=result_tree_yscrollbar.set, xscrollcommand=result_tree_xscrollbar.set)
        result_tree.pack(fill=tk.BOTH, expand=True)

        # Thiết lập thanh trượt ngang và thanh trượt dọc
        result_tree_yscrollbar.configure(command=result_tree.yview)
        result_tree_xscrollbar.configure(command=result_tree.xview)

        # Kết nối thanh trượt ngang và thanh trượt dọc với Treeview
        result_tree.configure(yscrollcommand=result_tree_yscrollbar.set, xscrollcommand=result_tree_xscrollbar.set)

        # Tạo Textbox để hiển thị giá trị khi chọn một dòng trong Treeview
        result_text = tk.Text(root, height=1)
        result_text.pack(fill=tk.X)


        # Khởi chạy vòng lặp sự kiện Tkinter
        root.mainloop()

def on_closing(root):
    if messagebox.askokcancel("Thoát", "Bạn có chắc chắn muốn thoát?"):
        root.destroy()
