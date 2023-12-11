using System;
using System.Data;
using System.Data.SqlClient;
using System.Windows.Forms;
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;

namespace WinFormApp
{
    public partial class MainForm : Form
    {
        private SqlConnection connection;

        public MainForm()
        {
            InitializeComponent();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            // Thiết lập các giá trị mặc định cho kết nối
            serverTextBox.Text = "Tên Server";
            databaseTextBox.Text = "Tên Database";
            userTextBox.Text = "Tên User";
            passwordTextBox.Text = "Mật khẩu";
        }

        private void connectButton_Click(object sender, EventArgs e)
        {
            // Kiểm tra các giá trị nhập vào
            if (string.IsNullOrEmpty(serverTextBox.Text) ||
                string.IsNullOrEmpty(databaseTextBox.Text) ||
                string.IsNullOrEmpty(userTextBox.Text) ||
                string.IsNullOrEmpty(passwordTextBox.Text))
            {
                MessageBox.Show("Vui lòng nhập đầy đủ thông tin kết nối.", "Lỗi",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Thiết lập chuỗi kết nối
            string connectionString = $"Data Source={serverTextBox.Text};" +
                $"Initial Catalog={databaseTextBox.Text};" +
                $"User ID={userTextBox.Text};" +
                $"Password={passwordTextBox.Text}";

            try
            {
                // Kết nối tới cơ sở dữ liệu
                connection = new SqlConnection(connectionString);
                connection.Open();
                MessageBox.Show("Kết nối thành công đến cơ sở dữ liệu.", "Thông báo",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Lỗi kết nối đến cơ sở dữ liệu: " + ex.Message, "Lỗi",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void executeButton_Click(object sender, EventArgs e)
        {
            // Kiểm tra kết nối cơ sở dữ liệu
            if (connection == null || connection.State != ConnectionState.Open)
            {
                MessageBox.Show("Vui lòng kết nối đến cơ sở dữ liệu trước khi thực hiện truy vấn.", "Lỗi",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Kiểm tra câu truy vấn
            if (string.IsNullOrEmpty(queryTextBox.Text))
            {
                MessageBox.Show("Vui lòng nhập câu truy vấn.", "Lỗi",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            try
            {
                // Thực hiện truy vấn
                SqlCommand command = new SqlCommand(queryTextBox.Text, connection);
                SqlDataAdapter adapter = new SqlDataAdapter(command);
                DataTable dataTable = new DataTable();
                adapter.Fill(dataTable);

                // Hiển thị kết quả
                resultDataGridView.DataSource = dataTable;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Lỗi thực hiện truy vấn: " + ex.Message, "Lỗi",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void exportButton_Click(object sender, EventArgs e)
        {
            // Kiểm tra kết nối cơ sở dữ liệu
            if (connection == null || connection.State != ConnectionState.Open)
            {
                MessageBox.Show("Vui lòng kết nối đến cơ sở dữ liệu trước khi xuất dữ liệu.", "Lỗi",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Kiểm tra dữ liệu hiển thị
            if (resultDataGridView.DataSource == null)
            {
                MessageBox.Show("Không có dữ liệu để xuất.", "Lỗi",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Chọn vị trí lưu file Excel
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.Filter = "Excel Files (*.xlsx)|*.xlsx";
            saveFileDialog.Title = "Lưu File Excel";
            if (saveFileDialog.ShowDialog() != DialogResult.OK)
                return;

            try
            {
                // Tạo file Excel mới
                using (SpreadsheetDocument spreadsheetDocument = SpreadsheetDocument.Create(saveFileDialog.FileName, SpreadsheetDocumentType.Workbook))
                {
                    // Tạo một Workbook mới
                    WorkbookPart workbookPart = spreadsheetDocument.AddWorkbookPart();
                    workbookPart.Workbook = new Workbook();

                    // Tạo một Worksheet mới
                    WorksheetPart worksheetPart = workbookPart.AddNewPart<WorksheetPart>();
                    worksheetPart.Worksheet = new Worksheet(new SheetData());

                    // Thêm Worksheet vào Workbook
                    Sheets sheets = spreadsheetDocument.WorkbookPart.Workbook.AppendChild<Sheets>(new Sheets());
                    Sheet sheet = new Sheet() { Id = spreadsheetDocument.WorkbookPart.GetIdOfPart(worksheetPart), SheetId = 1, Name = "Sheet1" };
                    sheets.Append(sheet);

                    // Lấy dữ liệu từ DataGridView
                    DataTable dataTable = (DataTable)resultDataGridView.DataSource;

                    // Thêm dữ liệu vào Worksheet
                    SheetData sheetData = worksheetPart.Worksheet.GetFirstChild<SheetData>();
                    uint rowIndex = 1;
                    foreach (DataRow row in dataTable.Rows)
                    {
                        Row newRow = new Row() { RowIndex = rowIndex++ };
                        foreach (var item in row.ItemArray)
                        {
                            Cell cell = new Cell();
                            cell.DataType = CellValues.String;
                            cell.CellValue = new CellValue(item.ToString());
                            newRow.AppendChild(cell);
                        }
                        sheetData.AppendChild(newRow);
                    }

                    // Lưu Workbook
                    workbookPart.Workbook.Save();

                    MessageBox.Show("Xuất dữ liệu thành công.", "Thông báo",
                        MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Lỗi xuất dữ liệu: " + ex.Message, "Lỗi",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
