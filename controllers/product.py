from flask_restful import Resource, reqparse
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

import boto3

from models.product import ProductModel

s3 = boto3.client('s3',
aws_access_key_id = 'AKIAJY3DK7BZYFXIHLFQ',
aws_secret_access_key = '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'
)

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
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

class ProductImgController(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage, location='files')
        data = parse.parse_args()
        print(data)
        img = data['file']
        
        if img:
            
            filename = secure_filename(img.filename)
            response = s3.upload_file(
                Body=img,
                Bucket = BUCKET_NAME,
                Key = filename
            ) 
            print(response)
            
        return{
            'ok' : True,
            'message' : 'Upload Done'
        }
        
