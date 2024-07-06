import sys
import re
import PyPDF2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QTextEdit, QMessageBox

class PDFWebsiteFinder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Website Finder")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.text_area = QTextEdit()
        layout.addWidget(self.text_area)

        self.find_button = QPushButton("Find Websites")
        self.find_button.clicked.connect(self.find_websites)
        layout.addWidget(self.find_button)

        self.open_button = QPushButton("Open PDF")
        self.open_button.clicked.connect(self.open_pdf)
        layout.addWidget(self.open_button)

        self.copy_button = QPushButton("Copy Links")
        self.copy_button.clicked.connect(self.copy_links)
        layout.addWidget(self.copy_button)

        self.website_label = QLabel()
        layout.addWidget(self.website_label)

    def open_pdf(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        filename, _ = file_dialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if filename:
            with open(filename, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()
                self.text_area.setPlainText(text)

    def find_websites(self):
        text = self.text_area.toPlainText()
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        if urls:
            websites = ", ".join(urls)
            self.website_label.setText(f"Websites found: {websites}")
        else:
            self.website_label.setText("No websites found in the PDF.")

    def copy_links(self):
        text = self.website_label.text()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "Copied", "Links copied to clipboard.")
        else:
            QMessageBox.warning(self, "No Links", "No links to copy.")

def main():
    app = QApplication(sys.argv)
    window = PDFWebsiteFinder()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
