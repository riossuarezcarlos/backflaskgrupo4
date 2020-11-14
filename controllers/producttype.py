from flask_restful import Resource, reqparse
from models.producttype import ProductTypeModel

class ProductTypesController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "producttypeDesc",
        type=str,
        required=True,
        help="producttypeDesc es obligatorio"
    )
    parser.add_argument(
        "subcategoryId",
        type=int,
        required=True,
        help="subcategoryId es obligatorio"
    )

    def get(self):
        producttypes = ProductTypeModel.query.all()
        listado = []
        for producttype in producttypes:
            listado.append(producttype.show())
        
        return{
            'ok': True,
            'message': None,
            'content': listado
        }

    def post(self):
        data = self.parser.parse_args()
        producttype = ProductTypeModel(data['producttypeDesc'], data['subcategoryId'])
        try:
            producttype.save()
            return{
                'ok': True,
                'message': 'Tipo de producto registrado correctamente',
                'content': producttype.show()
            }
        except Exception as e:
            return{
                'ok': False,
                'message': 'Ocurrio un error: ' + str(e),
                'content': None
            }, 500

class ProductTypeController(Resource):
    def get(self, producttypeId):
        producttype = ProductTypeModel.query.filter_by(producttypeId = producttypeId).first()
        if producttype:
            listado = producttype.show()
            listado['categoria'] = producttype.subcategory.show()['categoria']
            return{
                'ok': True,
                'message': '',
                'content': listado
            }
        else:
            return{
                'ok': False,
                'message': 'No existe tipo de producto con id: ' + str(producttypeId),
                'content': None
            }, 404

    def put(self, producttypeId):
        producttype = ProductTypeModel.query.filter_by(producttypeId = producttypeId).first()
        if producttype:
            parser = reqparse.RequestParser()
            parser.add_argument(
                "producttypeDesc",
                type=str,
                required=True,
                help="producttypeDesc es obligatorio"
            )
            parser.add_argument(
                "subcategoryId",
                type=int,
                required=True,
                help="subcategoryId es obligatorio"
            )

            data = parser.parse_args()
            producttype.producttypeDesc = data['producttypeDesc']
            producttype.subcategoryId = data['subcategoryId']
            producttype.save()

            return{
                'ok': True,
                'message': 'Tipo de producto actualizado correctamente',
                'content': producttype.show()
            }
        else:
            return{
                'ok': False,
                'message': 'No existe tipo de producto con id: ' + str(producttypeId),
                'content': None
            }, 404
    
    def delete(self, producttypeId):
        producttype = ProductTypeModel.query.filter_by(producttypeId = producttypeId).first()
        if producttype:
            if producttype.state:
                producttype.state = False
                producttype.save()
                return{
                    'ok': True,
                    'message': '',
                    'content': producttype.show()
                }
            else:
                return{
                    'ok': False,
                    'message': 'Tiipo de producto ya se encuentra deshabilitado',
                    'content': None
                }
        else:
            return{
                'ok': False,
                'message': 'No existe tipo de producto con id: ' + str(producttypeId),
                'content': None
            }, 404