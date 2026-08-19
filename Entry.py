import tkinter as tk 
# from tkinter import messagebox as msg
from Main import page_shape
# فقط کلاس رابط کاربری امده است 
# و رابط کاربری جوری طراحی شده است که با اجرای ان بقیه ی کلاس ها نیز اجرا خواهد شد 
from add_user import tkinter


class user_interface:
    def __init__(self , parent):
        self.win=tk.Toplevel(parent)
        self.win.title("فروشگاه")
        self.win.geometry("500x300")

        btn_main=tk.Button(self.win , text="ورود به برنامه "  , command=self.conn_main)
        btn_main.grid(row=2 , column=3)

        btn_users=tk.Button(self.win , text="تعریف کاربر " , command=self.conn_users)
        btn_users.grid(row=2  , column=2 , padx=50 , pady=50)

        self.win.mainloop()
        
    def conn_main(self):
        page_shape(self.win)
    def conn_users(self):
        tkinter(self.win)