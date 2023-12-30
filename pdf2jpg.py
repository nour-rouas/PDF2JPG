import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QMessageBox
from pdf2image import convert_from_path

class PdfToJpgConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('PDF to JPG Converter')

        self.input_label = QLabel('Select PDF File:', self)
        self.input_label.setGeometry(20, 20, 150, 20)

        self.output_label = QLabel('Save as JPG File:', self)
        self.output_label.setGeometry(20, 60, 150, 20)

        self.input_path = ''
        self.output_path = ''

        self.input_button = QPushButton('Select PDF', self)
        self.input_button.setGeometry(180, 20, 150, 30)
        self.input_button.clicked.connect(self.showPdfDialog)

        self.output_button = QPushButton('Save as JPG', self)
        self.output_button.setGeometry(180, 60, 150, 30)
        self.output_button.clicked.connect(self.showSaveDialog)

        convert_button = QPushButton('Convert', self)
        convert_button.setGeometry(120, 100, 150, 30)
        convert_button.clicked.connect(self.convertPdfToJpg)

    def showPdfDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 'Select PDF File', '', 'PDF Files (*.pdf);;All Files (*)', options=options)
        if fileName:
            self.input_path = fileName
            self.input_label.setText(f'Selected PDF: {fileName}')

    def showSaveDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save as JPG', '', 'Image Files (*.jpg);;All Files (*)', options=options)
        if fileName:
            self.output_path = fileName
            self.output_label.setText(f'Save as JPG: {fileName}')

    def convertPdfToJpg(self):
        if not self.input_path or not self.output_path:
            return

        # Set the path to the Poppler binaries explicitly
        poppler_path = r'C:\poppler-23.11.0\Library\bin'
        images = convert_from_path(self.input_path, poppler_path=poppler_path)
        images[0].save(self.output_path, 'JPEG')

        self.input_label.setText('Select PDF File:')
        self.output_label.setText('Save as JPG File:')
        self.input_path = ''
        self.output_path = ''

        print('Conversion complete. Ready for more conversions.')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PdfToJpgConverter()
    ex.show()
    sys.exit(app.exec_())
