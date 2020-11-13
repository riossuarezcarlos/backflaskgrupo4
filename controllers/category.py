from flask_restful import Resource, reqparse
from models.category import CategoryModel

class CategoriesController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "categoryDesc",
        type=str,
        required=True,
        help="categoryDesc es obligatorio"
    )

    def get(self):
        categories = CategoryModel.query.all()
        listado = []
        for category in categories:
            listado.append(category.show())
        
        return{
            'ok': True,
            'message': None,
            'content': listado
        }

    def post(self):
        data = self.parser.parse_args()
        category = CategoryModel(data['categoryDesc'])
        try:
            category.save()
            return{
                'ok': True,
                'message': 'Categoria registrada correctamente',
                'content': category.show()
            }
        except Exception as e:
            return{
                'ok': False,
                'message': 'Ocurrio un error: ' + str(e),
                'content': None
            }, 500

class CategoryController(Resource):
    def get(self, categoryId):
        category = CategoryModel.query.filter_by(categoryId = categoryId).first()

        listado = []    
        subcategories = []
        temporal = category.show()
        for subcategory in category.subcategories:
            subcategories.append(subcategory.show())
        temporal['subcategorias'] = subcategories
        listado.append(temporal)
 
        if category:
            return{
                'ok': True,
                'message': '',
                'content': listado
            }
        else:
            return{
                'ok': False,
                'message': 'No existe categoria con id: ' + str(categoryId),
                'content': None
            }, 404

    def put(self, categoryId):
        category = CategoryModel.query.filter_by(categoryId = categoryId).first()
        if category:
            parser = reqparse.RequestParser()
            parser.add_argument(
                "categoryDesc",
                type=str,
                required=True,
                help="categoryDesc es obligatorio"
            )

            data = parser.parse_args()
            category.categoryDesc = data['categoryDesc']
            category.save()

            return{
                'ok': True,
                'message': 'Categoria actualizada correctamente',
                'content': category.show()
            }
        else:
            return{
                'ok': False,
                'message': 'No existe categoria con id: ' + str(categoryId),
                'content': None
            }, 404
    
    def delete(self, categoryId):
        category = CategoryModel.query.filter_by(categoryId = categoryId).first()
        if category:
            if category.state:
                category.state = False
                category.save()
                return{
                    'ok': True,
                    'message': '',
                    'content': category.show()
                }
            else:
                return{
                    'ok': False,
                    'message': 'Cateogoria ya se encuentra deshabilitada',
                    'content': None
                }
        else:
            return{
                'ok': False,
                'message': 'No existe categoria con id: ' + str(categoryId),
                'content': None
            }, 404