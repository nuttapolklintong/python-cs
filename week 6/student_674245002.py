import tkinter as tk
from tkinter import messagebox
from collections import deque

class BookingNode:
    def __init__(self, time, user):
        self.time = time
        self.user = user
        self.left = None
        self.right = None

class BookingTree:
    def __init__(self):
        self.root = None

    def insert(self, time, user):
        if not self.root:
            self.root = BookingNode(time, user)
        else:
            self._insert(self.root, time, user)

    def _insert(self, node, time, user):
        if time < node.time:
            if node.left is None:
                node.left = BookingNode(time, user)
            else:
                self._insert(node.left, time, user)
        elif time > node.time:
            if node.right is None:
                node.right = BookingNode(time, user)
            else:
                self._insert(node.right, time, user)

    def is_available(self, time):
        return self._search(self.root, time) is None

    def _search(self, node, time):
        if not node:
            return None
        if node.time == time:
            return node
        elif time < node.time:
            return self._search(node.left, time)
        else:
            return self._search(node.right, time)

    def get_bookings(self):
        bookings = []
        self._inorder(self.root, bookings)
        return bookings

    def _inorder(self, node, bookings):
        if node:
            self._inorder(node.left, bookings)
            bookings.append((node.time, node.user))
            self._inorder(node.right, bookings)


class RoomBookingSystem:
    def __init__(self):
        self.rooms = {}
        self.waiting_queue = deque()

    def add_room(self, room_name):
        if room_name not in self.rooms:
            self.rooms[room_name] = BookingTree()
            return True
        return False

    def book_room(self, room_name, time, user):
        if room_name not in self.rooms:
            return "ไม่มีห้องนี้ในระบบ"

        tree = self.rooms[room_name]
        if tree.is_available(time):
            tree.insert(time, user)
            return f"{user} จองห้อง '{room_name}' เวลา {time} สำเร็จ"
        else:
            self.waiting_queue.append((room_name, time, user))
            return f"ห้อง '{room_name}' เวลา {time} ไม่ว่าง — เพิ่มเข้าในคิวรอ"

    def check_available(self, room_name, time):
        if room_name not in self.rooms:
            return "ไม่มีห้องนี้ในระบบ"
        return "ว่าง" if self.rooms[room_name].is_available(time) else "ไม่ว่าง"

    def process_queue(self):
        processed = []
        for _ in range(len(self.waiting_queue)):
            room_name, time, user = self.waiting_queue.popleft()
            if self.rooms[room_name].is_available(time):
                self.rooms[room_name].insert(time, user)
                processed.append(f"{user} ได้จองห้อง '{room_name}' เวลา {time} (จากคิวรอ)")
            else:
                self.waiting_queue.append((room_name, time, user))
        return processed

    def get_status(self):
        info = []
        for room, tree in self.rooms.items():
            bookings = tree.get_bookings()
            if bookings:
                btext = ", ".join([f"{t}:{u}" for t, u in bookings])
                info.append(f"{room}: {btext}")
            else:
                info.append(f"{room}: (ยังไม่มีการจอง)")
        return info


class BookingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ระบบจัดการการจองห้องเรียน / ห้องซ้อม")
        self.master.geometry("620x600")
        self.system = RoomBookingSystem()

        tk.Label(master, text="ชื่อห้อง:", font=("Tahoma", 10)).pack()
        self.room_entry = tk.Entry(master, width=30)
        self.room_entry.pack()

        tk.Button(master, text="เพิ่มห้อง", command=self.add_room, bg="#d0f0c0").pack(pady=5)

        tk.Label(master, text="ชื่อผู้จอง:", font=("Tahoma", 10)).pack()
        self.user_entry = tk.Entry(master, width=30)
        self.user_entry.pack()

        tk.Label(master, text="เวลาที่ต้องการจอง (ตัวเลขชั่วโมง เช่น 10):", font=("Tahoma", 10)).pack()
        self.time_entry = tk.Entry(master, width=30)
        self.time_entry.pack()

        tk.Button(master, text="จองห้อง", command=self.book_room, bg="#a8e6cf").pack(pady=5)
        tk.Button(master, text="ตรวจสอบห้องว่าง", command=self.check_room, bg="#ffd3b6").pack(pady=5)
        tk.Button(master, text="ประมวลผลคิวรอ", command=self.process_queue, bg="#ffaaa5").pack(pady=5)
        tk.Button(master, text="ดูสถานะทั้งหมด", command=self.show_status, bg="#dcedc1").pack(pady=5)

        self.output_box = tk.Text(master, height=18, width=75, font=("Consolas", 10))
        self.output_box.pack(pady=10)

    def add_room(self):
        room = self.room_entry.get().strip()
        if not room:
            messagebox.showerror("Error", "กรุณากรอกชื่อห้อง")
            return
        if self.system.add_room(room):
            self.log(f"เพิ่มห้อง '{room}' สำเร็จ")
        else:
            self.log(f"ห้อง '{room}' มีอยู่แล้ว")

    def book_room(self):
        room = self.room_entry.get().strip()
        user = self.user_entry.get().strip()
        time_str = self.time_entry.get().strip()

        if not room or not user or not time_str:
            messagebox.showerror("Error", "กรุณากรอกข้อมูลให้ครบ")
            return
        try:
            time = int(time_str)
        except ValueError:
            messagebox.showerror("Error", "เวลา ต้องเป็นตัวเลขชั่วโมง เช่น 10")
            return

        msg = self.system.book_room(room, time, user)
        self.log(msg)

    def check_room(self):
        room = self.room_entry.get().strip()
        time_str = self.time_entry.get().strip()
        if not room or not time_str:
            messagebox.showerror("Error", "กรุณากรอกชื่อห้องและเวลา")
            return
        try:
            time = int(time_str)
        except ValueError:
            messagebox.showerror("Error", "เวลา ต้องเป็นตัวเลข")
            return
        msg = self.system.check_available(room, time)
        self.log(f"{room} เวลา {time}: {msg}")

    def process_queue(self):
        results = self.system.process_queue()
        if results:
            for msg in results:
                self.log(msg)
        else:
            self.log("ไม่มีรายการในคิวรอ")

    def show_status(self):
        self.log("\n=== สถานะห้องทั้งหมด ===")
        for info in self.system.get_status():
            self.log(info)
        if self.system.waiting_queue:
            self.log("\nคิวรอ:")
            for item in list(self.system.waiting_queue):
                self.log(f"   {item}")
        else:
            self.log("\nไม่มีคิวรอ")

    def log(self, text):
        self.output_box.insert(tk.END, text + "\n")
        self.output_box.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = BookingApp(root)
    root.mainloop()
