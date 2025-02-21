from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройки базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель данных
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Создание базы данных при первом запуске
with app.app_context():
    db.create_all()

# Главная страница со списком продуктов
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Добавление продукта
@app.route('/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    if name and quantity:
        product = Product(name=name, quantity=int(quantity))
        db.session.add(product)
        db.session.commit()
    return redirect(url_for('index'))

# Удаление продукта
@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_quantity = request.form.get('quantity')
        
        if new_name and new_quantity:
            product.name = new_name
            product.quantity = int(new_quantity)
            db.session.commit()
            return redirect(url_for('index'))
    
    return render_template('edit.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
