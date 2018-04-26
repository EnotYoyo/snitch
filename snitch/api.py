from snitch import app
from snitch.batch import product, review
from flask_restful import Api


api = Api(app, prefix="/")
api.add_resource(product.Products, 'products')
api.add_resource(review.Reviews, 'reviews')
