import serial.tools.list_ports
import PySimpleGUI as sg

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
            # Thực hiện các hoạt động khác với cổng COM đã kết nối
            # Ví dụ: ser.write() hoặc ser.read()
        else:
            print("Không thể kết nối với cổng COM", com_port)
    except serial.SerialException as e:
        print("Lỗi khi kết nối với cổng COM:", str(e))

# Chọn cổng COM
selected_port = select_com_port()

if selected_port is not None:
    # Kết nối với cổng COM đã chọn
    connect_to_com_port(selected_port)
