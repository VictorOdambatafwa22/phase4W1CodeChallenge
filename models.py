from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Restaurant_pizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas',)

    id = db.Column(db.Integer(), primary_key=True)
    pizza_id = db.Column(db.Integer(), db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer(), db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer())
    created_at= db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
 

    def __repr__(self):

        return f'Restaurant_pizza(id={self.id}'
         

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    address= db.Column(db.String)

    pizzas = db.relationship(
        "Pizza", secondary="restaurant_pizzas", back_populates="restaurants"
    )

    def __repr__(self):
        return f'Restaurants {self.name}'
    

class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    ingredients= db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurants = db.relationship(
        "Restaurant", secondary="restaurant_pizzas", back_populates="pizzas"
    )

    def __repr__(self):
        return f'Pizza {self.name}'