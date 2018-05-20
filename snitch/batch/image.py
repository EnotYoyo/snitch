import os
import uuid

import werkzeug
from flask import jsonify, send_from_directory, make_response
from flask_restful import Resource, reqparse, abort
from snitch import models, db, app


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']


class Image(Resource):
    def __init__(self):
        self.post_parse = reqparse.RequestParser()
        self.post_parse.add_argument('file', type=werkzeug.FileStorage, location='files')

        self.get_parse = reqparse.RequestParser()
        self.get_parse.add_argument('filename', type=str, location='json')
        super(Image, self).__init__()

    def get(self):
        args = self.get_parse.parse_args()
        return send_from_directory(app.config['UPLOAD_FOLDER'], args['filename'])

    def post(self):
        args = self.post_parse.parse_args()

        if args['file'] is None:
            abort(400)

        file = args['file']
        if file.filename == '':
            abort(400)

        if not file or not allowed_file(file.filename):
            abort(400)

        extension = file.filename.rsplit('.', 1)[1].lower()
        filename = "{}.{}".format(uuid.uuid4(), extension)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return make_response(jsonify(dict(filename=filename)), 201)
