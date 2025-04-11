from flask_sqlalchemy import SQLAlchemy
from ..app import app

db = SQLAlchemy(app)

class Contrant_card(db.Model):
    number = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime)
    price = db.Column(db.Float)
    customer = db.Column(db.Text)
    update_date = db.Column(db.DateTime)
    place_date = db.Column(db.DateTime)
    execute_date = db.Column(db.DateTime)
    penalty = db.Column(db.Boolean)

    provider_id = db.Column(db.ForeignKey('company.inn'))

    products = db.relationship("Product", backref = 'contract')

    def to_dict(self):
        return {
            'number': str(self.number),
            'date': self.date.strftime('%d.%m.%Y'),
            'price': self.price,
            'update_date': self.update_date.strftime('%d.%m.%Y') if self.update_date else None,
        }

class Company(db.Model):
    inn = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    phone = db.Column(db.Text)
    e_mail = db.Column(db.Text)
    addres = db.Column(db.Text)

    contrants = db.relationship("Contrant_card", backref = 'contract')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    search_name = db.Column(db.Text)
    country_producer = db.Column(db.Text)
    ktru = db.Column(db.Text)
    okpd_2 = db.Column(db.Text)
    type = db.Column(db.Text)
    measure = db.Column(db.Text)
    quantity = db.Column(db.Float)
    price = db.Column(db.Float)
    cost = db.Column(db.Float)
    tax = db.Column(db.Text)
    comment = db.Column(db.Text)

    contrant_card_id = db.Column(db.ForeignKey("contrant_card.number"))
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'search_name': self.search_name,
            'country_producer': self.country_producer,
            'ktru': self.ktru,
            'okpd_2': self.okpd_2,
            'type': self.type,
            'quantity': self.quantity,
            'measure': self.measure,
            'price': self.price,
            'cost': self.cost,
            'tax': self.tax,
            'contrant_card_id': str(self.contrant_card_id),
            'contrant_card_date': self.contract.date.strftime('%d.%m.%Y'),
            'comment': self.comment,
            'kkn_id': '1',
            'kkn_name': '1',
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    comment = db.Column(db.Text)
    okpd_2_id = db.Column(db.Integer, db.ForeignKey('okpd_2.id'))
    ktru_id = db.Column(db.Integer, db.ForeignKey('ktru.id'))
    sub_categories = db.relationship('SubCategory', backref='category', lazy='joined')
    characteristics = db.relationship('Characteristic', backref='category', lazy=True)
    product_part_id = db.Column(db.Integer, db.ForeignKey('product_part.id'))

    def __repr__(self):
        return f'<Category {self.name}>'

class Characteristic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    type = db.Column(db.Text) # min_max/one/list
    measure = db.Column(db.Text)
    comment = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    values = db.relationship('Value', backref='characteristic', lazy=True)
    sub_categories = db.relationship('SubCategoryCharacteristic', backref='characteristic', lazy='joined')

class ProductPart(db.Model):
    __tablename__ = "product_part"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.Text)
    comment = db.Column(db.Text)
    categories = db.relationship('Category', backref='product_part', lazy=True)

class Value(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    comment = db.Column(db.Text)
    characteristic_id = db.Column(db.Integer, db.ForeignKey('characteristic.id'))
    characteristics = db.relationship('SubCategoryCharacteristic', backref='value', lazy='joined')
    def __str__(self):
        return f"Value(id={self.id}, name={self.name}, comment={self.comment})"

class okpd_2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    number = db.Column(db.Text)
    is_final = db.Column(db.Boolean)
    comment = db.Column(db.Text)
    parent_okpd_id = db.Column(db.Integer, db.ForeignKey('okpd_2.id'))
    sub_categories = db.relationship('Category', backref='okpd_2', lazy=True)

class SubCategory(db.Model):
    '''ККН'''
    __tablename__ = 'subcategory'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=True)
    name = db.Column(db.Text, nullable=True)
    code = db.Column(db.Text, nullable=True)
    measure = db.Column(db.Text, nullable=True)
    kkn_code = db.Column(db.Text, nullable=True)
    actualization_date = db.Column(db.DateTime, nullable=True)
    russian = db.Column(db.Boolean, default=None)
    comment = db.Column(db.Text)
    characteristics = db.relationship('SubCategoryCharacteristic', backref='subcategory', lazy='joined')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    ktru_id = db.Column(db.Integer, db.ForeignKey('ktru.id'))

class SubCategoryCharacteristic(db.Model):
    __tablename__ = 'sub_category_characteristic'
    sub_category_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), primary_key=True)
    characteristic_id = db.Column(db.Integer, db.ForeignKey('characteristic.id'), primary_key=True)
    value_id = db.Column(db.Integer, db.ForeignKey('value.id'), primary_key=True, nullable=True)
    min = db.Column(db.Float, nullable=True)
    max = db.Column(db.Float, nullable=True)
    comment = db.Column(db.Text, nullable=True)

class Ktru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    number = db.Column(db.Text)
    comment = db.Column(db.Text)
    sub_categories = db.relationship('SubCategory', backref='ktru', lazy=True)
    categories = db.relationship('Category', backref='ktru', lazy=True)
    # ktru_parent = db.Column(db.Integer, db.ForeignKey('ktru.id'))
    # ktru_chars = db.relationship('KtruChar', backref='ktru', lazy=True)


with app.app_context():
    db.create_all()
