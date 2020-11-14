from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from base_datos import db

from models.label import LabelModel
from models.category import CategoryModel
from models.subcategory import SubCategoryModel
from models.producttype import ProductTypeModel
from models.mark import MarkModel
from models.product import ProductModel

from controllers.label import LabelsController,LabelController
from controllers.mark import MarksController, MarkController
from controllers.product import ProductsController, ProductController

from controllers.category import CategoriesController, CategoryController
from controllers.subcategory import SubCategoriesController, SubCategoryController
from controllers.producttype import ProductTypeController, ProductTypesController


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://x4kvh5za35254lsa:qhokt2eflmcfee9m@sp6xl8zoyvbumaa2.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/lb8cwbrcgy5fhx0u';

api = Api(app=app)

@app.before_first_request
def iniciador():
    db.init_app(app)
    # db.drop_all()
    db.create_all(app=app)
    

@app.route('/')
def inicio():
    return 'Api Tienda Virtual - 200', 200


#Creacion de rutas

api.add_resource(LabelsController, '/label')
api.add_resource(LabelController, '/label/<int:labelId>')
api.add_resource(MarksController, '/mark')
api.add_resource(MarkController, '/mark/<int:markId>')
api.add_resource(ProductsController, '/product')
api.add_resource(ProductController, '/product/<int:productId>') 

api.add_resource(CategoriesController, '/category')
api.add_resource(CategoryController, '/category/<int:categoryId>')
api.add_resource(SubCategoriesController, '/subcategory')
api.add_resource(SubCategoryController, '/subcategory/<int:subcategoryId>')
api.add_resource(ProductTypesController, '/producttype')
api.add_resource(ProductTypeController, '/producttype/<int:producttypeId>')

if __name__ == '__main__':
    app.run(debug=True)

