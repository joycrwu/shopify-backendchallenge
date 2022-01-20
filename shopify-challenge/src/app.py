import json
import os
from db import db
from flask import Flask
from db import Item
from db import Warehouse
from flask import request

app = Flask(__name__)
db_filename = "shopify.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code

@app.route("/api/items/")
def get_all_items():
    items = Item.query.all()
    return success_response({"items": [i.serialize() for i in items]})

@app.route("/api/items/", methods=["POST"])
def create_item():
    body = json.loads(request.data)
    name = body.get("name")
    if name is None: 
        return failure_response("Item has no name!", 400)
    item = Item(name=name)
    db.session.add(item)
    db.session.commit()
    return success_response(item.serialize(), 201)

@app.route("/api/items/<int:item_id>/")
def get_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
        return failure_response("Item not found!")
    else:
        return success_response(item.serialize(), 200)

@app.route("/api/items/<int:item_id>/", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
        return failure_response("Item not found!")
    db.session.delete(item)
    db.session.commit()
    return success_response(item.serialize(), 200)

@app.route("/api/items/<int:item_id>/warehouse/", methods=["POST"])
def create_warehouse(item_id):
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
        return failure_response("Item not found!")
    body = json.loads(request.data)
    location = body.get("location")
    if location is None:
        return failure_response("Location not found!")
    new_warehouse = Warehouse(location=location)
    item.warehouses.append(new_warehouse)
    db.session.add(new_warehouse)
    db.session.commit()
    warehouse_response = new_warehouse.serialize()
    warehouse_response["item"] = item.sub_serialize()
    return success_response(warehouse_response, 201)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
