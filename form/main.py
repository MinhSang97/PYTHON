import tkinter as tk
from tkinter import messagebox
from login import login

def main():
    def on_closing():
        if messagebox.askokcancel("Thoát", "Bạn có chắc chắn muốn thoát?"):
            root.destroy()

    root = tk.Tk()

    root.title("Đăng nhập")

    

    # Set the size of the main window
    root.geometry("300x250")

    # Tạo và định vị các widget
    username_label = tk.Label(root, text="Tên người dùng:")
    username_label.pack(pady=10)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=10)

    password_label = tk.Label(root, text="Mật khẩu:")
    password_label.pack(pady=10)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=10)

    def login_callback(event=None):
        login(username_entry.get(), password_entry.get(), root)

    login_button = tk.Button(root, text="Đăng nhập", command=login_callback)
    login_button.pack(pady=20)

    # Bind the <Return> key event to the login_callback function
    root.bind('<Return>', login_callback)

    # Bind the closing event to the on_closing function
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Chạy vòng lặp sự kiện Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
