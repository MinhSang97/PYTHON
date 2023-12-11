import socket
import threading
import sys
import tkinter as tk
from tkinter import messagebox

class TcpServerForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(self)
        self.start_button["text"] = "Start Server"
        self.start_button["command"] = self.start_server
        self.start_button.pack(side="top")

        self.stop_button = tk.Button(self)
        self.stop_button["text"] = "Stop Server"
        self.stop_button["command"] = self.stop_server
        self.stop_button.pack(side="top")

        self.status_label = tk.Label(self, text="Server Status: Stopped")
        self.status_label.pack(side="top")

        self.command_entry = tk.Entry(self)
        self.command_entry.pack(side="top")

        self.send_button = tk.Button(self)
        self.send_button["text"] = "Send Command"
        self.send_button["command"] = self.send_command
        self.send_button.pack(side="top")

    def start_server(self):
        self.server_thread = threading.Thread(target=self.start_tcp_server)
        self.server_thread.start()
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "normal"
        self.status_label["text"] = "Server Status: Running"

    def stop_server(self):
        self.tcp_server.shutdown()
        self.tcp_server.server_close()
        self.server_thread.join()
        self.start_button["state"] = "normal"
        self.stop_button["state"] = "disabled"
        self.status_label["text"] = "Server Status: Stopped"

    def start_tcp_server(self):
        host = '192.168.30.230'
        port = 11140

        try:
            self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.tcp_server.bind((host, port))
            self.tcp_server.listen(1)
            messagebox.showinfo("TCP Server", f"Server started on {host}:{port}")
        except Exception as e:
            messagebox.showerror("TCP Server", f"Error starting server: {e}")
            self.stop_server()
            return

        while True:
            try:
                client_socket, client_address = self.tcp_server.accept()
                client_thread = threading.Thread(
                    target=self.handle_client_connection, args=(client_socket, client_address)
                )
                client_thread.start()
            except Exception as e:
                messagebox.showerror("TCP Server", f"Error accepting client connection: {e}")
                break

    def handle_client_connection(self, client_socket, client_address):
        message = f"Connected to server at {client_address[0]}:{client_address[1]}"
        print(message)

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Chuyển đổi dữ liệu nhận được thành chuỗi hex
                hex_data = ' '.join([hex(byte)[2:].zfill(2) for byte in data])
                print(f"Received data from {client_address[0]}:{client_address[1]}: {hex_data}")
                
                # Tách chuỗi và lấy giá trị cần thiết
                values = hex_data.split()
                start_index = 8
                length = 8
                selected_value = ''.join(values[start_index:start_index+length])
                print(f"Selected value: {selected_value}")

                # Gửi lệnh tới thiết bị với giá trị đã chọn làm địa chỉ
                command = f"Send command to address: {selected_value}"
                print(command)

                # Gửi dữ liệu phản hồi cho client dưới dạng chuỗi hex
                response = " ".join([hex(byte)[2:].zfill(2) for byte in data])
                client_socket.sendall(response.encode())
            except Exception as e:
                print(f"Error handling client connection: {e}")
                break

        client_socket.close()

    def send_command(self):
        command = self.command_entry.get()
        if command:
            try:
                # Lấy địa chỉ từ chuỗi lệnh
                address = command.strip()
                # Chuyển đổi địa chỉ thành chuỗi hex
                address_hex = ' '.join([hex(int(address[i:i+2], 16))[2:].zfill(2) for i in range(0, len(address), 2)])
                # Gửi địa chỉ dưới dạng chuỗi hex tới thiết bị
                self.tcp_server.sendall(address_hex.encode())
            except Exception as e:
                print(f"Error sending command: {e}")
            self.command_entry.delete(0, "end")


root = tk.Tk()
app = TcpServerForm(master=root)
app.mainloop()
