from flask_sqlalchemy import SQLAlchemy
from .app import app

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

with app.app_context():
    db.create_all()
