from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Restaurant_pizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas',)

    id = db.Column(db.Integer(), primary_key=True)
    pizza_id = db.Column(db.Integer(), ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer(), ForeignKey('restaurants.id'))
    price = db.Column(db.Integer())
    created_at= db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    restaurants = relationship('Book', back_populates='restaurant_pizzas')
    pizza = relationship('Pizza', back_populates='restaurant_pizzas')

    def __repr__(self):

        return f'Restaurant_pizza(id={self.id}'
         

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    address= db.Column(db.String)

    restaurant_pizzas = relationship('Restaurant_pizza', back_populates='restaurant')
    serialize_rules = ('-restaurant_pizzas.restaurant',)

    def __repr__(self):
        return f'Restaurants {self.name}'
    

class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    ingredients= db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurant_pizzas = relationship('Restaurant_pizza', back_populates='pizza')
    serialize_rules = ('-restaurant_pizzas.pizza',)

    def __repr__(self):
        return f'Pizza {self.name}'