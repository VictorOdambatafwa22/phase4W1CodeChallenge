from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()


Restaurant_pizzas = db.Table(
    "Restaurant_pizzas",
    db.Column("Restaurant_id", db.ForeignKey("Restaurant.id"), primary_key=True),
    db.Column("Pizza_id", db.ForeignKey("Pizza.id"), primary_key=True),
    db.Column("Price", db.String),
    db.Column("created_at", db.DateTime, server_default=db.func.now()),
    db.Column("updated_at", db.DateTime, onupdate=db.func.now())
)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'Restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    super_name= db.Column(db.String)
    created_at= db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    Pizza = db.relationship("Pizza", secondary=Restaurant_pizzas, back_populates="Restaurants")
    serialize_rules = ("-Pizza.Restaurants",)

    def __repr__(self):
        return f"Restaurants {self.name} has {self.super_name}."
    

class Pizza(db.Model, SerializerMixin):
    __tablename__ = "Pizza"

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    description= db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    Restaurant = db.relationship("Restaurant", secondary=Restaurant_pizzas, back_populates="pizza")
    serialize_rules = ("-Restaurant.pizza",)

    def __repr__(self):
        return f"Pizza {self.name} was created at {self.created_at}."