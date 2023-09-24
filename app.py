from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, Restaurant_pizzas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return make_response(jsonify({"msg": "Welcome to Pizzas api"}), 200)

#Get Rstaurants
@app.route("/Restaurants")
def Restaurants():
    Restaurants = [Restaurant.to_dict() for Restaurant in Restaurant.query.all()]
    return make_response(jsonify({"Restaurants": Restaurants}), 200)

# Get Restaurants by id
@app.route("/Restaurants/<int:id>")
def Restaurants_by_id(id):
    Restaurants = Restaurant.query.filter_by(id=id).first()
    if not Restaurant:
        return make_response(jsonify({"error": "Restaurant not found"}), 404)
    else:
        return make_response(jsonify(Restaurant.to_dict()), 200)

# get Pizza
@app.route("/Pizza")
def Pizza():
    Pizza = [Pizza.to_dict() for Pizza in Pizza.query.all()]
    return make_response(jsonify({"Pizza": Pizza}), 200)   

# get Pizza by id
@app.route("/Pizza/<int:id>", methods=["GET", "PATCH"])
def Pizza_by_id(id):
    Pizza = Pizza.query.filter_by(id=id).first()
    if not Pizza:
        return make_response(jsonify({"error": "Pizza not found"}), 404)
    else:
        if request.method == "GET":
            return make_response(jsonify(Pizza.to_dict()), 200)
        
        # update description
        elif request.method == "PATCH":
            description = request.form.get("description")
            if description and len(description) < 20:
                return make_response(jsonify({"error":"[validation errors]"}), 400)
            
            setattr(Pizza, "description", description)
            db.session.add(Pizza)
            db.session.commit()
            return make_response(jsonify(Pizza.to_dict()), 200)

# post Restaurant_pizzas
@app.route("/Restaurant_pizzas", methods=["POST"])
def create_Restaurant_pizzas():
        
        if request.method == "POST":
        
            if request.form.get("price") not in ["High", "Low", "Average"]:
                return make_response(jsonify({"errors": ["validation errors"]}),400)
            
            
            price = request.form.get("price")
            Pizza_id = request.form.get("Pizza_id")
            Restaurant_id =  request.form.get("Restaurant_id")

            new_Restaurant_pizzas = Restaurant_pizzas.insert().values(
                price = price ,
                Pizza_id= Pizza_id,
                Restaurant_id = Restaurant_id,
            )
            db.session.execute(Restaurant_pizzas)
            db.session.commit()
            

            updated_Restaurant = Restaurant.query.filter_by(id=Restaurant_id).first()
            response_data = {
                "id": Pizza.id,
                "name": Pizza.name,
                "ingredients": Pizza.ingredients,
            }

            return make_response(jsonify(response_data), 201)

if __name__ == '__main__':
    app.run(port=5555)