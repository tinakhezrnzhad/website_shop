from flask import Flask, render_template , request, redirect, url_for
# request برای دریافت اطلاعاتی که کاربر در فرم وارد کرده است 
# redirect, url_for برای انتقال کاربر به صفحه های دیگر هستند 
from flask_sqlalchemy import SQLAlchemy
# این ابزار باعث می‌شود به‌جای نوشتن مستقیم دستورات سخت SQL، با کلاس‌ها و آبجکت‌های پایتون با دیتابیس کار کنی.
import os
# برای کار با مسیر ها و پوشه هاست 
# import sqlite3
from werkzeug.utils import secure_filename
# برای امنیت هست که کسی نتواند فایل های مخرب وارد کند 


app = Flask(__name__)

# تنظیمات دیتابیس: اینجا می‌گیم دیتابیس ما یه فایل به اسم site.db باشه
# مسیر فایل دیتابیس رو بر اساس پوشه فعلی تنظیم می‌کنیم
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tinaShop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# فعال کردن این ابزار 

# تعریف مدل محصول (این همون ساختارِ هر محصول توی دیتابیس هست)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) # شناسه منحصر به فرد
    name = db.Column(db.String(100), nullable=False) # نام محصول
    price = db.Column(db.Float, nullable=False) # قیمت
    description = db.Column(db.String(200)) # توضیحات
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg') # نام فایل عکس

    def __repr__(self):
        # این تابع برای نمایش ساده‌ی محصول هنگام تست و اشکال‌زدایی است
        return f"Product('{self.name}', '{self.price}')"

# ایجاد دیتابیس و جدول‌ها (این رو فقط یک بار نیاز داریم اجرا کنیم)
with app.app_context():
    db.create_all()
    # برای اینکه الان سایت خالی نباشه، چند تا محصول تست می‌سازیم
    if not Product.query.first(): # اگه دیتابیس خالی بود...
        p1 = Product(name='لپ‌تاپ HP ZBook', price=45000000.0, description='لپ‌تاپ قدرتمند تینا', image_file='image.jpg')
        p2 = Product(name='ماوس گیمینگ', price=1200000.0, description='خیلی سریع و باحال', image_file='mouse.jpg')
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        print("دیتابیس ساخته شد")

@app.route('/')
# یعنی وقتی http://127.0.0.1:5000/ این را زدی و یا وارد این ادرس شدی بره و اون ادرس اچ تی ام ال را باز کن برام 
def index():
    return render_template('store.html')

@app.route('/products') # آدرس این صفحه می‌شه /products
def show_products():
    all_products = Product.query.all() # همه‌ی محصولات رو از دیتابیس می‌گیریم
    # صفحه products.html رو با لیست محصولات نشون می‌دیم
    return render_template('products.html', products=all_products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # ۱. گرفتن داده‌ها از فرم (دقیقاً با نام‌هایی که توی HTML دادی)
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['discription']
        
        # ۲. مدیریت عکس
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            # ذخیره عکس در پوشه static/uploads
            file.save(os.path.join('static/uploads', filename))
        else:
            filename = 'default.jpg'

        # ۳. ساختن یک محصول جدید و ذخیره در دیتابیس
        new_product = Product(name=name, price=price, description=description, image_file=filename)
        db.session.add(new_product)
        db.session.commit()
        
        return "محصول با موفقیت به دیتابیس اضافه شد"

    return render_template('add_product.html')


if __name__ == '__main__':
    app.run(debug=True)

