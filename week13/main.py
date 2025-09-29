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
                id_student TEXT PRIMARY KEY NOT NULL,
                first_name TEXT,
                last_name TEXT,
                major TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


class Studentfrom(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Studentfrom.ui", self)

        init_db()

        # เชื่อมปุ่ม
        self.pushButton.clicked.connect(self.saveData)            # ปุ่ม บันทึก
        self.pushButton_update.clicked.connect(self.updateData)   # ปุ่ม แก้ไข
        self.pushButton_delete.clicked.connect(self.deleteData)   # ปุ่ม ลบ
        self.tableWidget.cellClicked.connect(self.fillFieldsFromTable)

        self.loadData()

    def saveData(self):
        student_ID = self.textEdit.text().strip()
        first_name = self.textEdit_2.text().strip()
        last_name = self.textEdit_3.text().strip()
        major = self.textEdit_4.text().strip()

        if not all([student_ID, first_name, last_name, major]):
            QMessageBox.warning(self, "ข้อมูลไม่ถูกต้อง", "กรุณากรอกข้อมูลให้ครบ")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO profile(id_student, first_name, last_name, major) VALUES(?,?,?,?)",
                (student_ID, first_name, last_name, major)
            )
            conn.commit()
            QMessageBox.information(self, "สำเร็จ", "บันทึกข้อมูลเรียบร้อยแล้ว")
            self.loadData()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "ซ้ำ", "รหัสนักศึกษานี้มีอยู่แล้ว")
        except Exception as e:
            QMessageBox.critical(self, "ผิดพลาด", f"เกิดข้อผิดพลาด\n{e}")
        finally:
            conn.close()

    def loadData(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM profile")
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "ล้มเหลว", f"โหลดข้อมูลล้มเหลว\n{e}")
            return
        finally:
            conn.close()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["รหัส", "ชื่อ", "นามสกุล", "สาขาวิชา"])

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.tableWidget.setItem(r, c, QTableWidgetItem(str(val)))

        self.tableWidget.resizeColumnsToContents()

    def fillFieldsFromTable(self, row, column):
        # เมื่อคลิกแถว → ดึงข้อมูลจากแถวนั้น มาใส่ในช่องกรอก
        self.textEdit.setText(self.tableWidget.item(row, 0).text())
        self.textEdit_2.setText(self.tableWidget.item(row, 1).text())
        self.textEdit_3.setText(self.tableWidget.item(row, 2).text())
        self.textEdit_4.setText(self.tableWidget.item(row, 3).text())

    def updateData(self):
        student_ID = self.textEdit.text().strip()
        first_name = self.textEdit_2.text().strip()
        last_name = self.textEdit_3.text().strip()
        major = self.textEdit_4.text().strip()

        if not all([student_ID, first_name, last_name, major]):
            QMessageBox.warning(self, "ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลให้ครบ")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE profile
                SET first_name = ?, last_name = ?, major = ?
                WHERE id_student = ?
                """,
                (first_name, last_name, major, student_ID)
            )
            conn.commit()

            if cur.rowcount == 0:
                QMessageBox.warning(self, "ไม่พบข้อมูล", "ไม่พบรหัสนักศึกษานี้ในระบบ")
            else:
                QMessageBox.information(self, "สำเร็จ", "อัปเดตข้อมูลเรียบร้อยแล้ว")
                self.loadData()

        except Exception as e:
            QMessageBox.critical(self, "ผิดพลาด", f"อัปเดตข้อมูลล้มเหลว\n{e}")
        finally:
            conn.close()

    def deleteData(self):
        student_ID = self.textEdit.text().strip()
        if not student_ID:
            QMessageBox.warning(self, "กรุณาเลือกข้อมูล", "กรุณาเลือกข้อมูลจากตารางก่อนลบ")
            return

        confirm = QMessageBox.question(
            self,
            "ยืนยันการลบ",
            f"คุณต้องการลบรหัสนักศึกษา '{student_ID}' หรือไม่?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("DELETE FROM profile WHERE id_student = ?", (student_ID,))
            conn.commit()

            if cur.rowcount == 0:
                QMessageBox.warning(self, "ไม่พบข้อมูล", "ไม่พบรหัสนักศึกษานี้")
            else:
                QMessageBox.information(self, "สำเร็จ", "ลบข้อมูลเรียบร้อยแล้ว")
                self.loadData()

        except Exception as e:
            QMessageBox.critical(self, "ผิดพลาด", f"ลบข้อมูลล้มเหลว\n{e}")
        finally:
            conn.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Studentfrom()
    window.show()
    sys.exit(app.exec_())
