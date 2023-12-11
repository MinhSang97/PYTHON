import serial.tools.list_ports as list_ports
import time
import tkinter as tk
from tkinter import ttk
import serial
from serial import SerialException

BAUD_RATE_DEFAULT = 300

class SerialCommunication:
    def __init__(self, response_text):
        self.serial = None
        self.baud_rate = 300
        self.data_bits = serial.SEVENBITS
        self.parity = serial.PARITY_EVEN
        self.stop_bits = serial.STOPBITS_ONE
        self.response_text = response_text

    def connect(self, port):
        try:
            self.serial = serial.Serial(port, baudrate=self.baud_rate,
                                        bytesize=self.data_bits, parity=self.parity,
                                        stopbits=self.stop_bits, timeout=1)
            return True
        except serial.SerialException:
            return False

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        if self.serial:
            self.serial.baudrate = self.baud_rate

    def set_data_bits(self, data_bits):
        self.data_bits = data_bits
        if self.serial:
            self.serial.bytesize = self.data_bits

    def set_parity(self, parity):
        self.parity = parity
        if self.serial:
            self.serial.parity = self.parity

    def set_stop_bits(self, stop_bits):
        self.stop_bits = stop_bits
        if self.serial:
            self.serial.stopbits = self.stop_bits

    def send_command(self, command):
        if self.serial:
            # Get the current timestamp
            timestamp = time.strftime("%d/%m/%Y %H:%M:%S")

            # Update the response_text widget
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert(tk.END, f"[{timestamp}] Written data ({self.serial.port})\n")

            # Convert command to hex format
            command_hex = " ".join([f"{ord(c):02x}" for c in command])
            self.response_text.insert(tk.END, f"{command_hex} {' ' * (20 - len(command_hex))} {command}\n")

            # Encode the command string to bytes and send it
            command_bytes = command.encode('utf-8')
            self.serial.write(command_bytes)
            self.serial.flush()

            # Read the response
            response = self.serial.readline().strip()

            self.response_text.insert(tk.END, f"[{timestamp}] Read data ({self.serial.port})\n")

            # Convert response to hex format
            response_hex = " ".join([f"{byte:02x}" for byte in response])
            self.response_text.insert(tk.END, f"{response_hex} {''.join([' ' for _ in range(20 - len(response_hex))])} {response.decode('utf-8')}\n")



    def read_response(self):
        if self.serial:
            response = self.serial.readline().strip()

            # Get the current timestamp
            timestamp = time.strftime("%d/%m/%Y %H:%M:%S")

            self.response_text.insert(tk.END, f"[{timestamp}] Read data ({self.serial.port})\n")

            # Convert response to hex format
            response_hex = " ".join([f"{byte:02x}" for byte in response])
            self.response_text.insert(tk.END, f"{response_hex} {''.join([' ' for _ in range(20 - len(response_hex))])} {response.decode('utf-8')}\n")

            return response

    def disconnect(self):
        if self.serial:
            self.serial.close()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Serial Communication")
        self.geometry("800x600")

        self.serial_comm = None

        self.com_port_label = ttk.Label(self, text="COM Port:")
        self.com_port_label.pack()

        self.com_port_combobox = ttk.Combobox(self)
        self.com_port_combobox.pack()

        self.connect_button = ttk.Button(self, text="Connect", command=self.connect_to_port)
        self.connect_button.pack()

        self.data_bits_label = ttk.Label(self, text="Data Bits:")
        self.data_bits_label.pack()

        self.data_bits_combobox = ttk.Combobox(self, values=["5", "6", "7", "8"])
        self.data_bits_combobox.pack()

        self.parity_label = ttk.Label(self, text="Parity:")
        self.parity_label.pack()

        self.parity_combobox = ttk.Combobox(self, values=["NONE", "EVEN", "ODD"])
        self.parity_combobox.pack()

        self.stop_bits_label = ttk.Label(self, text="Stop Bits:")
        self.stop_bits_label.pack()

        self.stop_bits_combobox = ttk.Combobox(self, values=["1", "1.5", "2"])
        self.stop_bits_combobox.pack()

        self.send_button = ttk.Button(self, text="Send", command=self.send_command)
        self.send_button.pack()

        self.command_entry = ttk.Entry(self)
        self.command_entry.pack()

        self.response_label = ttk.Label(self, text="Response:")
        self.response_label.pack()

        self.response_text = tk.Text(self, height=5)
        self.response_text.pack()

        self.disconnect_button = ttk.Button(self, text="Disconnect", command=self.disconnect_from_port)
        self.disconnect_button.pack()

        self.update_com_ports()

    def update_com_ports(self):
        ports = [port.device for port in list_ports.comports()]
        self.com_port_combobox["values"] = ports
        if ports:
            self.com_port_combobox.current(0)

    def connect_to_port(self):
        port = self.com_port_combobox.get()
        self.serial_comm = SerialCommunication(self.response_text)
        if self.serial_comm.connect(port):
            self.connect_button["state"] = "disabled"
            self.com_port_combobox["state"] = "disabled"
            self.data_bits_combobox["state"] = "disabled"
            self.parity_combobox["state"] = "disabled"
            self.stop_bits_combobox["state"] = "disabled"
            self.disconnect_button["state"] = "normal"
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert(tk.END, "Connected to " + port)
        else:
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert(tk.END, "Failed to connect to " + port)

    def disconnect_from_port(self):
        if self.serial_comm:
            self.serial_comm.disconnect()
        self.connect_button["state"] = "normal"
        self.com_port_combobox["state"] = "readonly"
        self.data_bits_combobox["state"] = "readonly"
        self.parity_combobox["state"] = "readonly"
        self.stop_bits_combobox["state"] = "readonly"
        self.disconnect_button["state"] = "disabled"
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert(tk.END, "Disconnected")

    def send_command(self):
        if self.serial_comm:
            command = self.command_entry.get()
            self.serial_comm.send_command(command)
            time.sleep(0.1)  # Wait for response
            response = self.serial_comm.read_response()
            self.response_text.delete("1.0", tk.END)
                

if __name__ == "__main__":
    app = Application()
    app.mainloop()
