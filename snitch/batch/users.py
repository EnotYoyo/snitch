import base64

from flask import jsonify, current_app
from sqlalchemy import or_
from flask_restful import Resource, reqparse, abort
from snitch import models, db
from snitch.snark import snark


class Users(Resource):
    def __init__(self):
        self.post_parse = reqparse.RequestParser()
        self.post_parse.add_argument("login", type=str, location="json", required=True)
        # todo: change to vk_token(str) and get vk_id from vk.com with vk_token
        self.post_parse.add_argument("vk_id", type=int, location="json", required=True)
        self.post_parse.add_argument("hash", type=str, location="json", required=True)
        super(Users, self).__init__()

    def post(self):
        args = self.post_parse.parse_args()

        # check if exist abort
        user = models.User.query.filter(or_(models.User.login == args["login"],
                                            models.User.vk_id == args["vk_id"],
                                            models.User.hash == args["hash"])).first()
        if user is not None:
            abort(409)

        # create new object
        user = models.User(login=args["login"], vk_id=args["vk_id"], hash=args["hash"])
        db.session.add(user)
        db.session.commit()

        tree = snark.MerkleTree(current_app.config["TREE"], current_app.config["TREE_INDEX"])
        tree.add(base64.b64encode(args["hash"].encode('utf-8')))
        return jsonify(user.serialize, 201)
