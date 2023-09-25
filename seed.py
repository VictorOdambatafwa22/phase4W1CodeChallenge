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

    restaurant_pizzas = []
    prices = [10, 20, 35, 18, 41, 29, 13]

    for n in range(25):
        e = Restaurant_pizza(price=rc(prices))
        restaurant_pizzas.append(e)

    db.session.add_all(restaurant_pizzas)

    restaurants = []
    address = ['Lion', 'Tiger', 'Bear', 'Hippo', 'Rhino', 'Elephant', 'Ostrich',
        'Snake', 'Monkey']

    for n in range(200):
        name = fake.first_name()
        while name in [a.name for a in restaurants]:
            name=fake.first_name()
        a = Restaurant(name=name, address=rc(address))
        a.pizza = rc(pizzas)
        a.restaurant_pizza = rc(restaurant_pizzas)
        restaurants.append(a)