import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import sqlite3

# def tkinter():
#     global Name,Price,PDate,EDate,QTy
#     name=Name.get()
#     price=Price.get()
#     Pdate=PDate.get()
#     Edate=EDate.get()
#     Qty=QTy.get()

class product:
    def __init__(self,name,price,Pdate,Edate,Qty):
        self.nameClass=name
        self.priceClass=price
        self.PdateClass=Pdate
        self.EdateClass=Edate
        self.QtyClass=Qty
        # برای overload کردن تابع پرینت در کلاس می توان از تابع __str__ استفاده کرد 
    def __str__(self):
        return(
        f"name:{self.nameClass} \n"
        f"price:{self.priceClass} \n"
        f"Pdate:{self.PdateClass} \n"
        f"Edate:{self.EdateClass} \n"
        f"Qty:{self.QtyClass}"
        )

class anbar:
    def __init__(self):
        # self.products=[]
        self.connection = sqlite3.connect("StoreRoom.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            pdate TEXT,
            edate TEXT,
            qty INTEGER
        )
        """)
        self.connection.commit()
        # برای ذخیره ی اطلاعات 
        
    def add_product(self):
        try:
            name=ps.Name.get()
            price=int(ps.Price.get())
            pdate=ps.PDate.get()
            edate=ps.EDate.get()
            qty=int(ps.QTy.get())
            
            p=product(name,price ,pdate , edate , qty)
            # ذخیره در جدول
            self.cursor.execute("""
            INSERT INTO Stores(name, price, pdate, edate, qty)
            VALUES (?, ?, ?, ?, ?)
            """, (p.nameClass, p.priceClass, p.PdateClass, p.EdateClass, p.QtyClass))

            self.connection.commit()
            
            # self.products.append(p)
            msg.showinfo(title="Success",message= "Product added!")
        except Exception as e:
            print(e)
            msg.showerror("error", "invalid input!")
            
    def show_data_by_tkinter(self):
        dataWindow=tk.Toplevel(ps)
        dataWindow.title('Show data...')
        # اماده کردن بستر خروجی برای مشاهده ی اطلاعات
        table=ttk.Treeview(dataWindow,columns=("Name","Price","PDate","EDate", "QTy"), show="headings")
        table.heading("Name", text="نام ")
        table.heading("Price", text="قیمت ")
        table.heading("PDate", text="تاریخ تولید ")
        table.heading("EDate", text="تاریخ انقضا ")
        table.heading("QTy", text="تعداد محصول ")

        table.column("Name", width=120)
        table.column("Price", width=120)
        table.column("PDate", width=80)
        table.column("EDate", width=60)
        table.column("QTy", width=60)
        
        self.cursor.execute("SELECT name, price, pdate, edate, qty FROM Stores")       
        products = self.cursor.fetchall()
        
        for item in products:
            table.insert("", "end", values=(item[0], item[1], item[2], item[3], item[4]))

        table.pack(padx=2, pady=10, fill=tk.BOTH, expand=True)
            
            
    def search_product_by_name(self, name):
        # list_product=[]
        try:
            self.cursor.execute('SELECT name, price, pdate, edate, qty FROM Stores WHERE name=?' , (name,))      
            return self.cursor.fetchall()
            # دستور  fetchall  میره و اون چیز هایی که توسط کابر به دیتابیس اضافه شده را به صورت یک لیست بر می کرداند 
            #بنابراین هر هر عضو یک تاپل محسوب می شود و هر عضو برابر است با ا نام 
            # عضو 2 قیمت و 3 تاریخ تولید و 4 تاریخ انقضا و 5 تعداد و 
            #مثلا ایتم 1 میشه قیمت و در واقع از اندیس استفاده می کند 
            # for p in products:
            #     if p[0].lower() == name.lower():
            #         list_product.append(p)
                    
            # return list_product
        except:
            msg.showinfo("error","invalid input!")
            
    def search_product_by_price(self  , price ):
        # list_product=[]
        # self.cursor.execute("SELECT name, price, pdate, edate, qty FROM Stores")       
        # products = self.cursor.fetchall()
        # for p in products:
        #     # حالا p یک تاپل هست. p[1] یعنی همان قیمت (چون قیمت در اندیس ۱ هست)
        #     priceS=float(p[1])
        #     if priceS >= price:
        #         list_product.append(p)
        # return list_product
        try:
            #
            # ما به دیتابیس می‌گیم: فقط اونایی رو بیار که قیمت‌شون برابر این عدده
            # query = "SELECT name, price, pdate, edate, qty FROM Stores WHERE price = ?"
                
            # قیمت رو به float تبدیل می‌کنیم تا خیالمون راحت باشه
            self.cursor.execute('SELECT name, price, pdate, edate, qty FROM Stores WHERE price=?' , (int(price),)) 
                
                # حالا محصولات برمی‌گردن (فقط همون‌هایی که شرط رو داشتن!)
            return self.cursor.fetchall()                
        except Exception as e:
            print(f"خطای دیتابیس: {e}")
                
    def delete_product(self , name):
        try:
            # حذف مستقیم از دیتابیس با دستور SQL
            self.cursor.execute("DELETE FROM Stores WHERE name = ?", (name,))
            self.connection.commit()
            # اگر چیزی حذف شده باشه، تغییرات انجام شده
            # اگر روکاونت برابر 0 باشد یعنی هیچی حذف نشده ولی اگر برابر 1 یا از 0 بزرگتر باشد یعنی حذف انجام شده است 
            return self.cursor.rowcount > 0 
        except Exception as e:
            print(e)
            return False
        
    def do_search_for_update(self , oldName):
        try:
            self.cursor.execute('SELECT name, price, pdate, edate, qty FROM Stores WHERE name=?' , (oldName,))      
            return self.cursor.fetchall()
            
        except:
            msg.showinfo("error","invalid input!")
                        
    def update_product(self, oldName,name ,price, Pdate, Edate, Qty):
        try:
            self.cursor.execute("""
                UPDATE Stores 
                SET name=? , 
                price=? , 
                Pdate=? , 
                Edate=? , 
                Qty=?  
                WHERE name=? 
                """,
                (name, price, Pdate, Edate, Qty, oldName))
            self.connection.commit()
                
        except Exception as e:
            print(e)
            return False
def ShowUpdate():
    updatewind=tk.Toplevel(ps)
    updatewind.title('update Item')
    updatewind.geometry("300x150")

    tk.Label( updatewind , text="product name Entry : ").grid(row=0, column=0)
    UpdatenameEntry= tk.Entry(updatewind)
    UpdatenameEntry.grid(row=0, column=1, padx=5, pady=5)
    def do_update():
        oldName = UpdatenameEntry.get()
        # update=updateEntry.get()
        result = myShop.do_search_for_update(oldName)
        #این میره ببینه برای یه اسم که از ورودی دریافت میشه چه کاری بکند 
        #و برای همین میره به تابع سرچ محصول اونجا که گفتیم هربرو داخل لیست محصولات 
        # بگرد . همون لیستی که تابع سازنده ی کلاس انبار بود و اونجا هر چیزی را دیدی که 
        # با محصول وارد شده اسمش برابر بود را بیا نمایش بده 
        if len(result)!=0:
            # for item in result:
            #     myShop[item].name=update
            item=result[0]
            #اولین ورودی یا همان محصول اول که بعدا تغییر داده می شود 
            dataWindow=tk.Toplevel(ps)
            dataWindow.title('update products...')
            
            tk.Label(dataWindow, text="Name").grid(row=0, column=0)
            nameEntry = tk.Entry(dataWindow)
            nameEntry.grid(row=0, column=1)
            # مقدار قبلی را نمایش می دهیم
            nameEntry.insert(0, item[0])
            
            tk.Label(dataWindow, text="Price").grid(row=1, column=0)
            priceEntry = tk.Entry(dataWindow)
            priceEntry.grid(row=1, column=1)
            priceEntry.insert(0, item[1])

            tk.Label(dataWindow, text="PDate").grid(row=2, column=0)
            pdateEntry = tk.Entry(dataWindow)
            pdateEntry.grid(row=2, column=1)
            pdateEntry.insert(0, item[2])
            
            tk.Label(dataWindow, text="EDate").grid(row=3, column=0)
            edateEntry = tk.Entry(dataWindow)
            edateEntry.grid(row=3, column=1)
            edateEntry.insert(0, item[3])
            
            tk.Label(dataWindow, text="Quantity").grid(row=4, column=0)
            qtyEntry = tk.Entry(dataWindow)
            qtyEntry.grid(row=4, column=1)
            qtyEntry.insert(0, item[4])
            
            def save_changes():
                new_name = nameEntry.get()
                new_price = priceEntry.get()
                new_pdate = pdateEntry.get()
                new_edate = edateEntry.get()
                new_qty = qtyEntry.get()
                myShop.update_product(
                    oldName,
                    new_name,
                    new_price,
                    new_pdate,
                    new_edate,
                    new_qty
                )
                msg.showinfo("Done", "Product Updated Successfully")
            btnSave=tk.Button(dataWindow , text="" , command=save_changes)
            btnSave.grid(row=6 , column=1) 
        else:
            msg.showerror("Error", "Product Not Found")
    btn = tk.Button(updatewind,text="Search",command=do_update)
    btn.grid(row=1, column=1)

 
def ShowSerach_by_name():
    wind2=tk.Toplevel(ps)
    wind2.title('Search Item by name')
    wind2.geometry("300x150")

    tk.Label( wind2 , text="Search Entry : ").grid(row=0, column=0)
    searchEntry= tk.Entry(wind2)
    searchEntry.grid(row=0, column=1, padx=5, pady=5)
    def do_search_by_name():
        name = searchEntry.get()
        result = myShop.search_product_by_name(name)
        #این میره ببینه برای یه اسم که از ورودی دریافت میشه چه کاری بکند 
        #و برای همین میره به تابع سرچ محصول اونجا که گفتیم هربرو داخل لیست محصولات 
        # بگرد . همون لیستی که تابع سازنده ی کلاس انبار بود و اونجا هر چیزی را دیدی که 
        # با محصول وارد شده اسمش برابر بود را بیا نمایش بده 
        if len(result)!=0:
            dataWindow=tk.Toplevel(ps)
            dataWindow.title('search data by name ...')
            # اماده کردن بستر خروجی برای مشاهده ی اطلاعات
            table=ttk.Treeview(dataWindow,columns=("Name","Price","PDate","EDate", "QTy"), show="headings")
            table.heading("Name", text="نام ")
            table.heading("Price", text="قیمت ")
            table.heading("PDate", text="تاریخ تولید ")
            table.heading("EDate", text="تاریخ انقضا ")
            table.heading("QTy", text="تعداد محصول ")


            table.column("Name", width=120)
            table.column("Price", width=120)
            table.column("PDate", width=80)
            table.column("EDate", width=60)
            table.column("QTy", width=60)
            
            for item in result:
                table.insert("", "end", values=(item[0], item[1], item[2], item[3], item[4]))

            table.pack(padx=2, pady=10, fill=tk.BOTH, expand=True)
            # for i in result:
            #     print(i)
        else:
            msg.showerror("Error", "Product not found")
    btn = tk.Button(wind2 , text="show" , command=do_search_by_name)
    btn.grid(row=1, column=0)
    
def ShowSerach_by_price():
    windprice=tk.Toplevel(ps)
    windprice.title('Search Item by price')
    windprice.geometry("300x150")

    tk.Label( windprice , text="Search Entry : ").grid(row=0, column=0)
    searchPriceEntry= tk.Entry(windprice)
    searchPriceEntry.grid(row=0, column=1, padx=5, pady=5)
    
    def do_search_by_price():
        input_value = searchPriceEntry.get()
        if not input_value: # اگه فیلد خالی بود
            msg.showwarning("Warning", "لطفاً یک قیمت وارد کنید!")
            return
            
        price = int(input_value)
        result = myShop.search_product_by_price(price)
        if result is None:
            result = []
        #این میره ببینه برای یه اسم که از ورودی دریافت میشه چه کاری بکند 
        #و برای همین میره به تابع سرچ محصول اونجا که گفتیم هربرو داخل لیست محصولات 
        # بگرد . همون لیستی که تابع سازنده ی کلاس انبار بود و اونجا هر چیزی را دیدی که 
        # با محصول وارد شده اسمش برابر بود را بیا نمایش بده 
        # if len(result)!=0:
        elif len(result) != 0:
            dataWindow=tk.Toplevel(ps)
            dataWindow.title('searhc data by price ...')
            # اماده کردن بستر خروجی برای مشاهده ی اطلاعات
            table=ttk.Treeview(dataWindow,columns=("Name","Price","PDate","EDate", "QTy"), show="headings")
            table.heading("Name", text="نام ")
            table.heading("Price", text="قیمت ")
            table.heading("PDate", text="تاریخ تولید ")
            table.heading("EDate", text="تاریخ انقضا ")
            table.heading("QTy", text="تعداد محصول ")

            table.column("Name", width=120)
            table.column("Price", width=120)
            table.column("PDate", width=80)
            table.column("EDate", width=60)
            table.column("QTy", width=60)
            
            for item in result:
                table.insert("", "end", values=(item[0], item[1], item[2], item[3], item[4]))

            table.pack(padx=2, pady=10, fill=tk.BOTH, expand=True)
            # for i in result:
            #     print(i)
        else:
            msg.showerror("Error", "Product not found")
    btn = tk.Button(windprice , text="show" , command=do_search_by_price)
    btn.grid(row=1, column=0)

def Showdelete():
    wind3=tk.Toplevel(ps)
    wind3.title('Delete Item')
    wind3.geometry("300x150")

    tk.Label( wind3 , text="Delete Entry : ").grid(row=0, column=0)
    deleteEntry= tk.Entry(wind3)
    deleteEntry.grid(row=0, column=1, padx=5, pady=5)
    def do_delete():
        name=deleteEntry.get()
        result = myShop.delete_product(name)
        if result:
            msg.showinfo(title="Result", message="product deleted successfuly !")
        else:
            msg.showerror("Error", "Product not deleted !")
    btn = tk.Button(wind3 , text="delete" , command=do_delete)
    btn.grid(row=1, column=0)

myShop=anbar()

class page_shape:
    def __init__(self):
        self.win=tk.Tk()
        self.win.title("classProject")
        self.win.geometry("500x300")

        tk.Label( self.win , text="name").grid(row=0, column=0)
        self.Name = tk.Entry(self.win)
        self.Name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label( self.win , text="price").grid(row=1, column=0)
        self.Price = tk.Entry(self.win)
        self.Price.grid(row=1, column=1, padx=5, pady=5)

        tk.Label( self.win , text="Pdate").grid(row=2, column=0)
        self.PDate = tk.Entry(self.win)
        self.PDate.grid(row=2, column=1, padx=5, pady=5)

        tk.Label( self.win , text="Edate").grid(row=3, column=0)
        self.EDate = tk.Entry(self.win)
        self.EDate.grid(row=3, column=1, padx=5, pady=5)

        tk.Label( self.win , text="Qty").grid(row=4, column=0)
        self.QTy = tk.Entry(self.win)
        self.QTy.grid(row=4, column=1, padx=5, pady=5)

        btn1 = tk.Button(self.win , text="add data" , command=myShop.add_product)
        btn1.grid(row=5, column=1)

        btn2 = tk.Button(self.win , text="search by name " , command=ShowSerach_by_name)
        btn2.grid(row=7, column=1)

        btn5 = tk.Button(self.win , text="search by price " , command=ShowSerach_by_price)
        btn5.grid(row=8, column=1)

        btn3 = tk.Button(self.win , text="show data" , command=myShop.show_data_by_tkinter)
        btn3.grid(row=9, column=1)

        btn4 = tk.Button(self.win , text="delete data" , command=Showdelete)
        btn4.grid(row=10, column=1)

        btn = tk.Button(self.win , text="update data" , command=ShowUpdate)
        btn.grid(row=11, column=1)

        self.win.mainloop()
ps=page_shape()
