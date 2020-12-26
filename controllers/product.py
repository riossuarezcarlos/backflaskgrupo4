from flask_restful import Resource, reqparse
from models.product import ProductModel
from firebaseconfig import firebaseAlmacenamiento
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import werkzeug

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
        "producttypeId",
        type=int,
        required=True,
        help="producttypeId es obligatorio"
    ) 
    parser.add_argument(
        "markId",
        type=int,
        required=True,
        help="markId es obligatorio"
    )
    parser.add_argument(
        "labelId",
        type=int,
        required=True,
        help="labelId es obligatorio"
    )

    def get(self):
        products = ProductModel.query.all()
        listado = []
        for product in products: 
            listado.append(product.show())

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
            data['producttypeId'],
            data['markId'],
            data['labelId']
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

class ProductImage(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location='files')
        # Sending more info in the form? simply add additional arguments, with the location being 'form'
        # parser.add_argument("other_arg", type=str, location='form')
        self.req_parser = parser

    def post(self):
        try:
            image = self.req_parser.parse_args(strict=True).get("image", None)
            fecha = str(datetime.now().timestamp()).replace('.','')
            nombreFinal = fecha + image.filename
            nombre_seguro = secure_filename(nombreFinal)
            image.save(nombre_seguro)
            blobFirebase = firebaseAlmacenamiento.blob(nombre_seguro)
            blobFirebase.upload_from_filename(nombre_seguro)
            blobFirebase.make_public()
            url = blobFirebase.public_url
            os.remove(nombre_seguro)

            return {
                'ok': True,
                'message': 'Se agregó la imagen correctamente',
                'content': url
            }
        except:
            return {
                'ok': False,
                'message': 'Ocurrió un error al agregar la imagen',
                'content': None
            }

 
class ProductController(Resource):
    def get(self, productId):
        product = ProductModel.query.filter_by(productId=productId).first()

        if product:
            listado = product.show()
            listado['marcaDesc'] = product.mark.show()['descripcion']
            listado['etiquetaDesc'] = product.label.show()['descripcion']
            listado['tipoproductoDesc'] = product.producttype.show()['descripcion']
            listado['subcategoria'] = product.producttype.show()['subcategoria']
            listado['categoria'] = product.producttype.subcategory.show()['categoria']
            return{
                'ok' : True,
                'message' : None,
                'content' : listado
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
                "producttypeId",
                type=int,
                required=True,
                help="producttypeId es obligatorio"
            ) 
            parser.add_argument(
                "markId",
                type=int,
                required=True,
                help="markId es obligatorio"
            )
            parser.add_argument(
                "labelId",
                type=int,
                required=True,
                help="labelId es obligatorio"
            )

            data = parser.parse_args()

            product.productName = data['productName']
            product.productDesc = data['productDesc']
            product.productImg = data['productImg']
            product.productPrice = data['productPrice']
            product.productStock = data['productStock'] 
            product.producttypeId = data['producttypeId']
            product.markId = data['markId']
            product.labelId = data['labelId']
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


 
class ProductLabelController(Resource):
    def get(self, labelId):
        products = ProductModel.query.filter_by(labelId=labelId).limit(4).all()

        if products:
            listado = []
            for prod in products:
                listado.append(prod.show())
            
            return{
                'ok': True,
                'message': None,
                'content': listado
            }
        else:
            return{
                'ok' : False,
                'message' : 'No existes productos para esta etiqueta',
                'content' : None
            }, 404 