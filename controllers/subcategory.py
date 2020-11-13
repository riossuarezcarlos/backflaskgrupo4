from flask_restful import Resource, reqparse
from models.subcategory import SubCategoryModel

class SubCategoriesController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "subcategoryDesc",
        type=str,
        required=True,
        help="subcategoryDesc es obligatorio"
    )
    parser.add_argument(
        "categoryId",
        type=int,
        required=True,
        help="categoryId es obligatorio"
    )

    def get(self):
        subcategories = SubCategoryModel.query.all()
        listado = []
        for subcategory in subcategories:
            listado.append(subcategory.show())
        
        return{
            'ok': True,
            'message': None,
            'content': listado
        }

    def post(self):
        data = self.parser.parse_args()
        subcategory = SubCategoryModel(data['subcategoryDesc'], data['categoryId'])
        try:
            subcategory.save()
            return{
                'ok': True,
                'message': 'Subcategoria registrado correctamente',
                'content': subcategory.show()
            }
        except Exception as e:
            return{
                'ok': False,
                'message': 'Ocurrio un error: ' + str(e),
                'content': None
            }, 500

class SubCategoryController(Resource):
    def get(self, subcategoryId):
        subcategory = SubCategoryModel.query.filter_by(subcategoryId = subcategoryId).first()

        listado = []
        temporal = subcategory.show()
        temporal['categorias'] = subcategory.category.show()
        listado.append(temporal)


        if subcategory:
            return{
                'ok': True,
                'message': '',
                'content': listado
            }
        else:
            return{
                'ok': False,
                'message': 'No existe subcategoria con id: ' + str(subcategoryId),
                'content': None
            }, 404

    def put(self, subcategoryId):
        subcategory = SubCategoryModel.query.filter_by(subcategoryId = subcategoryId).first()
        if subcategory:
            parser = reqparse.RequestParser()
            parser.add_argument(
                "subcategoryDesc",
                type=str,
                required=True,
                help="subcategoryDesc es obligatorio"
            )
            parser.add_argument(
                "categoryId",
                type=int,
                required=True,
                help="categoryId es obligatorio"
            )

            data = parser.parse_args()
            subcategory.subcategoryDesc = data['subcategoryDesc']
            subcategory.categoryId = data['categoryId']
            subcategory.save()

            return{
                'ok': True,
                'message': 'Subcategoria actualizada correctamente',
                'content': subcategory.show()
            }
        else:
            return{
                'ok': False,
                'message': 'No existe subcategoria con id: ' + str(subcategoryId),
                'content': None
            }, 404
    
    def delete(self, labelId):
        subcategory = SubCategoryModel.query.filter_by(subcategoryId = subcategoryId).first()
        if subcategory:
            if subcategory.state:
                subcategory.state = False
                subcategory.save()
                return{
                    'ok': True,
                    'message': '',
                    'content': subcategory.show()
                }
            else:
                return{
                    'ok': False,
                    'message': 'Subcategoria ya se encuentra deshabilitada',
                    'content': None
                }
        else:
            return{
                'ok': False,
                'message': 'No existe subcategoria con id: ' + str(subcategoryId),
                'content': None
            }, 404