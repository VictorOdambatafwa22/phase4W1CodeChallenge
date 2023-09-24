from random import randint, choice as rc
from faker import Faker
from models import db, Restaurant, Pizza, Restaurant_pizzas
from app import app

fake = Faker()


with app.app_context():
    Restaurant.query.delete()
    Pizza.query.delete()

    Restaurants = []
    for i in range(50):
        Restaurant = Restaurant(
          name= fake.name(),
          super_name = fake.first_name(),  
        )
        Restaurant.append(Restaurant)
    db.session.add_all(Restaurants)

    Pizza = []
    for i in range(50):
        Pizza = Pizza(
            name = fake.name(),
            description = fake.paragraph()
        )
        Pizza.append(Pizza)
    db.session.add_all(Pizza)

    combinations = set()
    price = ["High", "Low", "Average"]
    for _ in range(50):
        Restaurant_id = randint(1, 50)
        Pizza_id = randint(1, 50)
        price = rc(price)

        if (Restaurant_id, Pizza_id, price) in combinations:
            continue
        combinations.add((Restaurant_id, Pizza_id, price))
        Restaurant_pizzas_data = {"Restaraunt_id": Restaurant_id, "Pizza_id": Pizza_id, "price": price}
        statement = db.insert(Restaurant_pizzas).values(Restaurant_pizzas_data)
        db.session.execute(statement)
        db.session.commit()
    db.session.commit()