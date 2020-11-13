from flask_restful import Resource, reqparse
import boto3
from models.product import ProductModel

s3 = boto3.client('s3',
aws_access_key_id = 'AKIAJE3GDYHJIKN5R3CA',
aws_secret_access_key = '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'
)

BUCKET_NAME = 'imgflask'

class ProductsController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "productName",
        type=str,
        required=True,
        help="productName es obligatorio"
    )
    parser.add_argument(
        "productDesc",
        type=str,
        required=True,
        help="productDesc es obligatorio"
    )
    parser.add_argument(
        "productImg",
        type=str,
        required=True,
        help="productImg es obligatorio"
    )
    parser.add_argument(
        "productPrice",
        type=float,
        required=True,
        help="productPrice es obligatorio"
    )
    parser.add_argument(
        "productStock",
        type=int,
        required=True,
        help="productStock es obligatorio"
    )
    parser.add_argument(
        "markId",
        type=int,
        required=True,
        help="markId es obligatorio"
    )

    def get(self):
        products = ProductModel.query.all()
        listado = []
        for product in products:
            temporal = product.show()
            temporal['marca'] = product.mark.show()
            listado.append(temporal)

        return{
            'ok' : True,
            'message' : '',
            'content' : listado
        }

    def post(self):
        data = self.parser.parse_args()

        product = ProductModel(
            data['productName'],
            data['productDesc'],
            data['productImg'],
            data['productPrice'],
            data['productStock'],
            data['markId']
        )
        try:
            product.save()
            return{
                'ok' : True,
                'message' : 'Producto registrado correctamente',
                'content' : product.show()
            }
        except Exception as e:
            return{
                'ok' : False,
                'message' : None,
                'content' : 'Ocurrio un error : ' + str(e)
            }, 500

class ProductController(Resource):
    def get(self, productId):
        product = ProductModel.query.filter_by(productId=productId).first()
        if product:
            return{
                'ok' : True,
                'message' : None,
                'content' : product.show()
            }
        else:
            return{
                'ok' : False,
                'message' : 'No existe un producto con el id: ' + str(productId),
                'content' : None
            }, 404

    def put(self, productId):
        product = ProductModel.query.filter_by(productId=productId).first()
        if product:
            parser = reqparse.RequestParser()
            parser.add_argument(
                "productName",
                type=str,
                required=True,
                help="productName es obligatorio"
            )
            parser.add_argument(
                "productDesc",
                type=str,
                required=True,
                help="productDesc es obligatorio"
            )
            parser.add_argument(
                "productImg",
                type=str,
                required=True,
                help="productImg es obligatorio"
            )
            parser.add_argument(
                "productPrice",
                type=float,
                required=True,
                help="productPrice es obligatorio"
            )
            parser.add_argument(
                "productStock",
                type=int,
                required=True,
                help="productStock es obligatorio"
            )
            parser.add_argument(
                "markId",
                type=int,
                required=True,
                help="markId es obligatorio"
            )

            data = parser.parse_args()

            product.productName = data['productName']
            product.productDesc = data['productDesc']
            product.productImg = data['productImg']
            product.productPrice = data['productPrice']
            product.productStock = data['productStock']
            product.markId = data['markId']
            product.save()            

            return{
                'ok' : True,
                'message' : 'Producto actualizado correctamente',
                'content' : product.show()
            }
        else:
            return{
                'ok' : False,
                'message' : 'No existe un producto con el id: ' + str(productId),
                'content' : None
            }, 404

    def delete(self, productId):
        product = ProductModel.query.filter_by(productId=productId).first()
        if product:

            if product.state:
                product.state = False
                product.save()
                return{
                    'ok' : True,
                    'message' : 'Producto deshabilitado correctamente',
                    'content' : product.show()
                }
            else:
                return{
                    'ok' : False,
                    'message' : 'Producto ya se encuentra deshabilitado',
                    'content' : product.show()
                }
        else:
            return{
                'ok' : False,
                'message' : 'No existe un producto con el id: ' + str(productId),
                'content' : None
            }, 404