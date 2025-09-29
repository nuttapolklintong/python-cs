import sys
import sqlite3
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem

DB_PATH = os.path.join(os.path.dirname(__file__), "asset.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS asset(
                code TEXT PRIMARY KEY NOT NULL,
                student_id TEXT,
                name TEXT,
                detail TEXT,
                room TEXT,
                location TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


class AssetForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ex01.ui", self)

        init_db()

        # เชื่อมปุ่ม
        self.pushButton_save.clicked.connect(self.saveData)
        self.pushButton_update.clicked.connect(self.updateData)
        self.pushButton_delete.clicked.connect(self.deleteData)
        self.tableWidget.cellClicked.connect(self.fillFieldsFromTable)

        self.loadData()

    def saveData(self):
        code = self.textEdit.text().strip()
        student_id = self.textEdit_2.text().strip()
        name = self.textEdit_3.text().strip()
        detail = self.textEdit_4.text().strip()
        room = self.textEdit_5.text().strip()
        location = self.textEdit_6.text().strip()

        if not all([code, student_id, name]):
            QMessageBox.warning(self, "ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลให้ครบ")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO asset(code, student_id, name, detail, room, location) VALUES(?,?,?,?,?,?)",
                (code, student_id, name, detail, room, location)
            )
            conn.commit()
            QMessageBox.information(self, "สำเร็จ", "บันทึกข้อมูลเรียบร้อยแล้ว")
            self.loadData()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "ซ้ำ", "รหัสนี้มีอยู่แล้ว")
        except Exception as e:
            QMessageBox.critical(self, "ผิดพลาด", f"เกิดข้อผิดพลาด\n{e}")
        finally:
            conn.close()

    def loadData(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM asset")
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "ล้มเหลว", f"โหลดข้อมูลล้มเหลว\n{e}")
            return
        finally:
            conn.close()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels([
            "รหัส", "รหัสนักศึกษา", "ชื่อ", "รายละเอียด", "ห้อง", "พิกัด"
        ])

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.tableWidget.setItem(r, c, QTableWidgetItem(str(val)))

        self.tableWidget.resizeColumnsToContents()

    def fillFieldsFromTable(self, row, column):
        self.textEdit.setText(self.tableWidget.item(row, 0).text())
        self.textEdit_2.setText(self.tableWidget.item(row, 1).text())
        self.textEdit_3.setText(self.tableWidget.item(row, 2).text())
        self.textEdit_4.setText(self.tableWidget.item(row, 3).text())
        self.textEdit_5.setText(self.tableWidget.item(row, 4).text())
        self.textEdit_6.setText(self.tableWidget.item(row, 5).text())

    def updateData(self):
        code = self.textEdit.text().strip()
        student_id = self.textEdit_2.text().strip()
        name = self.textEdit_3.text().strip()
        detail = self.textEdit_4.text().strip()
        room = self.textEdit_5.text().strip()
        location = self.textEdit_6.text().strip()

        if not all([code, student_id, name]):
            QMessageBox.warning(self, "ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลให้ครบ")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE asset
                SET student_id = ?, name = ?, detail = ?, room = ?, location = ?
                WHERE code = ?
                """,
                (student_id, name, detail, room, location, code)
            )
            conn.commit()

            if cur.rowcount == 0:
                QMessageBox.warning(self, "ไม่พบข้อมูล", "ไม่พบรหัสนี้ในระบบ")
            else:
                QMessageBox.information(self, "สำเร็จ", "อัปเดตข้อมูลเรียบร้อยแล้ว")
                self.loadData()

        except Exception as e:
            QMessageBox.critical(self, "ผิดพลาด", f"อัปเดตข้อมูลล้มเหลว\n{e}")
        finally:
            conn.close()

    def deleteData(self):
        code = self.textEdit.text().strip()
        if not code:
            QMessageBox.warning(self, "กรุณาเลือกข้อมูล", "กรุณาเลือกข้อมูลจากตารางก่อนลบ")
            return

        confirm = QMessageBox.question(
            self,
            "ยืนยันการลบ",
            f"คุณต้องการลบรหัส '{code}' หรือไม่?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("DELETE FROM asset WHERE code = ?", (code,))
            conn.commit()

            if cur.rowcount == 0:
                QMessageBox.warning(self, "ไม่พบข้อมูล", "ไม่พบรหัสนี้")
            else:
                QMessageBox.information(self, "สำเร็จ", "ลบข้อมูลเรียบร้อยแล้ว")
                self.loadData()

        except Exception as e:
            QMessageBox.critical(self, "ผิดพลาด", f"ลบข้อมูลล้มเหลว\n{e}")
        finally:
            conn.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AssetForm()
    window.show()
    sys.exit(app.exec_())
