import base64
import binascii
import datetime

from flask import jsonify, current_app, abort, json
from flask_restful import Resource, reqparse
from snitch import models, db
from snitch.snark import snark


class Reviews(Resource):
    def __init__(self):
        self.get_parse = reqparse.RequestParser()
        self.get_parse.add_argument("product_id", type=int, location="json", required=True)
        self.get_parse.add_argument("count", type=int, default=10, location="json")
        self.get_parse.add_argument("offset", type=int, default=0, location="json")

        self.post_parse = reqparse.RequestParser()
        self.post_parse.add_argument("product_id", type=int, location="json", required=True)
        self.post_parse.add_argument("review", type=str, location="json", required=True)
        self.post_parse.add_argument("review_id", type=str, location="json", required=True)
        self.post_parse.add_argument("review_sig", type=str, location="json", required=True)
        self.post_parse.add_argument("snark", type=str, location="json", required=True)
        self.post_parse.add_argument("tree_root", type=str, location="json", required=True)
        super(Reviews, self).__init__()

    def get(self):
        args = self.get_parse.parse_args()
        reviews = models.Review.query.filter(models.Review.product_id == args["product_id"])\
            .limit(args["count"]).offset(args["offset"])
        return jsonify(reviews=[i.serialize for i in reviews.all()])

    def post(self):
        args = self.post_parse.parse_args()

        try:
            zk_snark = base64.b64decode(args['snark'].encode('utf-8'))
            tree_root = base64.b64decode(args['tree_root'].encode('utf-8'))
            review_id = base64.b64decode(args['review_id'].encode('utf-8'))
            review_sig = base64.b64decode(args['review_sig'].encode('utf-8'))
        except binascii.Error:
            abort(400)
            return  # for pycharm static analyzer error :(

        verifier = snark.Verifier(current_app.config["VERIFICATION_KEY"])
        success, description = verifier.verify_snark(zk_snark,
                                                     tree_root,
                                                     str(args["product_id"]),
                                                     args["review"],
                                                     review_id,
                                                     review_sig)

        if not success:
            abort(400, description)

        # fixme!
        # exist_root = models.Root.query.filter(models.Root.hash == tree_root).first()
        # if not exist_root:
        #     abort(400, "Root not found")

        # create new object
        review = models.Review(id=review_id, product_id=args["product_id"], review=json.loads(args["review"])["review"])
        db.session.add(review)
        db.session.commit()
        return jsonify(review.serialize, 201)
