import os

from flask import jsonify, make_response
from flask_restful import Resource, reqparse, abort
from sqlalchemy import func

from snitch import models, db, app


class Products(Resource):
    def __init__(self):
        self.get_parse = reqparse.RequestParser()
        self.get_parse.add_argument("count", type=int, default=10, location="json")
        self.get_parse.add_argument("offset", type=int, default=0, location="json")
        self.get_parse.add_argument("category", type=str, default=None, location="json")
        self.get_parse.add_argument("top", type=bool, default=False, location="json")

        self.post_parse = reqparse.RequestParser()
        self.post_parse.add_argument("name", type=str, location="json", required=True)
        self.post_parse.add_argument("description", type=str, location="json", required=True)
        self.post_parse.add_argument("image", type=str, location="json")
        self.post_parse.add_argument("category", type=str, location="json", required=True)
        self.categories = ("films", "books", "events", "people", "companies", "other")
        super(Products, self).__init__()

    def _top(self, args):
        if not args["category"] or args["category"] not in self.categories:
            abort(400)

        stmt = db.session.query(models.Review.product_id, func.count('*').label('reviews_count')).group_by(
            models.Review.product_id).subquery()

        products = db.session.query(models.Product).filter(
            models.Product.category == args["category"]). \
            outerjoin(stmt, models.Product.id == stmt.c.product_id).order_by(stmt.c.reviews_count.desc())
        products = products.limit(args["count"]).offset(args["offset"])

        return jsonify(products=[i.serialize for i in products.all()])

    def get(self):
        args = self.get_parse.parse_args()

        if args["top"]:
            return self._top(args)

        products = models.Product.query
        if args["category"] is not None and args["category"] in self.categories:
            products = products.filter(models.Product.category == args["category"])
        products = products.limit(args["count"]).offset(args["offset"])

        return jsonify(products=[i.serialize for i in products.all()])

    def post(self):
        args = self.post_parse.parse_args()

        if args["category"] not in self.categories:
            abort(400)

        # check if exist abort
        product = models.Product.query.filter((models.Product.name == args["name"])).first()
        if product is not None:
            abort(409)

        image = None
        if args["image"] is not None and os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], args["image"])):
            image = args["image"]

        # create new object
        product = models.Product(name=args["name"], description=args["description"], image=image,
                                 category=args["category"])
        db.session.add(product)
        db.session.commit()
        return make_response(jsonify(product.serialize), 201)
