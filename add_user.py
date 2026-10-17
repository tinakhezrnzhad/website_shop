import tkinter as tk
from tkinter import messagebox as msg 
import sqlite3
from tkinter import ttk

class users:
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
            userName TEXT ,
            role TINYINT
        )
        """)
        self.connection.commit()
        
    def add_user(self , name , last_name , phone , password , address, userName, role):
        self.cursor.execute("""
        SELECT COUNT(*) AS number_of_user_entry FROM users WHERE userName=?
        """ ,(userName,))
        number_of_user_entry=self.cursor.fetchone()[0]
        # اولین نتیجه ای که پیدا کردی را برگردان
        if number_of_user_entry==0:
            self.cursor = self.connection.cursor()
            if role=="کاربری عادی":
                roleNumber=0
            elif role=="ادمین":
                roleNumber=1
            elif role=="نویسنده":
                roleNumber=2
            self.cursor.execute("""
            INSERT INTO users(Name, lastName, phoneNumber, password, address , userName ,role)
            VALUES (?, ?, ?, ?, ? , ? ,?)
            """,(name, last_name, phone, password, address , userName , roleNumber))
            self.connection.commit()
            msg.showinfo("موفق!" , "کاربر با موفقیت اضافه شد ")
        else:
            msg.showinfo("نام کاربری تکراری " , "این نام کاربری از قبل استفاده شده است ")
               

    def show_user(self , parent):
        dataWindow=tk.Toplevel(parent)
        dataWindow.title('Show data...')
        # اماده کردن بستر خروجی برای مشاهده ی اطلاعات
        table=ttk.Treeview(dataWindow,columns=("Name","lastName","phoneNumber","password", "address" , "userName" ,"role"), show="headings")
        table.heading("Name", text="نام ")
        table.heading("lastName", text="نام خانوادگی ")
        table.heading("phoneNumber", text="شماره تلفن ")
        table.heading("password", text="پسورد")
        table.heading("address", text="آدرس")
        table.heading("address", text="نام کاربری")
        table.heading("address", text="نقش")
        

        table.column("Name", width=120)
        table.column("lastName", width=120)
        table.column("phoneNumber", width=80)
        table.column("password", width=60)
        table.column("address", width=60)
        table.column("address", width=60)
        table.column("address", width=60)
        
        
        self.cursor.execute("SELECT * FROM users")       
        users_data=self.cursor.fetchall()
        
        for item in users_data:
            table.insert("", "end", values=(item[0], item[1], item[2], item[3], item[4] ,item[5] ,item[6]))

        table.pack(padx=2, pady=10, fill=tk.BOTH, expand=True)
user=users()
class tkinter:
    def __init__(self , parent):
        self.win=tk.Toplevel(parent)
        self.win.title("Add User")
        self.win.geometry("500x300")

        tk.Label(self.win , text="name:").grid(row=0, column=0)
        self.Name = tk.Entry(self.win)
        self.Name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.win , text="last name:").grid(row=1, column=0)
        self.lastName = tk.Entry(self.win)
        self.lastName.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.win , text="phone number:").grid(row=2, column=0)
        self.phoneNumber = tk.Entry(self.win)
        self.phoneNumber.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.win , text="password:").grid(row=3, column=0)
        self.password = tk.Entry(self.win)
        self.password.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.win , text="address").grid(row=4, column=0)
        self.address = tk.Entry(self.win)
        self.address.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(self.win , text="User Name").grid(row=5, column=0)
        self.userName = tk.Entry(self.win)
        self.userName.grid(row=5, column=1, padx=5, pady=5)
        
        roles = ["کاربری عادی" , "ادمین" , "نویسنده"]
        roles_var = tk.StringVar(self.win) #?
        roles_var.set(roles[0])
        ttk.Label(self.win , text="roles").grid(row=6 , column=0)
        self.role_combobox = ttk.Combobox(self.win, textvariable=roles_var, values=roles, state="readonly")
        self.role_combobox.grid(row=6, column=1, padx=5, pady=5)

        btn = tk.Button(self.win , text="Add User" , command=lambda: user.add_user (
            self.Name.get(),
            self.lastName.get(),
            self.phoneNumber.get(),
            self.password.get(),
            self.address.get(),
            self.userName.get().strip(),
            self.role_combobox.get()
        ))
        btn.grid(row=7, column=1)

        btn1=tk.Button(self.win , text="Show Users" , command=lambda:user.show_user(self.win))
        btn1.grid(row=8 , column=1)

        self.win.mainloop()