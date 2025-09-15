import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

class Studentfrom(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("student_form.ui", self)


        self.pushButton.clicked.connect(self.saveData)
    
    def saveData(self):
        student_ID = self.lineEdit.text()
        first_name = self.lineEdit_2.text()
        last_name  = self.lineEdit_3.text()
        major      = self.lineEdit_4.text()

        # QMessageBox.information(
        #     self ,
        #     "ข้อมูลนักศึกษา" ,
        #     f"รหัสนักศึกษา : {student_ID}\n"
        #     f"ชื่อ : {first_name}\n"
        #     f"นามสกุล : {last_name}\n"
        #     f"สาขาวิชา : {major}\n"
        # )



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Studentfrom()
    window.show()
    sys.exit(app.exec_())