import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required,
)
from models.item import ItemModel

BLANK_ERROR = "This {} cannot be left blank!"
ITEM_NOT_FOUND = "Item: {} not found"
NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
NOT_FOUND = "{} doesn't exist!"
ITEM_DELETED =  "{} deleted"

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help=BLANK_ERROR.format("price")
    )
    parser.add_argument(
        "store_id", type=int, required=True, help=BLANK_ERROR.format("store_id")
    )

    @classmethod
    @jwt_required
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": ITEM_NOT_FOUND.format(name)}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str):
        if ItemModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured while inserting item."}, 500

        return item.json(), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Admin privilege required!"}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED.format(name)}
        return {"message": NOT_FOUND.format(name)}
    
    @classmethod
    def put(cls, name: str):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):

    """
    jwt_optional can be use to capture user_id 
    and also show different data for authorized
    and unauthorized users.
    """

    @classmethod
    @jwt_optional
    def get(cls):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        # items = list(map(lambda x: x.json(), ItemModel.find_all()))
        if user_id:
            return {"items": items}, 200
        return (
            {
                "items": [item["name"] for item in items],
                "message": "Please to login to view item detail",
            },
            200,
        )
