from PyQt5.QtCore import QThread, pyqtSignal

class AsyncTransactionWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, transaction, parent=None):
        super().__init__(parent)
        self.transation = transaction
    
    def run(self):

        self.transation()
        
        self.finished.emit()