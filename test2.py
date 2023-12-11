import serial.tools.list_ports
import PySimpleGUI as sg
import threading

def select_com_port():
    # Lấy danh sách tất cả các cổng COM đang có
    ports = serial.tools.list_ports.comports()
    
    # Kiểm tra xem có cổng COM nào được tìm thấy hay không
    if len(ports) == 0:
        print("Không tìm thấy cổng COM.")
        return None
    
    # Tạo danh sách các cổng COM đã tìm thấy
    port_list = [port.device for port in ports]
    
    # Tạo giao diện chọn cổng COM
    layout = [
        [sg.Text("Chọn cổng COM:")],
        [sg.Combo(port_list, key="-PORT-", enable_events=True)],
        [sg.Button("Chọn", key="-SELECT-")]
    ]
    
    window = sg.Window("Chọn cổng COM", layout)
    
    # Xử lý sự kiện
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-SELECT-":
            selected_port = values["-PORT-"]
            window.close()
            return selected_port
    
    window.close()
    return None

def connect_to_com_port(com_port):
    try:
        # Tạo đối tượng Serial với tốc độ truyền dữ liệu là 9600 và timeout là 1 giây
        ser = serial.Serial(com_port, 9600, timeout=1)
        
        # Kiểm tra xem kết nối đã được thiết lập thành công hay không
        if ser.is_open:
            print("Đã kết nối với cổng COM", com_port)
            return ser
        else:
            print("Không thể kết nối với cổng COM", com_port)
    except serial.SerialException as e:
        print("Lỗi khi kết nối với cổng COM:", str(e))
    
    return None

def send_command_to_com_port(ser, command):
    try:
        # Gửi lệnh đi
        ser.write(command.encode())
        
        # Đọc phản hồi từ cổng COM (tuỳ thuộc vào thiết bị và giao thức)
        response = ser.read(100)  # Đọc tối đa 100 byte
        
        # Hiển thị phản hồi
        print("Phản hồi từ cổng COM:", response)
        
        return response
        
    except serial.SerialException as e:
        print("Lỗi khi gửi lệnh tới cổng COM:", str(e))
    
    return None

def send_command_with_timeout(ser, command):
    response = None
    
    # Tạo luồng riêng để gửi lệnh
    def send_command():
        nonlocal response
        response = send_command_to_com_port(ser, command)
    
    thread = threading.Thread(target=send_command)
    thread.start()
    thread.join(timeout=60)  # Chờ đợi luồng kết thúc trong khoảng thời gian timeout
    
    if thread.is_alive():
        print("Timeout khi gửi lệnh.")
        response = None
        thread.join()  # Đảm bảo kết thúc luồng
    
    return response

# Chọn cổng COM
selected_port = select_com_port()

if selected_port is not None:
    # Kết nối tới cổng COM đã chọn
    ser = connect_to_com_port(selected_port)
    
    if ser is not None:
        # Tạo giao diện nhập lệnh và hiển thị dữ liệu phản hồi
        layout = [
            [sg.Text("Nhập lệnh:")],
            [sg.Input(key="-COMMAND-")],
            [sg.Button("Gửi", key="-SEND-")],
            [sg.Multiline(size=(60, 10), key="-LOG-", autoscroll=True)]  # Vùng hiển thị log
        ]
        
        window = sg.Window("Gửi lệnh tới cổng COM", layout)
        
        # Xử lý sự kiện
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            if event == "-SEND-":
                command = values["-COMMAND-"]
                response = send_command_with_timeout(ser, command)
                log_text = f"Lệnh: {command}\nPhản hồi: {response}\n\n"
                window["-LOG-"].print(log_text)
        
        window.close()
        
        # Đóng kết nối
        ser.close()
