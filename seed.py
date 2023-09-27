from random import randint, choice as rc
from faker import Faker
from models import db, Restaurant, Pizza, Restaurant_pizza
from app import app

fake = Faker()

with app.app_context():

    Restaurant.query.delete()
    Pizza.query.delete()
    Restaurant_pizza.query.delete()

    pizzas = []
    for n in range(25):
        p = Pizza(name=fake.name(), ingredients=fake.name())  
        pizzas.append(p)

    db.session.add_all(pizzas)

    restaurants = []
    for i in range(25):
        r = Restaurant(name=fake.company(), address=fake.address())
        restaurants.append(r)

    db.session.add_all(restaurants)    

    restaurant_pizzas = []
    for i in range(30):
        rp = Restaurant_pizza(price=randint(1, 30), pizza_id=randint(1, 10), restaurant_id=randint(1, 10))
        restaurant_pizzas.append(rp)

    db.session.add_all(restaurant_pizzas)   

    db.session.commit()