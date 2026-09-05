import tkinter as tk
from tkinter import messagebox as msg 
import sqlite3
from Entry import user_interface 

class user:
    def __init__(self):
        self.connection = sqlite3.connect("StoreRoom.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT,
                    lastName TEXT,
                    phoneNumber TEXT,
                    password TEXT,
                    address TEXT,
                    userName TEXT, 
                    role TINYINT
                )
                """)
        self.connection.commit()
        # ربر پیش فر ض اضافه شودباید یک کبا
        self.cursor.execute("""
        SELECT COUNT(*) AS number_of_user_entry FROM users 
        """)
        number_of_user_entry=self.cursor.fetchone()[0]
        # اولین نتیجه ای که پیدا کردی را برگردان
        if number_of_user_entry==0:
        # در واقع این کد میگه فقط برای اولین بار برو و این کاربر از پیش تعریف اضافه کن 
        # بنابراین اگر کاربری اضافه نشده باشد این اضافه می شود و اگر اضافه شده بود دیگر این کاربر اضافه نمی ش.د 
            Name='Tina'
            last_name='Lee'
            phone='09149838328'
            password='ti13na89'
            address='Iran-Boukan'
            userName='TinLee'
            role=1
            query=(Name, last_name, phone, password, address , userName , role)
            self.cursor.execute("""
            INSERT INTO users(Name, lastName, phoneNumber, password, address , userName , role)
            VALUES (?, ?, ?, ?, ? ,? ,?)
            """,(query))
            
            self.connection.commit()
    def login(self):
        username = self.userName.get()
        password = self.password.get()

        self.cursor.execute("""
            SELECT * FROM users
            WHERE userName = ? AND password = ? AND role=?
        """, (username, password , 1))

        result = self.cursor.fetchone()
        # اولین چیزی را که پیدا کردی به من بده 

        if result:
            # باز کردن صفحه اصلی
            user_interface(self.win)

        else:
            msg.showerror("خطا", "نام کاربری یا پسورد اشتباه است.")
        
    def tkinterLogin(self):       
        self.win=tk.Tk()
        self.win.title("ورود به نرم افزار")
        self.win.geometry("500x300")
        
        tk.Label(self.win , text="پسورد:").grid(row=4, column=1)
        self.password = tk.Entry(self.win , show='*')
        self.password.grid(row=4, column=0, padx=5, pady=5)

        tk.Label(self.win , text="نام کاربری:").grid(row=6, column=1)
        self.userName = tk.Entry(self.win)
        self.userName.grid(row=6, column=0, padx=5, pady=5)

        btn=tk.Button(self.win , text="بررسی" , command=self.login)
        btn.grid(row=7, column=1)

        self.win.mainloop()
userPatern=user()
userPatern.tkinterLogin()










