from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
#from flask_restful import Resource,Api
from models import db, Restaurant, Pizza, Restaurant_pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return make_response(
        jsonify({"msg":"Pizza Restaurant"}), 200)


@app.route("/restaurants")
def Restaurants():
    restaurants = [{
            "id":restaurant.id,
            "name":restaurant.name,
            "address":restaurant.address,
        } for restaurant in Restaurant.query.all()]
    return make_response(jsonify({"Restaurants": restaurants}), 200)

            
@app.route("/pizzas")
def pizza():
    pizzas = [{
            "id":pizza.id,
            "name":pizza.name,
            "ingredients":pizza.ingredients,           
        } for pizza in Pizza.query.all()]
    return make_response(jsonify({"Pizzas": pizzas}), 200)

@app.route("/restaurants/<int:id>",methods=["GET", "DELETE"])
def restaurant_view(id):
    if request.method =="GET":
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            pizzas = [{"id": pizza.id, "name": pizza.name, "ingredients": pizza.ingredients} for pizza in restaurant.pizzas]
            response = {
                "id":restaurant.id,
                "name":restaurant.name,
                "address":restaurant.address,
                "pizzas": pizzas
            }
            return make_response(jsonify(response), 200 )
        else: 
            return make_response(jsonify({"error": "Restaurant not found"}), 404 )
   
    elif request.method =="DELETE":
        restaurant = Restaurant.query.filter_by(id=id).first() 
        if restaurant:
            Restaurant_pizza.query.filter_by(restaurant_id=id).delete()
            db.session.delete(restaurant)
            db.session.commit()
            return make_response("", 204 )
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404 )




@app.route("/restaurant_pizzas", methods=["GET", "POST"])
def restaurant_pizaas_view():
    if request.method =="GET":
        restaurants_pizzas = [{
            "id":restaurantpizza.id,
            "price":restaurantpizza.price,
            "pizza_id":restaurantpizza.pizza_id,
            "restaurant_id":restaurantpizza.restaurant_id,
            "created_at":str(restaurantpizza.created_at),
            "updated_at":str(restaurantpizza.updated_at),
        } for restaurantpizza in Restaurant_pizza.query.all()]
        return make_response(jsonify({"Restaurants_pizzas": restaurants_pizzas}), 200)
    elif request.method =="POST":
        try:
            data = request.get_json()
            rp = Restaurant_pizza(
                price=data["price"],
                pizza_id=data["pizza_id"],
                restaurant_id=data["restaurant_id"]
            )
            db.session.add(rp)
            db.session.commit()
            pizza = Pizza.query.filter_by(id=data["pizza_id"]).first()
            pizza_dict = {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            }

            response = make_response(jsonify(pizza_dict), 201)

            return response
        except ValueError as e:
            response = make_response(jsonify({"errors": e.args}), 400)
            return response
        except Exception as e:
            response = make_response(jsonify({"errors": e.args}), 400)
            return response

   
if __name__ == '__main__':
    app.run(port=5555,debug=True)
