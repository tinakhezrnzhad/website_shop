# فلسک در واقع باعث میشه برنامه روی سرور مرورگر باز بشه و برای نمایش دادنش به سی اس اس و اچ تی ام ال و جاوا اسکریپت نیاز داریم
from flask import Flask, render_template , request, redirect, url_for , session , jsonify 
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
# برای بررسی زمان سفارش 


app = Flask(__name__)
# اینجا فلاسک را داخل یک متغیر به اسم app می گذاریم 

app.secret_key = 'your-secret-key'
# برای قسمت سشن لازم است 

# مسیر فایل دیتابیس رو بر اساس پوشه فعلی تنظیم می‌کنیم
basedir = os.path.abspath(os.path.dirname(__file__))
# تنظیمات مربوط به دیتابیس اینجا میگیم یک دیتابیس به اسم .... را در مسیر فایل app.py  بساز 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tinaShop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # ؟
app.config["UPLOAD_FOLDER"] = "static/uploads"

db = SQLAlchemy(app)
# فعال کردن دیتابیس جوری که فلاسک یا برنامه به ان دسترسی داشته باشد 


class main_categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # نام محصول
    description = db.Column(db.String(200)) # توضیحات
    sub_categories = db.relationship('sub_categories',back_populates="main_category",lazy=True)
    #ببین اینجا میگیم بیا بین دو ا جدول رابطه ی دو طرفه برطرف کن که هردو با هم ارتباط داشته باشند با استفاده از بکپاپیولیتس
    
class sub_categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_categories_id = db.Column(db.Integer ,db.ForeignKey("main_categories.id") )
    name = db.Column(db.String(100), nullable=False) # نام محصول
    main_category = db.relationship("main_categories",back_populates="sub_categories")
#ببین اینجا میگیم بیا بین دو ا جدول رابطه ی دو طرفه برطرف کن که هردو با هم ارتباط داشته باشند با استفاده از بکپاپیولیتس

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) # شناسه منحصر به فرد
    sub_categories_id = db.Column(db.Integer, db.ForeignKey("sub_categories.id"))
    name = db.Column(db.String(100), nullable=False) # نام محصول
    price = db.Column(db.Integer, nullable=False) # قیمت
    brand = db.Column(db.String(100))
    weight = db.Column(db.Float)
    Inventory = db.Column(db.Integer)
    description = db.Column(db.String(200)) # توضیحات
    image_file = db.Column(db.String(100),default='default.jpg') # نام فایل عکس
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sub_category = db.relationship("sub_categories",backref="products")
    # اینجا از بکرف استفاده کردیم چون فقط محصول به محصول فرعی دارد و رابطه دو سویه نیست

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
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30),nullable=False,default="pending")
    created_at = db.Column(db.DateTime,default=datetime.utcnow )


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,db.ForeignKey('order.id'),nullable=False)
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer,nullable=False)
    product = db.relationship("Product")
    
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    adress = db.Column(db.String(300), nullable=False)
    telephone = db.Column(db.Integer, nullable=False)
    
class buying_factor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Company_id = db.Column(db.Integer,db.ForeignKey('company.id'),nullable=False)
    Product_id = db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    company = db.relationship( "Company", backref="buying_factors")
    product =  db.relationship( "Product", backref="buying_factors" )
    
class selling_factor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    User_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    Product_id = db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user = db.relationship( "User", backref="selling_factors" )
    product = db.relationship( "Product", backref="selling_factors")
    
class SupportMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column( db.Integer, db.ForeignKey("user.id"), nullable=False )
    message = db.Column( db.Text, nullable=False)
    created_at = db.Column( db.DateTime, default=datetime.utcnow)
    is_read = db.Column( db.Boolean, default=False)
    sender = db.Column( db.String(20),  nullable=False,  default="user" )
    user = db.relationship( "User",  backref="support_messages")
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column( db.Integer, db.ForeignKey("user.id"), nullable=False )
    comment = db.Column(  db.Text,  nullable=False)
    created_at = db.Column(  db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(  db.Boolean,  default=False)
    user = db.relationship( "User", backref="comments")
# ایجاد دیتابیس و جدول‌ها (این رو فقط یک بار نیاز داریم اجرا کنیم)
# این تابع فقط اولین بار لازم است و در صورتی که دیتابیس حذف شده باشد و دوباره قصد راه اندازی ان را داشته باشی 
with app.app_context():
    db.create_all()

@app.route('/home')
# یعنی وقتی http://127.0.0.1:5000/ این را زدی و یا وارد این ادرس شدی بره و اون ادرس اچ تی ام ال را باز کن برام 
def index():
    return render_template('store.html')

@app.route('/' ,  methods=['GET', 'POST'])
def show_products():

    categories = main_categories.query.all()

    category_id = request.args.get('category_id', type=int)
    sub_category_id = request.args.get('sub_category_id', type=int)
    availability = request.args.get('availability')
    sort = request.args.get('sort')
    search = request.args.get('search')


    query = Product.query
    
    if sub_category_id:

        query = (
            query.filter(
                Product.sub_categories_id == sub_category_id,
                Product.is_active == True
            )
        )

    elif category_id:

        query = (
            query.join( sub_categories, Product.sub_categories_id == sub_categories.id
            ) .filter(   sub_categories.main_categories_id == category_id, Product.is_active == True )
        )

    else:

        query = query.filter_by( is_active=True)
        # برای شرط مقدار از فیلتر بای استفاده میکنیم 

    if search:
        query = query.filter(Product.name.contains(search))
    
    if availability == 'available':
        query = query.filter(Product.Inventory > 0)
        # برای شرط منطقی از فیلتر

    elif availability == 'unavailable':
        query = query.filter(Product.Inventory == 0)
        
    elif availability == 'all':
        pass
    
    if sort == "default":
        pass
    
    elif sort == "newest":
        query = query.order_by(Product.created_at.desc())
        
    elif sort == "price_low":
        query = query.order_by(Product.price.asc())
        
    elif sort == "price_high":
        query = query.order_by(Product.price.desc()) 
    
    elif sort == "name":
        query = query.order_by(Product.name.asc()) 
        # این بحث مرتب کردنه نه پیدا کردن چیزی به همین دلیل از اوردر بای استفاده میکنیم
        
    elif sort == "random":
        query = query.order_by(db.func.random())
        
        
    products = query.all()
        
    return render_template(
        'products.html',
        categories=categories,
        products=products,
        selected_category_id=category_id,
        selected_sub_category_id=sub_category_id 
    )
    
@app.route('/product/<int:product_id>')
def product_detail(product_id):

    product = db.session.get(Product, product_id)

    if not product:
        return "محصول پیدا نشد", 404

    if not product.is_active:
        return "این محصول در حال حاضر موجود نیست", 404

    return render_template(
        'detail_products.html',
        product=product
    )

@app.route('/edit_products/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = db.session.get(Product, product_id)

    if not product:
        return "محصول پیدا نشد", 404

    if request.method == 'POST':
        product.name = request.form["product_name"]
        product.price = request.form["price"]
        product.brand = request.form["brand"]
        product.weight = request.form["weight"]
        product.Inventory = request.form["Inventory"]
        product.description = request.form["description"]
        image = request.files.get("image")
        if image and image.filename:
            image_filename = image.filename
            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    image_filename
                )
            )
            product.image_file = image_filename

        db.session.commit()
        return redirect(url_for("admin_products"))

    else:
        return render_template( "check_products.html", product=product)


@app.route('/add_main_product', methods=['GET', 'POST'])
# یعنی وقتی رفتی داخل اون سایت دو تا چیز اتفاق میافته یکی اینکه محصولات را میگری و بعد برابر با محصولات پست اونها به جایی دیگر است 
def add_main_product():
    # اگر رویدکه ی داخل سایت کلیک شد
    # اطلاعات پایین گرفته شوند و به دیتابیس اضافه شوند و سپس در صفحه ی محصولات نمایش داده شوند
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        # ساختن یک محصول جدید و ذخیره در دیتابیس
        new_product = main_categories(name=name, description=description)
        db.session.add(new_product)
        db.session.commit()
        
    categories = main_categories.query.all()
    

    return render_template('add_main_product.html' , categories=categories)

@app.route("/add_sub_product", methods=['GET', 'POST'])
def add_sub_product():
    if request.method == 'POST':
        main_category_id = request.form['main_category_id']
        sub_category_name = request.form['sub_category_name']
        # پیدا کردن دسته اصلی
        main_category = db.session.get(main_categories, main_category_id)
        # با توجه به اسمیکه انتخاب شده برو ایدی را پیدا کن و در جدول دیتابیسقرار بده

        if main_category:

            new_sub_category = sub_categories(
                main_categories_id=main_category.id,
                name=sub_category_name
            )

            db.session.add(new_sub_category)
            db.session.commit()
            
    categories = sub_categories.query.all()
    main_categories_list = main_categories.query.all()    
    
    return render_template('add_sub_product.html' , categories=categories ,main_categories_list=main_categories_list)

@app.route("/add_product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":
        sub_category_id = request.form["sub_category_id"]
        product_name = request.form["product_name"]
        price = request.form["price"]
        brand = request.form["brand"]
        weight = request.form["weight"]
        Inventory = request.form["Inventory"]
        description = request.form["description"]
        image = request.files.get("image")
        image_filename = "default.jpg"

        if image and image.filename:
            image_filename = image.filename
            image.save(os.path.join(app.config["UPLOAD_FOLDER"],image_filename))

        new_product = Product(
            sub_categories_id=sub_category_id,
            name=product_name,
            price=price,
            brand=brand,
            weight=weight,
            Inventory=Inventory,
            description=description,
            image_file=image_filename
        )

        db.session.add(new_product)
        db.session.commit()

    products = Product.query.all()
    main_categories_list = main_categories.query.all()
    sub_categories_list = sub_categories.query.all()

    return render_template(
        "add_product.html",
        products=products,
        main_categories_list=main_categories_list,
        sub_categories_list=sub_categories_list
    )

@app.route("/get_sub_categories/<int:main_category_id>")
# تابعی که بتونه محصولات فرعی را بر اساس ایدی محصولات اصلی برگرداند
def get_sub_categories(main_category_id):

    sub_categories_list = sub_categories.query.filter_by(
        main_categories_id=main_category_id
    ).all()
    # تمام محصولات فرعی مربوط به یک محصول اصلی که بر اساس ایدی مشخصی شود برگردنده میشود

    return [
        {
            "id": category.id,
            "name": category.name
        }
        for category in sub_categories_list
    ]

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
        
        session['user_id'] = new_user.id 
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
            session['user_id'] = user.id  # حالا ست کن
            return jsonify({"status":"success " , "message":"کاربر گرامی با موفقیت وارد شدید"})
        else:
            return jsonify({"status":"error" , "message":"کاربر گرامی نام کاربری یا رمز عبور اشتباه است "})
        
    return render_template('login.html')

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):

    product = db.session.get(Product, product_id)

    if not product:
        return "محصول پیدا نشد", 404

    # بررسی فعال بودن محصول
    if not product.is_active:
        return "این محصول در حال حاضر فعال نیست", 400

    # بررسی موجودی
    if not product.Inventory or product.Inventory <= 0:
        return "این محصول ناموجود است", 400

    cart = session.get('cart', {})

    product_id = str(product_id)

    current_quantity = cart.get(product_id, 0)

    # جلوگیری از بیشتر شدن تعداد سبد از موجودی
    if current_quantity >= product.Inventory:
        return "تعداد درخواستی بیشتر از موجودی محصول است", 400

    cart[product_id] = current_quantity + 1

    session['cart'] = cart

    return redirect(url_for('product_detail' , product_id=product.id))

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

    cart_error = session.pop('cart_error', None)
    
    return render_template(
        'cart.html',
        products=products,
        grand_total=grand_total,
        cart_error=cart_error
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

@app.route('/logout' ,  methods=['POST'])
def logout():
    if "user_id" in session:
        del session['user_id']
    
    return redirect(url_for('show_products'))

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):

    cart = session.get('cart', {})

    product_id = str(product_id)
    try:
        quantity = int(request.form['quantity'])
    except (ValueError, TypeError):
        session['cart_error'] = "تعداد وارد شده صحیح نیست."
        return redirect(url_for('show_cart'))
    
    product = db.session.get(Product, product_id)

    if not product:
        session['cart_error'] = "محصول پیدا نشد."
        return redirect(url_for('show_cart'))

    if quantity < 1:
        session['cart_error'] = "تعداد باید حداقل ۱ باشد."
        return redirect(url_for('show_cart'))

    if quantity > product.Inventory:
        session['cart_error'] = (
            f"موجودی محصول «{product.name}» فقط "
            f"{product.Inventory} عدد است."
        )
        return redirect(url_for('show_cart'))

    if product_id in cart:
        cart[product_id] = quantity

    session['cart'] = cart

    return redirect(url_for('show_cart'))

# خلاصه ای که در بالای صحفه قرار گرفته
@app.route('/checkout', methods=['POST'])
def checkout_o():

    user_id = session.get('user_id')

    if not user_id:
        return "لطفاً ابتدا وارد حساب کاربری شوید.", 401

    cart = session.get('cart', {})

    if not cart:
        return "سبد خرید شما خالی است.", 400

    grand_total = 0

    order_items = []

    for product_id, quantity in cart.items():

        product = db.session.get(Product, product_id)

        if not product:
            continue

        if not product.is_active:
            return f"محصول «{product.name}» دیگر فعال نیست.", 400

        if quantity > product.Inventory:
            return (
                f"موجودی محصول «{product.name}» "
                f"فقط {product.Inventory} عدد است."
            ), 400

        item_total = product.price * quantity

        grand_total += item_total
        
        order_items.append({
            'product': product,
            'quantity': quantity,
            'price': product.price
        })

    if not order_items:
        return "هیچ محصول معتبری در سبد خرید وجود ندارد.", 400

    order = Order(
        user_id=user_id,
        total_price=grand_total,
        status="ثبت شده"
    )

    db.session.add(order)

    db.session.flush()

    for item in order_items:

        order_item = OrderItem(
            order_id=order.id,
            product_id=item['product'].id,
            quantity=item['quantity'],
            price=item['price']
        )

        db.session.add(order_item)

        item['product'].Inventory -= item['quantity']
        # وقتی خریدی انجام میشد هربار موج.دی محصول کم شود 

    db.session.commit()

    session['cart'] = {}

    return render_template('succes_order.html', order=order)

@app.route('/admin_register', methods=['GET', 'POST'])
def admin_signup():
    
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("admin_login"))

    current_user = db.session.get(User, user_id)

    if not current_user or current_user.role != "super_admin":
        return "دسترسی غیرمجاز", 403
    
    if request.method == 'POST':

        first_name = request.form.get('name')
        last_name = request.form.get('LastName')
        phone_email = request.form.get('phoneEmail')
        username = request.form.get('userName')
        password = request.form.get('password')
        role = request.form.get('role')

        if not all([first_name, last_name, phone_email, username, password, role]):
            return "لطفاً همه فیلدها را کامل کنید."

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "این نام کاربری قبلاً ثبت شده است!"

        hashed_password = generate_password_hash(password)

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            phone_email=phone_email,
            username=username,
            password=hashed_password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()
    users = User.query.all()
    # وقتی کاربر فقط آدرس صفحه رو باز می‌کنه
    return render_template('admin_signin.html', users=users)

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

            if user.role in ["super_admin", "product_admin", "user_admin" , "chat_admin" , "order_admin"]:
                # چک کن نقش را 
                session["user_id"] = user.id
                # شناسه‌ی کاربر رو داخل session نگه می‌داریم تا Flask بفهمه چه کسی وارد شده.
                # این سشن باعث میشه وقتی یکبار وارد میشی بتونی بدون لاگ وارد ادمین پنل بشی یعنی اگر 
                # ادرس ادمین پنل در قسمت جستجو سرچ کردی بتونی وارد بشی 
                # اما بعد از حذف صفحه یا بستن صفحه دیگه این سشن هم از کار میافتد
                return redirect(url_for("admin_p"))

            return jsonify({"status":"error" , "message":"شما دسترسی ادمین ندارید"})


        return jsonify({"status":"error" , "message":"کاربر گرامی نام کاربری یا رمز عبور اشتباه است "})


    return render_template("admin_login.html")


@app.route("/admin_panel")
def admin_p():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("admin_login"))

    user = db.session.get(User, user_id)

    if not user or user.role not in ["super_admin", "product_admin", "user_admin" , "chat_admin" , "order_admin"]:
        return "دسترسی غیرمجاز", 403

    return render_template("admin_panel.html", role=user.role)


@app.route("/admin/users")
def admin_users():
    user_id = session.get("user_id")
    
    if not user_id:
        return redirect(url_for("admin_login"))

    user = db.session.get(User,user_id)

    if not user or user.role not in ["super_admin", "user_admin"]:
        return "دسترسی غیرمجاز", 403
    
    users = User.query.all()
    return render_template("check_users.html" , users=users)

@app.route("/admin/products")
def admin_products():
        
    user_id = session.get("user_id")
    
    if not user_id:
        return redirect(url_for("admin_login"))

    user = db.session.get(User,user_id)

    if not user or user.role not in ["super_admin", "product_admin"]:
        return "دسترسی غیرمجاز", 403
    
    products = Product.query.all()
    main_categories_list = main_categories.query.all()
    sub_categories_list = sub_categories.query.all()
    return render_template(
        "check_products.html" ,
        products=products,
        main_categories_list=main_categories_list,
        sub_categories_list=sub_categories_list
        )

@app.route("/add_company" , methods=["GET", "POST"])
def add_company():
    if request.method == "POST":
        name = request.form["name"]
        owner = request.form["owner"]
        adress = request.form["adress"]
        telephone = request.form["telephone"]
        
        new_company = Company(
            name = name,
            owner = owner,
            adress = adress,
            telephone = telephone
        )
        db.session.add(new_company)
        db.session.commit()   
     
    companies = Company.query.all()
    return render_template("add_company.html" , companies = companies)  

# صفحه ی فاکتور فروش 
@app.route("/selling_factor" , methods=["GET", "POST"]) 
def sellingFactor():

    users = User.query.all()
    products = Product.query.all()

    selling_factors = []

    if request.method == "POST":

        user_id = request.form.get("user_id")

        selling_factors = selling_factor.query.filter_by(
            User_id=user_id
        ).all()

    return render_template( "selling_factor.html" , users=users , products=products , selling_factors=selling_factors)

# اضافه کردن به دیتابیس
@app.route("/add_selling_factor" , methods=["GET", "POST"])
def addSellingFactor():
    user_id = request.form.get("user_id")
    product_id = request.form.get("product_id")
    price = request.form.get("price")
    quantity = request.form.get("quantity")
    
    new_factor = selling_factor(
        User_id=user_id,
        Product_id=product_id,
        price=price,
        quantity=quantity
    )
    
    db.session.add(new_factor)
    db.session.commit()
    
    return redirect(url_for("sellingFactor"))  
    
    
@app.route("/buying_factor" , methods=["GET", "POST"])
def buyingFactor():
    companies = Company.query.all()
    products = Product.query.all()
    
    buying_factors = []
    
    if request.method == "POST":
    
        company_id = request.form.get("company_id")

        buying_factors = buying_factor.query.filter_by( Company_id = company_id ).all()
    
    return render_template( "buying_factor.html", products=products , companies=companies, buying_factors=buying_factors)

@app.route("/add_buying_factor" , methods=["GET", "POST"])
def addBuyingFactor():
    company_id = request.form.get("company_id")
    product_id = request.form.get("product_id")
    price = request.form.get("price")
    quantity = request.form.get("quantity")
    
    new_factor = buying_factor(
        Company_id=company_id,
        Product_id=product_id,
        price=price,
        quantity=quantity
    )
    
    db.session.add(new_factor)
    db.session.commit()
    
    return redirect(url_for("buyingFactor")) 
  
@app.route("/aboutMe")
def a_me():
    return render_template('about_me.html')

# پشتیبانی
@app.route("/support", methods=["GET", "POST"])
def support():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    if request.method == "POST":

        message = request.form.get("message")

        if not message:
            return "لطفاً پیام خود را وارد کنید."

        new_message = SupportMessage(
            user_id=user_id,
            message=message
        )

        db.session.add(new_message)
        db.session.commit()

        return redirect(url_for("support"))

    messages = SupportMessage.query.filter_by( user_id=user_id ).order_by( SupportMessage.created_at ).all()
    return render_template( "support.html", messages=messages )

@app.route("/admin/support_chat")
def admin_support():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("admin_login"))

    current_user = db.session.get(User, user_id)

    if not current_user or current_user.role not in ["super_admin", "chat_admin"]:
        return "دسترسی غیرمجاز", 403

    messages = SupportMessage.query.order_by(SupportMessage.created_at.desc()).all()
    # این برای مرتب بودن بر اساس زمان 

    return render_template("admin_support.html", messages=messages, sender="user" )

@app.route("/admin/support/reply/<int:user_id>", methods=["POST"])
def admin_support_reply(user_id):

    admin_id = session.get("user_id")

    if not admin_id:
        return redirect(url_for("admin_login"))

    admin = db.session.get(User, admin_id)

    if not admin or admin.role not in ["super_admin", "chat_admin"]:
        return "دسترسی غیرمجاز", 403

    message = request.form.get("message")

    if not message:
        return "پیام خالی است."

    new_message = SupportMessage(
        user_id=user_id,
        message=message,
        sender="admin"
    )

    db.session.add(new_message)
    db.session.commit()

    return redirect( url_for("admin_support_chat", user_id=user_id))

@app.route("/admin/support_chat/<int:user_id>")
def admin_support_chat(user_id):

    admin_id = session.get("user_id")

    if not admin_id:
        return redirect(url_for("admin_login"))

    admin = db.session.get(User, admin_id)

    if not admin or admin.role not in ["super_admin", "chat_admin"]:
        return "دسترسی غیرمجاز", 403

    user = db.session.get(User, user_id)

    if not user:
        return "کاربر پیدا نشد", 404

    messages = SupportMessage.query.filter_by(
        user_id=user_id
    ).order_by(
        SupportMessage.created_at.asc()
    ).all()

    return render_template("admin_support_chat.html", user=user,messages=messages)
    
@app.route("/comments", methods=["GET", "POST"])
def comments():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    if request.method == "POST":

        comment_text = request.form.get("comment")

        if not comment_text:
            return "لطفاً نظر خود را وارد کنید."

        new_comment = Comment(
            user_id=user_id,
            comment=comment_text
        )

        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for("comments"))

    comments = Comment.query.filter_by(is_approved=True ).order_by(Comment.created_at.desc() ).all()

    return render_template(  "comment.html",  comments=comments  )

@app.route("/admin/comment_chat")
def admin_comment():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("admin_login"))

    current_user = db.session.get(User, user_id)

    if not current_user or current_user.role not in ["super_admin", "chat_admin"]:
        return "دسترسی غیرمجاز", 403

    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    # این برای مرتب بودن بر اساس زمان 

    return render_template("admin_comment.html", comments=comments)

@app.route("/admin/comments/approve/<int:comment_id>")
def approve_comment(comment_id):

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("admin_login"))

    current_user = db.session.get(User, user_id)

    if not current_user or current_user.role not in ["super_admin", "chat_admin"]:
        return "دسترسی غیرمجاز", 403

    comment = db.session.get(Comment, comment_id)

    if not comment:
        return "نظر پیدا نشد", 404

    comment.is_approved = True

    db.session.commit()

    return redirect(url_for("admin_comment"))

@app.route("/admin/products/deactivate/<int:product_id>", methods=["POST"])
def deactivate_product(product_id):

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("admin_login"))

    current_user = db.session.get(User, user_id)

    if not current_user or current_user.role not in ["super_admin", "product_admin"]:
        return "دسترسی غیرمجاز", 403

    product = db.session.get(Product, product_id)

    if not product:
        return "محصول پیدا نشد", 404

    product.is_active = False

    db.session.commit()

    return redirect(url_for("admin_products"))


@app.route("/admin/products/activate/<int:product_id>", methods=["POST"])
def activate_product(product_id):

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("admin_login"))

    current_user = db.session.get(User, user_id)

    if not current_user or current_user.role not in ["super_admin", "product_admin"]:
        return "دسترسی غیرمجاز", 403

    product = db.session.get(Product, product_id)

    if not product:
        return "محصول پیدا نشد", 404

    product.is_active = True

    db.session.commit()

    return redirect(url_for("admin_products"))

@app.route('/admin/orders')
def check_orders():

    # 1. بررسی ورود ادمین
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('admin_login'))

    # 2. پیدا کردن کاربر فعلی
    current_user = db.session.get(User, user_id)

    if not current_user:
        return "کاربر پیدا نشد", 404

    # 3. بررسی دسترسی
    if current_user.role not in ['super_admin', 'order_admin']:
        return "دسترسی غیرمجاز", 403

    # 4. گرفتن همه سفارش‌ها
    orders = Order.query.order_by(  Order.created_at.desc() ).all()

    # 5. فرستادن سفارش‌ها به صفحه
    return render_template( 'check_orders.html', orders=orders)

@app.route('/admin/orders/<int:order_id>' ,  methods=["POST"])
def order_detail(order_id):
    
    order = db.session.get(Order , order_id)
    
    if not order:
        return "سفارش پیدا نشد", 404
    
    items = OrderItem.query.filter_by(order_id=order.id).all()
    
    return render_template("order_detail.html", order=order, items=items)
@app.route('/admin/inventory')
def admin_inventory():

    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('admin_login'))

    current_user = db.session.get(User, user_id)

    if not current_user:
        return "کاربر پیدا نشد", 404

    if current_user.role not in ['super_admin', 'order_admin']:
        return "دسترسی غیرمجاز", 403

    products = Product.query.order_by(Product.name.asc()).all()

    return render_template( 'admin_inventory.html',  products=products )

    

if __name__ == '__main__':
    app.run(debug=False)

# 1- وقتی در سبد خرید روی روی پرداخت کلیک میکنم یه اروری میاره (Method Not Allowed
# The method is not allowed for the requested URL.)

# 2-باید قسمت orders را هم درست کنم در ادمین پنل 

# 3- باید اگه چیزی انجام شد مثل اضافه شدن به سبد خرید یه پیام از گوشه ای از صفحه بیاد بیرون 

# چطور 404 را در پایتون فلاسم هندل کنیم 