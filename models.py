from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Restaurant_pizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    #serialize_rules = ('-restaurant', '-pizza','-restaurant_pizzas')

    id = db.Column(db.Integer(), primary_key=True)
    pizza_id = db.Column(db.Integer(), db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer(), db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer())
    created_at= db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    

    @validates("price")
    def validate_price(self, key, price):
        if isinstance(price, int) and (price >= 1 and price <= 30):
            return price
        else:
            raise ValueError("Must have a price between 1 and 30")
 

    def __repr__(self):

        return f'Restaurant_pizza(id={self.id}'
         

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    #serialize_rules = ('-restaurant_pizzas.restaurants',)
    #serialize_rules = ('-Pizza.restaurants',)

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String,unique=True)
    address= db.Column(db.String)

    pizzas = db.relationship(
        "Pizza", secondary="restaurant_pizzas", back_populates="restaurants"
    )

    @validates("name")
    def validate_name(self, key, name):
        if not len(name.strip().split(" ")) < 50:
            raise ValueError("Must have a name less than 50 words in length")
        restaurant = Restaurant.query.filter_by(name=name).first()
        if restaurant:
            raise ValueError("Name value must be unique")
        return name

    def __repr__(self):
        return f'Restaurants {self.name}'
    

   # serialize_rules = ('-restaurant_pizzas.pizza',)
class Pizza(db.Model):
    __tablename__ = 'pizzas'

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