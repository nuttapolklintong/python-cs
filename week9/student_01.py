import os
from pathlib import Path

class TXT:
    def Created():
        text_data = """ Hello Nuttapol Klintong """
        with open("student.txt", "w", encoding="utf-8") as file:
                file.write(text_data)
                try:
                        print("บันทึกไฟล์เรียบร้อยแล้ว")
                except:
                        print("บันทึกล้มเหลว")
    def Reader():
      with open ("student.txt", "r", encoding="utf-8") as file:
            try:
                print(file.read())
            except:
                print("อ่านไฟล์ไม่ได้")
    def updated(data_update):
        with open("student.txt", "w", encoding="utf-8") as file:
            try:
                 file.write(data_update)
                 print("อัพเดทข้อมูลเสร็จสิ้น")
            except:
                 print("ไม่สามารถอัพเดทข้อมูลได้")
    def Del(fileName):
        file = fileName
        if(os.path.exists(file)):
            os.remove(file)
        else:
            print("ไม่พบ", file)

status = True
while True:
     print("------ Menu ------")
     print("Q=Quit, C=Create, R=Read, U=Update, D=Delete")
     print("------ Menu ------")
     status = input("Select the menu : ")
     if(status.lower() == "q"):
          break
     elif(status.lower() == "c"):
          TXT.Created()
     elif(status.lower() == "r"):
          TXT.Reader()
     elif(status.lower() == "u"):
          inp = input("Data Update : ")
          TXT.updated(inp)
     elif(status.lower() == "d"):
          TXT.Del("student.txt")





#create = TXT.Created()
#read = TXT.Reader()
#up_to_dated = TXT.updated("Test")
#read = TXT.Reader()
#delete = TXT.Del("student.txt")