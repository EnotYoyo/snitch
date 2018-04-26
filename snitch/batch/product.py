from flask import jsonify
from flask_restful import Resource, reqparse, abort
from snitch import models, db


class Products(Resource):
    def __init__(self):
        self.get_parse = reqparse.RequestParser()
        self.get_parse.add_argument("count", type=int, default=10, location="json")
        self.get_parse.add_argument("offset", type=int, default=0, location="json")

        self.post_parse = reqparse.RequestParser()
        self.post_parse.add_argument("name", type=str, location="json", required=True)
        self.post_parse.add_argument("description", type=str, location="json", required=True)
        super(Products, self).__init__()

    def get(self):
        args = self.get_parse.parse_args()
        products = models.Product.query.limit(args["count"]).offset(args["offset"])
        return jsonify(products=[i.serialize for i in products.all()])

    def post(self):
        args = self.post_parse.parse_args()

        # check if exist abort
        product = models.Product.query.filter((models.Product.name == args["name"])).first()
        if product is not None:
            abort(409)

        # create new object
        product = models.Product(name=args["name"], description=args["description"])
        db.session.add(product)
        db.session.commit()
        return jsonify(product.serialize, 201)
