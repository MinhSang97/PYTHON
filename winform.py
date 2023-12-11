import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QLineEdit, QPushButton, QTextBrowser

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ứng dụng WinForms với kết nối MSSQL")
        self.setGeometry(100, 100, 600, 400)  # Thiết lập kích thước cửa sổ

        self.label = QLabel("Nhập câu truy vấn:", self)
        self.label.move(20, 20)

        self.query_input = QLineEdit(self)
        self.query_input.setGeometry(20, 40, 400, 30)

        self.query_button = QPushButton("Truy vấn", self)
        self.query_button.setGeometry(430, 40, 80, 30)
        self.query_button.clicked.connect(self.execute_query)

        self.result_display = QTextBrowser(self)
        self.result_display.setGeometry(20, 80, 560, 300)

    def execute_query(self):
        query = self.query_input.text()

        # Kết nối với cơ sở dữ liệu MSSQL
        connection_string = "DRIVER={SQL Server};SERVER=192.168.40.253;DATABASE=SPC;UID=amr;PWD=123456"
        connection = pyodbc.connect(connection_string)

        try:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            # Hiển thị kết quả truy vấn lên QTextBrowser
            result_text = ""
            for row in rows:
                result_text += str(row) + "\n"
            self.result_display.setText(result_text)
        except Exception as e:
            self.result_display.setText("Lỗi truy vấn: " + str(e))

        connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
