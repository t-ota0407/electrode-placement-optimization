from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar

class AsyncTransactionProgressWindow(QDialog):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Processing')
        self.setGeometry(400, 400, 300, 100)

        self.layout = QVBoxLayout()

        self.label = QLabel('Now processing...')
        self.layout.addWidget(self.label)

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 0)
        self.layout.addWidget(self.progressBar)

        self.setLayout(self.layout)
    
    def finishProcessing(self):
        self.label.setText('Processing finished!')
