from flask import jsonify
from flask_restful import Resource, reqparse, abort
from snitch import models, db


class Reviews(Resource):
    def __init__(self):
        self.get_parse = reqparse.RequestParser()
        self.get_parse.add_argument("count", type=int, default=10, location="json")
        self.get_parse.add_argument("offset", type=int, default=0, location="json")

        self.post_parse = reqparse.RequestParser()
        self.post_parse.add_argument("product_id", type=int, location="json", required=True)
        self.post_parse.add_argument("review", type=str, location="json", required=True)
        super(Reviews, self).__init__()

    def get(self):
        args = self.get_parse.parse_args()
        reviews = models.Review.query.limit(args["count"]).offset(args["offset"])
        return jsonify(reviews=[i.serialize for i in reviews.all()])

    def post(self):
        args = self.post_parse.parse_args()

        # create new object
        review = models.Review(product_id=args["product_id"], review=args["review"])
        db.session.add(review)
        db.session.commit()
        return jsonify(review.serialize, 201)
