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
        cur.execute(
            """
                    CREATE TABLE IF NOT EXISTS profile(
                    id_student BLOB PRIAMRY KEY NOT NULL,
                    first_name BLOB,
                    last_name BLOB,
                    major BLOB)"""
        )
        conn.commit()
    finally:
        conn.close()


class Studentfrom(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Studentfrom.ui", self)

        init_db()

        self.pushButton.clicked.connect(self.saveData)
        self.loadData()

    def saveData(self):
        student_ID = self.textEdit.text()
        first_name = self.textEdit_2.text()
        last_name = self.textEdit_3.text()
        major = self.textEdit_4.text()

        if not all([student_ID, first_name, last_name, major]):
            QMessageBox.warning(self, "ข้อมูลไม่ถูกต้อง", "กรุณาลองใหม่")
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO profile(id_student, first_name, last_name, major) VALUES(?,?,?,?) ",
                (student_ID, first_name, last_name, major),
            )
            conn.commit()
        except Exception as e:
            QMessageBox.critical(self, "บันทึกข้อมูล ล้มเหลว", f"เกิดข้อผิดพลาด\n{e}")
            return
        finally:
            conn.close()

        QMessageBox.information(self, "บันทึกข้อมูลสำเร็จ", "บันทึกเรียบร้อย")

    def loadData(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM profile")
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "Failed", f"You failed\n{e}")
            return
        finally:
            conn.close()

        # กำหนดแถว
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["รหัส", "ชื่อ", "นามสกุล", "สาขาวิชา"])

        # load ข้อมูลทีละแถว
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.tableWidget.setItem(r, c, QTableWidgetItem(str(val)))

        self.tableWidget.resizeColumnsToContents()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Studentfrom()
    window.show()
    sys.exit(app.exec_())
