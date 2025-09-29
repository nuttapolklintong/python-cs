import sys
import sqlite3
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem

DB_PATH = os.path.join(os.path.dirname(__file__), "student.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                id_student TEXT PRIMARY KEY NOT NULL,
                first_name TEXT,
                last_name TEXT,
                major TEXT
            )
        """)
        conn.commit()
    finally:
        conn.close()

class StudentForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Studentfrom.ui", self)

        init_db()

        self.pushButton.clicked.connect(self.saveData)
        self.pushButton_delete.clicked.connect(self.deleteData)
        self.pushButton_update.clicked.connect(self.updateData)
        self.tableWidget.cellClicked.connect(self.loadSelectedRow)

        self.loadData()

    def showMessage(self, title, message, icon=QMessageBox.Information):
        QMessageBox(icon, title, message, QMessageBox.Ok, self).exec_()

    def saveData(self):
        id_student = self.textEdit.text().strip()
        first_name = self.textEdit_2.text().strip()
        last_name = self.textEdit_3.text().strip()
        major = self.textEdit_4.text().strip()

        if not all([id_student, first_name, last_name, major]):
            self.showMessage("กรอกข้อมูลไม่ครบ", "กรุณากรอกข้อมูลให้ครบ", QMessageBox.Warning)
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("INSERT INTO profile VALUES (?, ?, ?, ?)", (id_student, first_name, last_name, major))
            conn.commit()
            self.showMessage("สำเร็จ", "บันทึกข้อมูลเรียบร้อยแล้ว")
            self.loadData()
        except sqlite3.IntegrityError:
            self.showMessage("ผิดพลาด", "รหัสนักศึกษาซ้ำ", QMessageBox.Critical)
        finally:
            conn.close()

    def loadData(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM profile")
        rows = cur.fetchall()
        conn.close()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["รหัส", "ชื่อ", "นามสกุล", "สาขา"])

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.tableWidget.setItem(r, c, QTableWidgetItem(str(val)))

    def loadSelectedRow(self, row, col):
        self.linecode.setText(self.tableWidget.item(row, 0).text())
        self.lineEdit.setText(self.tableWidget.item(row, 0).text())
        self.lineEdit_2.setText(self.tableWidget.item(row, 1).text())
        self.lineEdit_3.setText(self.tableWidget.item(row, 2).text())
        self.lineEdit_4.setText(self.tableWidget.item(row, 3).text())

    def deleteData(self):
        id_student = self.linecode.text().strip()
        if not id_student:
            self.showMessage("ผิดพลาด", "กรุณาเลือกรายการจากตาราง", QMessageBox.Warning)
            return

        reply = QMessageBox.question(self, "ยืนยัน", f"ต้องการลบรหัส {id_student} ใช่หรือไม่?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM profile WHERE id_student = ?", (id_student,))
        conn.commit()
        conn.close()
        self.showMessage("สำเร็จ", "ลบข้อมูลเรียบร้อยแล้ว")
        self.loadData()

    def updateData(self):
        code = self.linecode.text().strip()
        id_student = self.lineEdit.text().strip()
        first_name = self.lineEdit_2.text().strip()
        last_name = self.lineEdit_3.text().strip()
        major = self.lineEdit_4.text().strip()

        if not code:
            self.showMessage("ผิดพลาด", "กรุณาเลือกรายการจากตาราง", QMessageBox.Warning)
            return

        if not all([id_student, first_name, last_name, major]):
            self.showMessage("ผิดพลาด", "กรุณากรอกข้อมูลให้ครบ", QMessageBox.Warning)
            return

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "UPDATE profile SET id_student = ?, first_name = ?, last_name = ?, major = ? WHERE id_student = ?",
            (id_student, first_name, last_name, major, code)
        )
        conn.commit()
        conn.close()
        self.showMessage("สำเร็จ", "อัปเดตข้อมูลเรียบร้อยแล้ว")
        self.loadData()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StudentForm()
    window.show()
    sys.exit(app.exec_())
