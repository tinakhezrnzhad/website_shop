# فلسک در واقع باعث میشه برنامه روی سرور مرورگر باز بشه و برای نمایش دادنش به سی اس اس و اچ تی ام ال و جاوا اسکریپت نیاز داریم
from flask import Flask, render_template , request, redirect, url_for , session
# session یک فضای کوچک برای نگه‌داشتن اطلاعات مربوط به یک کاربر
#  برای پیدا کردن فایل های اچ تی ام ال است render_template
# request برای دریافت اطلاعاتی که کاربر در فرم وارد کرده است 
# redirect, url_for برای انتقال کاربر به صفحه های دیگر هستند 
from flask_sqlalchemy import SQLAlchemy
# این ابزار باعث می‌شود به‌جای نوشتن مستقیم دستورات سخت SQL، با کلاس‌ها و آبجکت‌های پایتون با دیتابیس کار کنی.
#  اصلا لازم دستورات دیتابیس را وارد کنی بلکه اینجا  با یک سری کد میتونی به sqalchemy بگی برو در دیتابیس همین کاری برایم انجام بده مانند نمایندهیعنی 
import os
# برای کار با مسیر ها و پوشه هاست 
from werkzeug.utils import secure_filename
# برای امنیت هست که کسی نتواند فایل های مخرب وارد کند 
from werkzeug.security import generate_password_hash
# برای هش کردن رمز عبور
from werkzeug.security import check_password_hash
# برای چک کردن رمز عبور هش شده
from datetime import datetime

app = Flask(__name__)
# اینجا فلاسک را داخل یک متغیر به اسم app می گذاریم 

app.secret_key = 'your-secret-key'
# برای قسمت سشن لازم است 

# مسیر فایل دیتابیس رو بر اساس پوشه فعلی تنظیم می‌کنیم
basedir = os.path.abspath(os.path.dirname(__file__))
# تنظیمات مربوط به دیتابیس اینجا میگیم یک دیتابیس به اسم .... را در مسیر فایل app.py  بساز 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tinaShop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # ؟

db = SQLAlchemy(app)
# فعال کردن دیتابیس جوری که فلاسک یا برنامه به ان دسترسی داشته باشد 

# اینجا به دیتابیس میگیم برو یه جدول بساز و اسمش را از اسم کلاس ایده بگیر و ستون های داخل حپجدول را هم قرار بده
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) # شناسه منحصر به فرد
    name = db.Column(db.String(100), nullable=False) # نام محصول
    price = db.Column(db.Integer, nullable=False) # قیمت
    description = db.Column(db.String(200)) # توضیحات
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg') # نام فایل عکس

    # def __repr__(self):
    #     # این تابع برای نمایش ساده‌ی محصول هنگام تست و اشکال‌زدایی است
    #     return f"Product('{self.name}', '{self.price}')"
    
#اینجا هم به دیتابیس میگیم برو یه جدول بساز و اسمش را از اسم کلاس ایده بگیر و این ستون ها را داخلش قرار بده 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_email = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)  # unique=Trueنام کاربری تکراری مجاز نیست  یعنی ذخیره ی 
    password = db.Column(db.String(200), nullable=False)  # برای ذخیره پسورد هش‌ شده
    role = db.Column(db.String(30), nullable=False, default="user")

    # def __repr__(self):
    #     return f"User('{self.username}')"
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30),nullable=False,default="pending")
    created_at = db.Column(db.DateTime,default=datetime.utcnow )


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,db.ForeignKey('order.id'),nullable=False)
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float,nullable=False)


# ایجاد دیتابیس و جدول‌ها (این رو فقط یک بار نیاز داریم اجرا کنیم)
with app.app_context():
    db.create_all()
    # برای اینکه الان سایت خالی نباشه، چند تا محصول تست می‌سازیم
    # if not Product.query.first(): # اگه دیتابیس خالی بود...
    #     p1 = Product(name='لپ‌تاپ HP ZBook', price=45000000.0, description='لپ‌تاپ قدرتمند تینا', image_file='image.jpg')
    #     p2 = Product(name='ماوس گیمینگ', price=1200000.0, description='خیلی سریع و باحال', image_file='mouse.jpg')
    #     db.session.add(p1)
    #     db.session.add(p2)
    #     db.session.commit()
    #     print("دیتابیس ساخته شد")

@app.route('/')
# یعنی وقتی http://127.0.0.1:5000/ این را زدی و یا وارد این ادرس شدی بره و اون ادرس اچ تی ام ال را باز کن برام 
def index():
    return render_template('store.html')

@app.route('/products') # آدرس این صفحه می‌شه /products
def show_products():
    all_products = Product.query.all() # همه‌ی محصولات رو از دیتابیس می‌گیریم
    # صفحه products.html رو با لیست محصولات نشون می‌دیم
    return render_template('products.html', xy=all_products)

@app.route('/add_product', methods=['GET', 'POST'])
# یعنی وقتی رفتی داخل اون سایت دو تا چیز اتفاق میافته یکی اینکه محصولات را میگری و بعد برابر با محصولات پست اونها به جایی دیگر است 
def add_product():
    # اگر رویدکه ی داخل سایت کلیک شد
    # اطلاعات پایین گرفته شوند و به دیتابیس اضافه شوند و سپس در صفحه ی محصولات نمایش داده شوند
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['discription']
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            # ذخیره عکس در پوشه static/uploads
            file.save(os.path.join('static/uploads', filename))
        else:
            filename = 'default.jpg'

        # ساختن یک محصول جدید و ذخیره در دیتابیس
        new_product = Product(name=name, price=price, description=description, image_file=filename)
        db.session.add(new_product)
        db.session.commit()

    return render_template('add_product.html')


@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # ۱. گرفتن مقادیر از فرم بر اساس name تگ‌های html
        first_name = request.form['name']
        last_name = request.form['LastName']
        phone_email = request.form['phoneEmail']
        username = request.form['userName']
        password = request.form['password']

        # ۲. چک کردن اینکه آیا نام کاربری قبلاً ثبت شده یا نه
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "این نام کاربری قبلاً ثبت شده است! لطفاً نام دیگری انتخاب کنید."
        # ۳. هش کردن پسورد (برای اینکه پسورد خام تو دیتابیس نمونه)
        hashed_password = generate_password_hash(password)
        # ۴. ساختن کاربر جدید با کلاس User
        new_user = User(first_name=first_name,last_name=last_name,phone_email=phone_email,username=username,password=hashed_password ,role="user")
        # ۵. ذخیره در دیتابیس
        db.session.add(new_user)
        db.session.commit()
        # بعد از ثبت‌نام موفق، می‌فرستیمش به صفحه اصلی (store.html)
        return redirect(url_for('index'))
    # وقتی کاربر فقط آدرس صفحه رو باز می‌کنه
    return render_template('signin.html')

@app.route('/logIn', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # دریافت داده‌ها
        username = request.form.get('userName')
        password = request.form.get('password') # چک کن حتما تو HTML همین باشه

        # پیدا کردن کاربر
        user = User.query.filter_by(username=username).first()

        # بررسی نهایی
        if user and check_password_hash(user.password, password):
            return "ورود موفقیت‌آمیز بود!"
        else:
            return "نام کاربری یا رمز عبور اشتباه است."

    return render_template('login.html')

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
# این روت فقط کار کلیک روی دکمه ی اضافه کردن به سبد را مدیریت می کند
def add_to_cart(product_id):

    cart = session.get('cart', {})
    # در واقع اون چیزیه که کاربر کلیک کرده مثلا محصول 2 را 1 بار کلیک کرده

    product_id = str(product_id)

    # این شرط برای بررسی موجودیت است 
    # اگر ایدی محصول در دیکشنری وجود داشت به اون ایدی یکی دیگه هم اضافه کند 
    # در غیر اینصورت فقط یکی را برابرش قرار دهد 
    if product_id in cart:
        cart[product_id] += 1
        # اگر چند کلیک کرد به تعداد دفعات کلیک اضافه شود 
    else:
        cart[product_id] = 1

    session['cart'] = cart

    return redirect(url_for('show_products'))

@app.route('/cart')
def show_cart():
    cart = session.get('cart', {})
    # برو داخل دیکشنری بگرد و ایدی و تعداد را بگیر 

    products = []
    grand_total = 0

    for product_id, quantity in cart.items():
        # برو داخل چیز هایی که پیدا کردی در کارت ایدی محصولات و تعداد را برگردان

        product = db.session.get(Product, product_id)
        # حالا برو داخل دیتابیس و باتوجه به ایدی محصول اطلاعات ان محصول را پیدا کن و بده به سشن تا برگرداند

        if product:
            item_total = product.price * quantity
            # حالا اگر برگرداند در بین اطلاعات محصول قیمتش را پیدا کن و در تعداد که بالاتر در سشن دریافت کردی ضرب کن 

            grand_total += item_total
            # وهربار قیمت محصولات را اینگونه محاسبه و به اینجا اضافه کن 

            products.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })

    return render_template(
        'cart.html',
        products=products,
        grand_total=grand_total
        # و اینجا در صفحه ی سبد خرید فقط جمع کل را برمیگرداند
    )

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):

    cart = session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    session['cart'] = cart

    return redirect(url_for('show_cart'))

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):

    cart = session.get('cart', {})

    product_id = str(product_id)

    quantity = int(request.form['quantity'])

    if product_id in cart:
        cart[product_id] = quantity

    session['cart'] = cart

    return redirect(url_for('show_cart'))

@app.route('/admin_register', methods=['GET', 'POST'])
def admin_signup():
    
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("admin_login"))

    current_user = User.query.get(user_id)

    if not current_user or current_user.role != "super_admin":
        return "دسترسی غیرمجاز", 403
    
    if request.method == 'POST':
        # ۱. گرفتن مقادیر از فرم بر اساس name تگ‌های html
        first_name = request.form['name']
        last_name = request.form['LastName']
        phone_email = request.form['phoneEmail']
        username = request.form['userName']
        password = request.form['password']
        role = request.form['role']

        # ۲. چک کردن اینکه آیا نام کاربری قبلاً ثبت شده یا نه
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "این نام کاربری قبلاً ثبت شده است! لطفاً نام دیگری انتخاب کنید."
        # ۳. هش کردن پسورد (برای اینکه پسورد خام تو دیتابیس نمونه)
        hashed_password = generate_password_hash(password)
        # ۴. ساختن کاربر جدید با کلاس User
        new_user = User(first_name=first_name,last_name=last_name,phone_email=phone_email,username=username,password=hashed_password ,role=role)
        # ۵. ذخیره در دیتابیس
        db.session.add(new_user)
        db.session.commit()
        # بعد از ثبت‌نام موفق، می‌فرستیمش به صفحه اصلی (store.html)
        return redirect(url_for('index'))
    # وقتی کاربر فقط آدرس صفحه رو باز می‌کنه
    return render_template('admin_signin.html')

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("userName")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        # برو بر اساس نام کابری سرچ کن 

        if user and check_password_hash(user.password, password):
            # اگر همچین نام کاربری یا پسوردی اونجا بود بیا و...
            
            print("USERNAME:", user.username)
            print("ROLE:", user.role)

            if user.role in ["super_admin", "product_admin", "user_admin"]:
                # چک کن نقش را 
                session["user_id"] = user.id
                # شناسه‌ی کاربر رو داخل session نگه می‌داریم تا Flask بفهمه چه کسی وارد شده.
                return redirect(url_for("admin_p"))

            return "شما دسترسی ادمین ندارید."

        return "نام کاربری یا رمز عبور اشتباه است."

    return render_template("admin_login.html")


@app.route("/admin_panel")
def admin_p():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("admin_login"))

    user = User.query.get(user_id)

    if not user or user.role not in ["super_admin", "product_admin", "user_admin"]:
        return "دسترسی غیرمجاز", 403

    return render_template("admin_panel.html", role=user.role)

@app.route("/admin/products")
def admin_products():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("admin_login"))

    user = User.query.get(user_id)

    if not user or user.role not in ["super_admin", "product_admin"]:
        return "دسترسی غیرمجاز", 403
    
    all_products = Product.query.all() # همه‌ی محصولات رو از دیتابیس می‌گیریم
        # صفحه products.html رو با لیست محصولات نشون می‌دیم
    return render_template("admin_products.html", xy=all_products)


@app.route("/admin/users")
def admin_users():
    user_id = session.get("user_id")
    
    if not user_id:
        return redirect(url_for("admin_login"))

    user = User.query.get(user_id)

    if not user or user.role not in ["super_admin", "user_admin"]:
        return "دسترسی غیرمجاز", 403
    
    users = User.query.all()
    return render_template("admin_users.html" , users=users)

@app.route("/aboutMe")
def a_me():
    return render_template('about_me.html')

@app.route("/checkout", methods=["POST"])
def checkout_o():

    user_id = session.get("user_id")
    # پیدا کردن کاربر با استفاده از سشن است 

    if not user_id:
        return "لطفاً ابتدا وارد حساب کاربری خود شوید.", 401

    cart = session.get("cart", {})
    # برو داخل دیکشنری محصولات را برگردان 
    # اگر خالی بود بگو محصولی در سبد خرید نیست 

    if not cart:
        return "سبد خرید خالی است."
    # ساخت سفارش اصلی
    new_order = Order(
        user_id=user_id,
        total_price=0,
        status="pending"
    )
    db.session.add(new_order)
    # فعلاً برای اینکه order_id ساخته شود
    db.session.flush()
    # برو محصولات را بفرست به دیتابیس و من بعدش ایدی را پیدا خواهم کرد 

    grand_total = 0

    # بررسی محصولات داخل سبد
    for product_id, quantity in cart.items():

        product = db.session.get(Product, product_id)

        if product:

            item_total = product.price * quantity

            grand_total += item_total

            # ذخیره محصول داخل سفارش
            new_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=quantity,
                price=product.price
            )
            db.session.add(new_item)

    # ثبت جمع کل سفارش
    new_order.total_price = grand_total
    # حالا جا خالی های محصولی که ساخته میشود پر خواهد شد 
    # ذخیره همه اطلاعات
    db.session.commit()
    # پاک کردن سبد خرید
    session['cart'] = {}
    return render_template(
        "succes_order.html",
        order=new_order
    )

if __name__ == '__main__':
    app.run(debug=False)

# 1- وقتی در سبد خرید روی روی پرداخت کلیک میکنم یه اروری میاره (Method Not Allowed
# The method is not allowed for the requested URL.)

# 2-باید قسمت orders را هم درست کنم در ادمین پنل 

# 3- باید اگه چیزی انجام شد مثل اضافه شدن به سبد خرید یه پیام از گوشه ای از صفحه بیاد بیرون 