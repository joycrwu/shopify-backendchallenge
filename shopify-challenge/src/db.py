from flask_sqlalchemy import SQLAlchemy
import requests
import os

db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    warehouses = db.relationship("Warehouse", cascade="delete")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "warehouses": [w.sub_serialize() for w in self.warehouses]
            }
    
    def sub_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Warehouse(db.Model):
    __tablename__ = "warehouse"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))

    def __init__(self, **kwargs):
        self.location = kwargs.get("location")

    def serialize(self):
        return {
            "id": self.id,
            "location": self.location,
            "item": self.item_id
        }
    def sub_serialize(self):
        return {
            "id": self.id,
            "location": self.location
        }
