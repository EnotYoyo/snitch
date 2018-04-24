from snitch import app, product
from flask_restful import Api


api = Api(app, prefix="/")
api.add_resource(product.Product, 'product/<int:product_id>')
