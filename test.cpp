#include <QtWidgets>
#include <QtSql>
#include <QXlsx/QtXlsx>
#include <QMessageBox>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr)
        : QMainWindow(parent)
    {
        // Tạo các widget
        userLabel = new QLabel("Username:");
        userLineEdit = new QLineEdit;
        passwordLabel = new QLabel("Password:");
        passwordLineEdit = new QLineEdit;
        passwordLineEdit->setEchoMode(QLineEdit::Password);
        dbLabel = new QLabel("Database:");
        dbLineEdit = new QLineEdit;
        serverLabel = new QLabel("Server:");
        serverLineEdit = new QLineEdit;
        queryLabel = new QLabel("Query:");
        queryTextEdit = new QTextEdit;
        executeButton = new QPushButton("Execute");
        exportButton = new QPushButton("Export to Excel");

        // Tạo layout
        QFormLayout *formLayout = new QFormLayout;
        formLayout->addRow(userLabel, userLineEdit);
        formLayout->addRow(passwordLabel, passwordLineEdit);
        formLayout->addRow(dbLabel, dbLineEdit);
        formLayout->addRow(serverLabel, serverLineEdit);
        formLayout->addRow(queryLabel, queryTextEdit);
        QVBoxLayout *mainLayout = new QVBoxLayout;
        mainLayout->addLayout(formLayout);
        mainLayout->addWidget(executeButton);
        mainLayout->addWidget(exportButton);

        // Tạo widget chính
        QWidget *mainWidget = new QWidget;
        mainWidget->setLayout(mainLayout);
        setCentralWidget(mainWidget);

        // Kết nối các sự kiện
        connect(executeButton, SIGNAL(clicked()), this, SLOT(executeQuery()));
        connect(exportButton, SIGNAL(clicked()), this, SLOT(exportToExcel()));

        // Kết nối cơ sở dữ liệu
        db = QSqlDatabase::addDatabase("QODBC");
        QString connectionTemplate = "DRIVER={SQL Server};SERVER=%1;DATABASE=%2;UID=%3;PWD=%4";
        QString connectionStr = connectionTemplate.arg(serverLineEdit->text())
                                                  .arg(dbLineEdit->text())
                                                  .arg(userLineEdit->text())
                                                  .arg(passwordLineEdit->text());
        db.setDatabaseName(connectionStr);
        if (!db.open()) {
            QMessageBox::critical(this, "Error", "Could not connect to database.");
        }
    }

public slots:
    void executeQuery()
    {
        QSqlQuery query;
        QString queryString = queryTextEdit->toPlainText();
        if (!query.exec(queryString)) {
            QMessageBox::critical(this, "Error", "Query execution failed.");
            return;
        }

        // Xóa kết quả trước đó
        while (query.next()) {
            query.clear();
        }

        // Lấy dữ liệu truy vấn
        QXlsx::Document xlsx;
        QSqlRecord record = query.record();
        int columnCount = record.count();
        QStringList headers;
        for (int i = 0; i < columnCount; ++i) {
            headers << record.fieldName(i);
        }
        xlsx.writeRow("Sheet1", 1, headers);
        int row = 2;
        while (query.next()) {
            QStringList rowData;
            for (int i = 0; i < columnCount; ++i) {
                rowData << query.value(i).toString();
            }
            xlsx.writeRow("Sheet1", row, rowData);
            ++row;
        }

        // Lưu kết quả thành file Excel
        QString fileName = QFileDialog::getSaveFileName(this, "Save Excel File", "", "Excel Files (*.xlsx)");
        if (!fileName.isEmpty()) {
            xlsx.saveAs(fileName);
        }
    }

    void exportToExcel()
    {
        // Thực hiện truy vấn và xuất kết quả thành file Excel
        executeQuery();
    }

private:
    QLabel *userLabel;
    QLineEdit *userLineEdit;
    QLabel *passwordLabel;
    QLineEdit *passwordLineEdit;
    QLabel *dbLabel;
    QLineEdit *dbLineEdit;
    QLabel *serverLabel;
    QLineEdit *serverLineEdit;
    QLabel *queryLabel;
    QTextEdit *queryTextEdit;
    QPushButton *executeButton;
    QPushButton *exportButton;

    QSqlDatabase db;
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    MainWindow window;
    window.show();

    return app.exec();
}

#include "main.moc"
