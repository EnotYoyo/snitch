from snitch import app
from snitch.batch import product
from flask_restful import Api


api = Api(app, prefix="/")
api.add_resource(product.Product, 'products/<int:product_id>')
api.add_resource(product.Products, 'products')
