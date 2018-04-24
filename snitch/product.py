from flask_restful import Resource


class Product(Resource):
    def get(self, product_id):
        return "hello, product " + str(product_id)
