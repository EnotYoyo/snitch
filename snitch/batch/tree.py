import base64
import binascii

from flask import jsonify, current_app, request
from flask_restful import abort
from snitch import app
from snitch.snark import snark


@app.route("path", methods=["GET"])
def get_tree_path():
    user_hash = request.args.get('hash', type=str, default=None)
    if not user_hash:
        abort(400)

    try:
        user_hash = base64.b64decode(user_hash.encode('utf-8'))
    except binascii.Error:
        abort(400)

    tree = snark.MerkleTree(current_app.config["TREE"], current_app.config["TREE_INDEX"])
    if not tree.check(user_hash):
        abort(404)

    path = tree.get_path(user_hash)
    return jsonify({"path": base64.b64encode(path).decode("utf-8")})
