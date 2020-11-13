from flask_restful import Resource, reqparse
from models.mark import MarkModel

class MarksController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "markDesc",
        type=str,
        required=True,
        help="markDesc es obligatorio"
    )

    def get(self):
        marks = MarkModel.query.all()
        listado = []
        for mark in marks:
            temporal = mark.show()
            products = []
            for product in mark.products:
                products.append(product.show())
            temporal['productos'] = products
            listado.append(temporal)

        return{
            'ok' : True,
            'message' : None,
            'content' : listado
        }
    
    def post(self):
        data = self.parser.parse_args()
        mark = MarkModel(data['markDesc'])
        try:
            mark.save()
            return{
                'ok' : True,
                'message' : 'Marca registrada correctamente',
                'content' : mark.show()
            }   
        except Exception as e:
            return{
                'ok' : False,
                'message' : 'Ocurrio un error : ' + str(e),
                'content' : None
            }, 500

class MarkController(Resource):
    def get(self, markId):
        mark = MarkModel.query.filter_by(markId=markId).first()

        if mark:
            return{
                'ok' : True,
                'message' : '',
                'content' : mark.show()
            }
        else:
            return{
                'ok' : False,
                'message' : 'No existe una marca con el id: ' + str(markId),
                'content' : None
            }, 404
    
    def put(self, markId):
        mark = MarkModel.query.filter_by(markId=markId).first()

        if mark:

            parser = reqparse.RequestParser()
            parser.add_argument(
                "markDesc",
                type=str,
                required=True,
                help="markDesc es obligatorio"
            )
            data = parser.parse_args()

            mark.markDesc = data['markDesc']
            mark.save()
            return{
                'ok' : True,
                'message' : 'Marca actualizada correctamente',
                'content' : mark.show()
            }
        else:
            return{
                'ok' : False,
                'message' : 'No existe una marca con el id: ' + str(markId),
                'content' : None
            }, 404

    def delete(self, markId):
        mark = MarkModel.query.filter_by(markId=markId).first()

        if mark:
            if mark.state:
                mark.state = False
                mark.save()
                return{
                    'ok' : True,
                    'message' : 'Marca deshabilitada correctamente',
                    'content' : mark.show()
                }
            else:
                return{
                    'ok' : False,
                    'message' : 'Marca ya se encuentra deshabilitada',
                    'content' : mark.show()
                }
        else:
            return{
                'ok' : False,
                'message' : 'No existe una marca con el id: ' + str(markId),
                'content' : None
            }, 404
